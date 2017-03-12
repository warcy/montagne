import time
import json
from montagne.notifier.notifier import BaseNotifier
from montagne.common import hub, http_methods


class RestNotifier(BaseNotifier):
    """
    Usage:

    1. inherit from RestNotifier
    2. override self.action_mapper,
       action_name is only used to get method info.

    3. get the instance of notifier and use method send_message()
       to GET/POST/PUT/DELETE with action_name

    Example: ::

        class TestRestNotifier(RestNotifier):
            def __init__(self):
                super(TestRestNotifier, self).__init__()
                # {action_name: [http_method, host, port, path]}
                self.action_mapper = {
                    'edge_switch_down':
                        ['POST', '0.0.0.0', '8080',
                         '/openrainbow/edge_switch_down'],
                }

        test_rest_notifier = TestRestNotifier()
        action_name = 'edge_switch_down'
        data = http_methods.encode({"tunnel_ip": "10.0.1.31"})
        hub.spawn(test_rest_notifier.send_message, action_name, data)

    """
    def __init__(self):
        super(RestNotifier, self).__init__()
        self.url_template = 'http://{}:{}{}'
        self.http_method_mapper = {
            'GET': http_methods.get,
            'POST': http_methods.post,
            'PUT': http_methods.put,
            'DELETE': http_methods.delete}

        # override by your own actions
        # {action_name: [http_method, host, port, path]}
        self.action_mapper = {}

    def send_message(self, action_name, data=None):
        actions = self.action_mapper.get(action_name)
        if not actions:
            # no registered action found.
            return None

        method = self.http_method_mapper.get(actions[0])
        url = self.url_template.format(
            actions[1], actions[2], actions[3])
        recv_data = method(url=url, data=data)
        return http_methods.decode(recv_data)

