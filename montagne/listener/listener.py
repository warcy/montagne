import time
import json
from montagne.common import hub
from montagne.common.application import MontagneApp
from montagne.listener.event import (TestListenerEvent, TestListenerRequest,
                                     TestListenerReply)
from montagne.common.wsgi import ControllerBase, route, Response


class BaseListener(MontagneApp):
    def __init__(self):
        super().__init__()


class OpenRainbowListener(BaseListener):
    def __init__(self):
        super(OpenRainbowListener, self).__init__()
        pass


class TestListener(BaseListener):
    def __init__(self):
        super(TestListener, self).__init__()
        self.wsgi_controller = TestListenerController

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


class TestListenerController(ControllerBase):
    def __init__(self, req, link, data, **config):
        super(TestListenerController, self).__init__(req, link, data, **config)
        self.inst = data[TestListener.__name__]

    @route('template', '/template_resource', methods=['GET'])
    def test_handler(self, req, **kwargs):
        return Response(content_type='application/json', charset='UTF-8',
                        body=json.dumps({'test msg': 'hello montage.'}),
                        status=200)
