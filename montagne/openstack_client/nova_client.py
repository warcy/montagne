from montagne.common.application import MontagneApp
from montagne.common.credentials import get_nova_v1_1_credentials
from novaclient.v1_1 import client as novaclient
from novaclient.exceptions import NotFound as NovaResourceNotFound
from montagne.openstack_client import event as oc_ev


def nova_api_handler(func):
    def wrapper(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except NovaResourceNotFound:
            return None
    return wrapper


class NovaClient(MontagneApp):
    def __init__(self):
        super(NovaClient, self).__init__()
        self._credentials = get_nova_v1_1_credentials()
        self.nova_client = novaclient.Client(**self._credentials)
        # check nova client connection
        self.get_all_hypervisors()

        self.event_handlers = {
            oc_ev.GetNovaClientRequest: self.reply_client
        }

    def reply_client(self, req):
        rep = oc_ev.GetNovaClientReply(msg=self)
        self.reply_to_request(req, rep)

    @nova_api_handler
    def get_hypervisor(self, **kwargs):
        return self.nova_client.hypervisors.find(**kwargs)

    @nova_api_handler
    def get_all_hypervisors(self, **kwargs):
        return self.nova_client.hypervisors.findall(**kwargs)

    @nova_api_handler
    def get_hypervisor_by_hostname(self, hostname):
        return self.nova_client.hypervisors.find(hypervisor_hostname=hostname)

    @nova_api_handler
    def get_hypervisor_by_id(self, hypervisor_id):
        return self.nova_client.hypervisors.get(hypervisor_id)

    @nova_api_handler
    def get_hypervisor_with_server(self, hostname):
        return self.nova_client.hypervisors.search(hypervisor_match=hostname,
                                                   servers=True)

    @nova_api_handler
    def get_server_by_id(self, server_id):
        return self.nova_client.servers.get(server_id)

    @nova_api_handler
    def get_servers(self, search_opts):
        return self.nova_client.servers.list(search_opts=search_opts)
