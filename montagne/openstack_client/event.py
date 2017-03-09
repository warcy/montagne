from montagne.common.event import BaseEvent, BaseRequest, BaseReply

dst_to_novaclient = 'montagne.openstack_client.nova_client'
dst_to_neutronclient = 'montagne.openstack_client.neutron_client'


class GetNovaClientRequest(BaseRequest):
    def __init__(self, msg):
        super(GetNovaClientRequest, self).__init__()
        self.dst = dst_to_novaclient
        self.msg = msg


class GetNovaClientReply(BaseReply):
    def __init__(self, msg):
        super(GetNovaClientReply, self).__init__()
        self.msg = msg


class GetNeutronClientRequest(BaseRequest):
    def __init__(self, msg):
        super(GetNeutronClientRequest, self).__init__()
        self.dst = dst_to_neutronclient
        self.msg = msg


class GetNeutronClientReply(BaseReply):
    def __init__(self, msg):
        super(GetNeutronClientReply, self).__init__()
        self.msg = msg
