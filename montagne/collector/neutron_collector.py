from montagne import cfg
import time
from montagne.common import hub
from montagne.collector.collector import OpenStackCollector
from montagne.openstack_client.event import GetNeutronClientRequest
from montagne.collector import event as cl_ev


CONF = cfg.CONF
CONF.register_opts([
    cfg.IntOpt('pull_agent_interval', default=60,
               help='pull interval of agent(seconds).'),
    cfg.IntOpt('pull_lb_member_interval', default=60,
               help='pull interval of loadbalancer member(seconds).')
], 'neutron_collector')


class NeutronCollector(OpenStackCollector):
    def __init__(self):
        super(NeutronCollector, self).__init__()
        self.pull_agent_interval = \
            CONF.neutron_collector.pull_agent_interval
        self.pull_lb_member_interval = \
            CONF.neutron_collector.pull_lb_member_interval
        print(self.pull_agent_interval)

        self.neutron = None
        self._agents = None
        self._lb_members = None
        self.ovs_agents = {}
        self.lbaas_agents = {}
        self.lb_members = {}
        self.event_handlers = {
            cl_ev.GetOVSAgentRequest: self.reply_ovs_agents,
            cl_ev.GetLBMemberRequest: self.reply_lb_members
        }
        hub.spawn(self._get_neutron_client)

    def serve(self):
        self.thread(self._get_agents_loop)
        self.thread(self._get_lb_members_loop)

    def reply_ovs_agents(self, req):
        tunnel_ip = req.msg
        ovs_agent = self.ovs_agents.get(tunnel_ip)
        rep = cl_ev.GetOVSAgentReply(ovs_agent)
        self.reply_to_request(req, rep)

    def reply_lb_members(self, req):
        ip_list = req.msg
        rval = {}
        for ip in ip_list:
            member = self.lb_members.get(ip)
            if member:
                rval.setdefault(ip, member)
        rep = cl_ev.GetLBMemberReply(rval)
        self.reply_to_request(req, rep)

    def sync_agents(self):
        self.ovs_agents, self.lbaas_agents = self.neutron.sync_agent()

    def sync_lb_members(self):
        self.lb_members = self.neutron.sync_lb_members()

    def _get_agents_loop(self):
        while True:
            timestamp = time.time()
            if self.neutron:
                self.sync_agents()
                self.LOG.debug(
                    "get neutron agents, ovs-agent:%s, lbaas-agent:%s",
                    self.ovs_agents.keys(), self.lbaas_agents.keys())
            hub.sleep(
                self.pull_agent_interval - (time.time() - timestamp))

    def _get_lb_members_loop(self):
        while True:
            timestamp = time.time()
            if self.neutron:
                self.sync_lb_members()
                self.LOG.debug(
                    "get lb members, ovs-agent:%s",
                    self.lb_members.keys())
            hub.sleep(
                self.pull_lb_member_interval - (time.time() - timestamp))

    def _get_neutron_client(self):
        while True and (not self.neutron):
            reply = self.send_request(GetNeutronClientRequest(msg=None))
            self.neutron = reply.msg
            hub.sleep(0.5)
        self.sync_agents()
        self.sync_lb_members()
