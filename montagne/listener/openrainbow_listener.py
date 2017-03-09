import json
from montagne.listener.listener import BaseListener
from montagne.common.wsgi import ControllerBase, route, Response


class OpenRainbowListener(BaseListener):
    def __init__(self):
        super(OpenRainbowListener, self).__init__()
        self.wsgi_controller = OpenRainbowListenerController

    def edge_phy_switch_down(self, req):
        pass


class OpenRainbowListenerController(ControllerBase):
    def __init__(self, req, link, data, **config):
        super(OpenRainbowListenerController, self).__init__(
            req, link, data, **config)
        self.inst = data[OpenRainbowListener.__name__]

    @route('openrainbow', '/openrainbow', methods=['POST'])
    def edge_phy_switch_down(self, req, **kwargs):
        self.inst.edge_phy_switch_down(req)
        return Response(status=200)
