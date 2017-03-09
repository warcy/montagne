import time
import json
from montagne.notifier.notifier import BaseNotifier
from montagne.common import hub, http_methods


class RestNotifier(BaseNotifier):
    def __init__(self):
        super(RestNotifier, self).__init__()

    def serve(self):
        self.thread(self._mock_notice)

    def _mock_notice(self):
        while True:
            timestamp = time.time()
            self.LOG.debug('get %s', self.get_test())
            self.LOG.debug('post %s', self.post_test())
            hub.sleep(
                5 - (time.time() - timestamp))

    def get_test(self):
        url = 'http://203.0.113.3:8088/hostmanage/server_acl'
        return http_methods.get(url)

    def post_test(self):
        url = 'http://203.0.113.3:8088/hostmanage/server_acl'
        data = [
            {
                "ip_addr": "203.0.113.14",
                "service_type": "VIDEO"
            },
            {
                "ip_addr": "203.0.113.21",
                "service_type": "USER"
            }
        ]
        edata = http_methods.encode(data)
        return http_methods.put(url, edata)
