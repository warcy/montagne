from montagne.common.application import MontagneApp
from montagne.common.credentials import get_nova_v1_1_credentials
from novaclient.v1_1 import client as novaclient
from montagne.openstack_client import event as oc_ev


class NovaClient(MontagneApp):
    def __init__(self):
        super(NovaClient, self).__init__()
        self._credentials = get_nova_v1_1_credentials()
        self.nova_client = novaclient.Client(**self._credentials)
        self.event_handlers = {
            oc_ev.GetNovaClientRequest: self.reply_client
        }

    def reply_client(self, req):
        rep = oc_ev.GetNovaClientReply(msg=self.nova_client)
        self.reply_to_request(req, rep)
