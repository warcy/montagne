from montagne.common.application import MontagneApp
from montagne.common.credentials import get_ceilometer_credentials
from ceilometerclient import client as ceilometerclient


class CeilometerClient(MontagneApp):
    def __init__(self):
        super(CeilometerClient, self).__init__()
        self._credentials = get_ceilometer_credentials()
        self.ceilometer_client = ceilometerclient.get_client(**self._credentials)
