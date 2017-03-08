from montagne.common.event import BaseEvent, BaseRequest, BaseReply

dst_to_scheduler = 'montagne.scheduler.scheduler'


class TestListenerEvent(BaseEvent):
    def __init__(self, msg):
        super(TestListenerEvent, self).__init__()
        self.dst = dst_to_scheduler
        self.msg = msg


class TestListenerRequest(BaseRequest):
    def __init__(self, msg):
        super(TestListenerRequest, self).__init__()
        self.dst = dst_to_scheduler
        self.msg = msg


class TestListenerReply(BaseReply):
    def __init__(self, msg):
        super(TestListenerReply, self).__init__()
        self.msg = msg
