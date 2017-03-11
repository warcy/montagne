from montagne.common.credentials import get_neutron_credentials
from neutronclient.v2_0 import client as neutronclient
from neutronclient.common import exceptions
from montagne.common.neutron_constants import (AGENT_TYPE_OVS,
                                               AGENT_TYPE_LOADBALANCER)
from montagne.common.openstack_object import OVSAgent, LBAgent, LBMember
from montagne.common.application import MontagneApp
from montagne.openstack_client import event as oc_ev
from montagne.common.utils import unicode_fmt


class NeutronClient(MontagneApp):
    def __init__(self):
        super(NeutronClient, self).__init__()
        self._credentials = get_neutron_credentials()
        self.neutron_client = neutronclient.Client(**self._credentials)
        # check neutron client connection
        self.neutron_client.list_agents()

        self.event_handlers = {
            oc_ev.GetNeutronClientRequest: self.reply_client
        }

    def reply_client(self, req):
        rep = oc_ev.GetNeutronClientReply(msg=self)
        self.reply_to_request(req, rep)

    def sync_agent(self):
        try:
            data = self.neutron_client.list_agents()
            fmt_data = unicode_fmt(data)
        except exceptions.NeutronException as e:
            self.LOG.exception(e)
            return None, None
        agents_list = fmt_data['agents']
        ovs_agents = {}
        lb_agents = {}
        for a in agents_list:
            if a['agent_type'] == AGENT_TYPE_OVS:
                na = OVSAgent(**a)
                ovs_agents[na.configuration.tunneling_ip] = na
            elif a['agent_type'] == AGENT_TYPE_LOADBALANCER:
                na = LBAgent(**a)
                lb_agents[na.id] = na
            else:
                pass
        return ovs_agents, lb_agents

    def sync_lb_members(self):
        try:
            data = self.neutron_client.list_members()
            fmt_data = unicode_fmt(data)
        except exceptions.NeutronException as e:
            self.LOG.exception(e)
            return None
        lb_members_list = fmt_data['members']
        lb_members = {}
        for m in lb_members_list:
            lm = LBMember(**m)
            lb_members[lm.address] = lm
        return lb_members
