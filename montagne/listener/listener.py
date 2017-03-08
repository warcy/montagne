import time
from montagne.common import hub
from montagne.common.application import MontagneApp
from montagne.listener.event import (TestListenerEvent, TestListenerRequest,
                                     TestListenerReply)


class BaseListener(MontagneApp):
    def __init__(self):
        super().__init__()


class OpenRainbowListener(BaseListener):
    def __init__(self):
        super(OpenRainbowListener, self).__init__()
        pass


class TestListener(BaseListener):
    def __init__(self):
        super().__init__()

    def serve(self):
        self.thread(self._mock_rcv)

    def _mock_rcv(self):
        while True:
            timestamp = time.time()
            msg = 'listener receive msg and send to Scheduler'

            self.send_event(
                TestListenerEvent(msg=('async event:' + msg)))

            self.LOG.info('send msg %s to Scheduler', msg+' in async way')

            self.LOG.info('send msg %s to Scheduler', msg + ' in sync way')
            reply = self.send_request(
                TestListenerRequest(msg='sync request'))
            self.LOG.info('reply: %s', reply.msg)
            self.LOG.info('do some other things...')

            hub.sleep(
                5 - (time.time() - timestamp))
