import time
from montagne.common import hub
from montagne.common.utils import unicode_fmt
from montagne.common.openstack_object import NovaHypervisor
from novaclient.exceptions import NotFound as NovaResourceNotFound
from montagne.collector.collector import OpenStackCollector
from montagne.openstack_client.event import GetNovaClientRequest


def nova_api_handler(func):
    def wrapper(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except NovaResourceNotFound:
            return None
    return wrapper


class NovaCollector(OpenStackCollector):
    poll_instance_interval = 10

    def __init__(self):
        super(NovaCollector, self).__init__()
        self.nova = None
        self.hypervisors = {}

    def serve(self):
        self.thread(self._sync_hypervisor_instances_loop)

    def _sync_hypervisor_instances_loop(self):
        while True:
            timestamp = time.time()
            if self.nova:
                self.sync_hypervisor_instances()
                self.LOG.debug("get instance in hypervisor: %s",
                               self.hypervisors.keys())
            else:
                reply = self.send_request(GetNovaClientRequest(msg=None))
                self.nova = reply.msg
            hub.sleep(self.poll_instance_interval - (time.time() - timestamp))

    def sync_hypervisors(self):
        deprecate_hostnames = set(self.hypervisors)
        for hyperv in self._get_all_hypervisors():
            hostname = unicode_fmt(hyperv.hypervisor_hostname)
            deprecate_hostnames.discard(hostname)
            self.hypervisors[hostname] = NovaHypervisor(hyperv)

        for dh in deprecate_hostnames:
            self.hypervisors.pop(dh)

    def sync_hypervisor_instances(self):
        self.sync_hypervisors()

        for hostname, hypervisor in self.hypervisors.items():
            if hypervisor.running_vms <= 0:
                # ignore hypervisor without running instance
                continue
            hv = self._get_hypervisor_with_server(hostname)
            if not hv:
                # ignore hypervisor un-synchronized (hypervisor died after
                # function NovaCollector.sync_hypervisors() is called)
                continue
            for srv in hv[0].servers:
                hypervisor.servers = NovaHypervisor.Instances(srv)

    @nova_api_handler
    def _get_hypervisor(self, **kwargs):
        return self.nova.hypervisors.find(**kwargs)

    @nova_api_handler
    def _get_all_hypervisors(self, **kwargs):
        return self.nova.hypervisors.findall(**kwargs)

    @nova_api_handler
    def _get_hypervisor_by_hostname(self, hostname):
        return self.nova.hypervisors.find(hypervisor_hostname=hostname)

    @nova_api_handler
    def _get_hypervisor_by_id(self, hypervisor_id):
        return self.nova.hypervisors.get(hypervisor_id)

    @nova_api_handler
    def _get_hypervisor_with_server(self, hostname):
        return self.nova.hypervisors.search(hypervisor_match=hostname,
                                            servers=True)
