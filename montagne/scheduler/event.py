from montagne.common.event import BaseEvent, BaseRequest, BaseReply

dst_to_scheduler = 'montagne.scheduler.scheduler'


class EdgePhySwitchDownEvent(BaseEvent):
    def __init__(self, msg):
        super(EdgePhySwitchDownEvent, self).__init__()
        self.dst = dst_to_scheduler
        self.msg = msg
