from montagne.common import hub
from montagne.common.application import MontagneApp
from montagne.scheduler import event as sc_ev
from montagne.collector.event import GetOVSAgentRequest, GetHypervisorRequest, GetLBMemberRequest
from montagne.openstack_client.event import GetNeutronClientRequest, GetNovaClientRequest
from montagne.notifier.event import DeleteLBMemberEvent


class Scheduler(MontagneApp):
    def __init__(self):
        super(Scheduler, self).__init__()
        self.neutron = None
        self.nova = None
        self.event_handlers = {
            sc_ev.EdgePhySwitchDownEvent: self.edge_phy_switch_down,
            sc_ev.EdgePhySwitchPortDownEvent: self.edge_phy_switch_port_down
        }
        hub.spawn(self._get_neutron_client)
        hub.spawn(self._get_nova_client)

    def edge_phy_switch_down(self, ev):
        msg = ev.msg
        tunnel_ip_list = msg.get('tunnel_ip')
        dpid = msg.get('dpid')
        status = msg.get('status')
        self.LOG.debug("switch %s down, affected tunnel_ip: %s",
                       dpid, tunnel_ip_list)

        for tunnel_ip in tunnel_ip_list:
            # get affected tunnel agent by tunnel ip
            ovs_agent = self.send_request(GetOVSAgentRequest(tunnel_ip)).msg
            if not ovs_agent:
                self.LOG.warning("ovs agent not found(tunnel_ip=%s)", tunnel_ip)
                return

            # get hypervisor/phy server by agent.hostname
            host = ovs_agent.host
            hypervisor = self.send_request(GetHypervisorRequest(host)).msg
            if not hypervisor:
                self.LOG.warning("hypervisor not found(hypervisor=%s)", host)
                return
            self.LOG.debug("hypervisor [%s] with instances: %s",
                           host, hypervisor.servers.keys())

            # TODO: call novaclient methods directly to find specific
            #       servers/instances, will be a bottleneck.
            for server_uuid in hypervisor.servers:
                hub.spawn(self._thread_edge_phy_switch_down, server_uuid)

    def _thread_edge_phy_switch_down(self, server_uuid):
        # get specific server/instance information.
        server = self.nova.get_server_by_id(server_uuid)
        if not server:
            return

        srv_dict = {}
        # get server/instance ip and build dict = {server_ip: tenant_id},
        # because single server may have multiple ip address.
        for network_name, address_list in server.networks.items():
            for ip_addr in address_list:
                srv_dict.setdefault(ip_addr, server.tenant_id)

        # check server/instance having load balance service or not.
        # as we get load balance members by fix ip address from nova,
        # we check tenant id to make sure it's the same one in neutron.
        inst_ip_list = srv_dict.keys()
        lb_members = self.send_request(GetLBMemberRequest(inst_ip_list)).msg
        deprecated_members = []
        for ip, lb_member in lb_members.items():
            if lb_member.tenant_id != srv_dict[ip]:
                deprecated_members.append(ip)
        for dm in deprecated_members:
            lb_members.pop(dm)
        self.LOG.debug("affected lb members: %s", lb_members.keys())

        # send affected lb members to notifier.
        if lb_members:
            self.send_event(DeleteLBMemberEvent(lb_members))

    def edge_phy_switch_port_down(self, ev):
        msg = ev.msg
        tunnel_ip_list = msg.get('tunnel_ip')
        dpid = msg.get('dpid')
        port_no = msg.get('port_no')
        status = msg.get('status')
        self.LOG.debug("switch %s port %s down, affected tunnel_ip: %s",
                       dpid, port_no, tunnel_ip_list)

        for tunnel_ip in tunnel_ip_list:
            # get affected tunnel agent by tunnel ip
            ovs_agent = self.send_request(GetOVSAgentRequest(tunnel_ip)).msg
            if not ovs_agent:
                self.LOG.warning("ovs agent not found(tunnel_ip=%s)", tunnel_ip)
                return

            # get hypervisor/phy server by agent.hostname
            host = ovs_agent.host
            hypervisor = self.send_request(GetHypervisorRequest(host)).msg
            if not hypervisor:
                self.LOG.warning("hypervisor not found(hypervisor=%s)", host)
                return
            self.LOG.debug("hypervisor [%s] with instances: %s",
                           host, hypervisor.servers.keys())

            # TODO: call novaclient methods directly to find specific
            #       servers/instances, will be a bottleneck.
            for server_uuid in hypervisor.servers:
                hub.spawn(self._thread_edge_phy_switch_down, server_uuid)

    def _get_neutron_client(self):
        while True and (not self.neutron):
            reply = self.send_request(GetNeutronClientRequest(msg=None))
            self.neutron = reply.msg
            hub.sleep(0.5)

    def _get_nova_client(self):
        while True and (not self.nova):
            reply = self.send_request(GetNovaClientRequest(msg=None))
            self.nova = reply.msg
            hub.sleep(0.5)
