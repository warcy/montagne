class BaseEvent(object):
    def __init__(self):
        super(BaseEvent, self).__init__()
        self.src = None
        self.dst = None


class BaseRequest(BaseEvent):
    def __init__(self):
        super(BaseRequest, self).__init__()
        self.reply_queue = None


class BaseReply(BaseEvent):
    def __init__(self):
        super(BaseReply, self).__init__()
