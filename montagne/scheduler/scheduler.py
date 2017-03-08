
from montagne.common import hub
from montagne.common.application import MontagneApp
from montagne.listener import event as listener_ev


class Scheduler(MontagneApp):
    def __init__(self):
        super(Scheduler, self).__init__()
        self.event_handlers = {
            listener_ev.TestListenerEvent: self.receive_event,
            listener_ev.TestListenerRequest: self.receive_request
        }

    def receive_event(self, ev):
        self.LOG.debug("scheduler receive event: [%s]",
                       ev.msg)

    def receive_request(self, req):
        self.LOG.debug("scheduler receive request: [%s]",
                       req.msg)
        rep = listener_ev.TestListenerReply(msg='sync reply')
        self.reply_to_request(req, rep)
