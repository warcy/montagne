from montagne.common import hub
from montagne.notifier.notifier import BaseNotifier
from montagne.openstack_client.event import GetNeutronClientRequest


class NeutronNotifier(BaseNotifier):
    def __init__(self):
        super(NeutronNotifier, self).__init__()
        self.neutron = None
        hub.spawn(self._get_neutron_client)

    def _get_neutron_client(self):
        while True and (not self.neutron):
            reply = self.send_request(GetNeutronClientRequest(msg=None))
            self.neutron = reply.msg
            hub.sleep(0.5)
