from montagne.common.application import MontagneApp


class BaseCollector(MontagneApp):
    def __init__(self):
        super(BaseCollector, self).__init__()


class RestCollector(BaseCollector):
    def __init__(self):
        super(RestCollector, self).__init__()
        pass


class OpenStackCollector(BaseCollector):
    def __init__(self):
        super(OpenStackCollector, self).__init__()
        pass
