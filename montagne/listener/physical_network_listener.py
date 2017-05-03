import json
from montagne.listener.listener import BaseListener
from montagne.common.wsgi import ControllerBase, route, Response
from montagne.common.http_methods import decode
from montagne.scheduler.event import (EdgePhySwitchDownEvent,
                                      EdgePhySwitchPortDownEvent)


class PhysicalNetworkListener(BaseListener):
    def __init__(self):
        super(PhysicalNetworkListener, self).__init__()
        self.wsgi_controller = PhysicalNetworkListenerController


class PhysicalNetworkListenerController(ControllerBase):
    def __init__(self, req, link, data, **config):
        super(PhysicalNetworkListenerController, self).__init__(
            req, link, data, **config)
        self.inst = data[PhysicalNetworkListener.__name__]

    @route('physical_network', '/event/switch', methods=['POST'])
    def edge_phy_switch_down(self, req, **kwargs):
        payload = decode(req.body)
        tunnel_ip = payload.get('tunnel_ip')
        if tunnel_ip:
            self.inst.send_event(EdgePhySwitchDownEvent(payload))
            return Response(status=200)
        else:
            return Response(content_type='application/json', charset='UTF-8',
                            body=json.dumps({'msg': 'tunnel_ip not found'}),
                            status=404)

    @route('physical_network', '/event/switch/port', methods=['POST'])
    def edge_phy_switch_port_down(self, req, **kwargs):
        payload = decode(req.body)
        tunnel_ip = payload.get('tunnel_ip')
        if tunnel_ip:
            self.inst.send_event(EdgePhySwitchPortDownEvent(payload))
            return Response(status=200)
        else:
            return Response(content_type='application/json', charset='UTF-8',
                            body=json.dumps({'msg': 'tunnel_ip not found'}),
                            status=404)
