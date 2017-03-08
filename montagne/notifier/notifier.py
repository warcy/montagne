import time
from montagne.common import hub
from montagne.common.application import MontagneApp


class BaseNotifier(MontagneApp):
    def __init__(self):
        super(BaseNotifier, self).__init__()


class OpenRainbowNotifier(BaseNotifier):
    def __init__(self):
        super(OpenRainbowNotifier, self).__init__()
        pass


class TestNotifier(BaseNotifier):
    def __init__(self):
        super().__init__()
