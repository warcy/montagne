from montagne.common.application import MontagneApp


class BaseNotifier(MontagneApp):
    def __init__(self):
        super(BaseNotifier, self).__init__()
