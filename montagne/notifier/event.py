from montagne.common.event import BaseEvent, BaseRequest, BaseReply

dst_to_neutron_notifier = 'montagne.notifier.neutron_notifier'


class DeleteLBMemberEvent(BaseEvent):
    def __init__(self, msg):
        super(DeleteLBMemberEvent, self).__init__()
        self.dst = dst_to_neutron_notifier
        self.msg = msg
