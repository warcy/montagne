from montagne.common.event import BaseEvent, BaseRequest, BaseReply

dst_to_neutron_collector = 'montagne.collector.neutron_collector'
dst_to_nova_collector = 'montagne.collector.nova_collector'


class GetOVSAgentRequest(BaseRequest):
    def __init__(self, msg):
        super(GetOVSAgentRequest, self).__init__()
        self.dst = dst_to_neutron_collector
        self.msg = msg


class GetOVSAgentReply(BaseReply):
    def __init__(self, msg):
        super(GetOVSAgentReply, self).__init__()
        self.msg = msg


class GetHypervisorRequest(BaseRequest):
    def __init__(self, msg):
        super(GetHypervisorRequest, self).__init__()
        self.dst = dst_to_nova_collector
        self.msg = msg


class GetHypervisorReply(BaseReply):
    def __init__(self, msg):
        super(GetHypervisorReply, self).__init__()
        self.msg = msg


class GetLBMemberRequest(BaseRequest):
    def __init__(self, msg):
        super(GetLBMemberRequest, self).__init__()
        self.dst = dst_to_neutron_collector
        self.msg = msg


class GetLBMemberReply(BaseReply):
    def __init__(self, msg):
        super(GetLBMemberReply, self).__init__()
        self.msg = msg

