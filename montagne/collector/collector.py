import time
from montagne.common import hub
from montagne.common.application import MontagneApp
from montagne.common.utils import unicode_fmt
from montagne.common.credentials import (get_neutron_credentials,
                                         get_nova_v1_1_credentials)
from montagne.common.neutron_constants import (AGENT_TYPE_OVS,
                                               AGENT_TYPE_LOADBALANCER)
from montagne.common.openstack_object import OVSAgent, LBAgent, NovaHypervisor
from neutronclient.v2_0 import client as neutronclient
from novaclient.exceptions import NotFound as NovaResourceNotFound
from novaclient.v1_1 import client as novaclient


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


class NeutronCollector(OpenStackCollector):
    poll_agent_interval = 10

    def __init__(self):
        super(NeutronCollector, self).__init__()
        self._credentials = get_neutron_credentials()
        self.neutron = neutronclient.Client(**self._credentials)
        self._agents = None
        self.ovs_agents = {}
        self.lbaas_agents = {}

    def serve(self):
        self.thread(self._get_agents_loop)

    def _get_agents_loop(self):
        while True:
            timestamp = time.time()
            self.sync_agents()
            self.LOG.debug("get neutron agents, ovs-agent:%s, lbaas-agent:%s",
                           self.ovs_agents.keys(), self.lbaas_agents.keys())
            hub.sleep(
                self.poll_agent_interval - (time.time() - timestamp))

    def sync_agents(self):
        agents = self.neutron.list_agents()
        try:
            self._agents = unicode_fmt(agents)
        except:
            raise

        self._instance_agents()

    def _instance_agents(self):
        agents_list = self._agents['agents']

        for a in agents_list:
            if a['agent_type'] == AGENT_TYPE_OVS:
                na = OVSAgent(**a)
                self.ovs_agents[na.configuration.tunneling_ip] = na
            elif a['agent_type'] == AGENT_TYPE_LOADBALANCER:
                na = LBAgent(**a)
                self.lbaas_agents[na.id] = na
            else:
                pass


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
        self._credentials = get_nova_v1_1_credentials()
        self.nova = novaclient.Client(**self._credentials)
        self._hypervisors = self.nova.hypervisors
        self._servers = self.nova.servers
        self.hypervisors = {}

        # syncing hypervisor
        for hyperv in self._get_all_hypervisors():
            hostname = unicode_fmt(hyperv.hypervisor_hostname)
            if hostname in self.hypervisors:
                raise AssertionError(
                    'hypervisor hostname duplicate!!! '
                    'compute node with same hostname is not allowed. ')
            self.hypervisors[hostname] = NovaHypervisor(hyperv)

    def serve(self):
        self.thread(self._sync_hypervisor_instances_loop)

    def _sync_hypervisor_instances_loop(self):
        while True:
            timestamp = time.time()
            self.sync_hypervisor_instances()
            self.LOG.debug("get instance in hypervisor: %s",
                           self.hypervisors.keys())
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
        return self._hypervisors.find(**kwargs)

    @nova_api_handler
    def _get_all_hypervisors(self, **kwargs):
        return self._hypervisors.findall(**kwargs)

    @nova_api_handler
    def _get_hypervisor_by_hostname(self, hostname):
        return self._hypervisors.find(hypervisor_hostname=hostname)

    @nova_api_handler
    def _get_hypervisor_by_id(self, hypervisor_id):
        return self._hypervisors.get(hypervisor_id)

    @nova_api_handler
    def _get_hypervisor_with_server(self, hostname):
        return self._hypervisors.search(hypervisor_match=hostname,
                                        servers=True)
