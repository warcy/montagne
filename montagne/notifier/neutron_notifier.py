from montagne.common import hub
from montagne.notifier.notifier import BaseNotifier
from montagne.openstack_client.event import GetNeutronClientRequest
from montagne.notifier import event as nt_ev


class NeutronNotifier(BaseNotifier):
    def __init__(self):
        super(NeutronNotifier, self).__init__()
        self.neutron = None
        self.event_handlers = {
            nt_ev.DeleteLBMemberEvent: self.delete_lb_member
        }
        hub.spawn(self._get_neutron_client)

    def delete_lb_member(self, ev):
        lb_members = ev.msg
        self.LOG.info("remove load balance pool members: %s",
                      [v.id for k, v in lb_members.items()])
        for ip, lb_member in lb_members.items():
            hub.spawn(self.neutron.neutron_client.delete_member, lb_member.id)

    def _get_neutron_client(self):
        while True and (not self.neutron):
            reply = self.send_request(GetNeutronClientRequest(msg=None))
            self.neutron = reply.msg
            hub.sleep(0.5)
