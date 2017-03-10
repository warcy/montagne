import json
from montagne.listener.listener import BaseListener
from montagne.common.wsgi import ControllerBase, route, Response
from montagne.common.http_methods import decode
from montagne.scheduler.event import EdgePhySwitchDownEvent


class OpenRainbowListener(BaseListener):
    def __init__(self):
        super(OpenRainbowListener, self).__init__()
        self.wsgi_controller = OpenRainbowListenerController


class OpenRainbowListenerController(ControllerBase):
    def __init__(self, req, link, data, **config):
        super(OpenRainbowListenerController, self).__init__(
            req, link, data, **config)
        self.inst = data[OpenRainbowListener.__name__]

    @route('openrainbow', '/openrainbow/edge_switch_down', methods=['POST'])
    def edge_phy_switch_down(self, req, **kwargs):
        payload = decode(req.body)
        tunnel_ip = payload.get('tunnel_ip')
        if tunnel_ip:
            self.inst.send_event(EdgePhySwitchDownEvent(tunnel_ip))
            return Response(status=200)
        else:
            return Response(content_type='application/json', charset='UTF-8',
                            body=json.dumps({'msg': 'tunnel_ip not found'}),
                            status=404)
