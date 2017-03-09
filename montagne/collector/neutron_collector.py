import time
from montagne.common import hub
from montagne.common.utils import unicode_fmt
from montagne.common.neutron_constants import (AGENT_TYPE_OVS,
                                               AGENT_TYPE_LOADBALANCER)
from montagne.common.openstack_object import OVSAgent, LBAgent
from montagne.collector.collector import OpenStackCollector
from montagne.openstack_client.event import GetNeutronClientRequest


class NeutronCollector(OpenStackCollector):
    poll_agent_interval = 10

    def __init__(self):
        super(NeutronCollector, self).__init__()
        self.neutron = None
        self._agents = None
        self.ovs_agents = {}
        self.lbaas_agents = {}

    def serve(self):
        self.thread(self._get_agents_loop)

    def _get_agents_loop(self):
        while True:
            timestamp = time.time()
            if self.neutron:
                self.sync_agents()
                self.LOG.debug(
                    "get neutron agents, ovs-agent:%s, lbaas-agent:%s",
                    self.ovs_agents.keys(), self.lbaas_agents.keys())
            else:
                reply = self.send_request(GetNeutronClientRequest(msg=None))
                self.neutron = reply.msg
                continue
            hub.sleep(
                self.poll_agent_interval - (time.time() - timestamp))

    def sync_agents(self):
        agents = self.neutron.list_agents()
        try:
            self._agents = unicode_fmt(agents)
        except:
            raise

        self._instance_agents()

    def _instance_agents(self):
        agents_list = self._agents['agents']

        for a in agents_list:
            if a['agent_type'] == AGENT_TYPE_OVS:
                na = OVSAgent(**a)
                self.ovs_agents[na.configuration.tunneling_ip] = na
            elif a['agent_type'] == AGENT_TYPE_LOADBALANCER:
                na = LBAgent(**a)
                self.lbaas_agents[na.id] = na
            else:
                pass