from montagne.common.credentials import get_neutron_credentials
from neutronclient.v2_0 import client as neutronclient
from montagne.common.application import MontagneApp
from montagne.openstack_client import event as oc_ev


class NeutronClient(MontagneApp):
    def __init__(self):
        super(NeutronClient, self).__init__()
        self._credentials = get_neutron_credentials()
        self.neutron_client = neutronclient.Client(**self._credentials)
        self.event_handlers = {
            oc_ev.GetNeutronClientRequest: self.reply_client
        }

    def reply_client(self, req):
        rep = oc_ev.GetNeutronClientReply(msg=self.neutron_client)
        self.reply_to_request(req, rep)
