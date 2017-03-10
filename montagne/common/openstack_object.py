from montagne.common.utils import unicode_fmt


class OpenStackAgents(object):
    def __init__(self):
        pass


class NeutronAgents(OpenStackAgents):
    """
        OpenStack SDK list_agents example:

            {
              "binary": "neutron-openvswitch-agent",
              "description": null,
              "admin_state_up": true,
              "heartbeat_timestamp": "2017-03-06 09:03:23",
              "alive": true,
              "id": "070334ba-2b61-4cbb-9b48-21d3a9d8a1e3",
              "topic": "N/A",
              "host": "compute3",
              "agent_type": "Open vSwitch agent",
              "started_at": "2017-02-27 07:25:44",
              "created_at": "2016-08-23 08:26:17",
              "configurations": {
                "arp_responder_enabled": false,
                "tunneling_ip": "10.0.1.33",
                "devices": 6,
                "l2_population": true,
                "tunnel_types": [
                  "vxlan"
                ],
                "enable_distributed_routing": false,
                "bridge_mappings": {}
              }
            },

    """

    def __init__(self, **kwargs):
        super(NeutronAgents, self).__init__()
        self.binary = kwargs['binary']
        self.description = kwargs['description']
        self.admin_state_up = kwargs['admin_state_up']
        self.heartbeat_timestamp = kwargs['heartbeat_timestamp']
        self.alive = kwargs['alive']
        self.id = kwargs['id']
        self.topic = kwargs['topic']
        self.host = kwargs['host']
        self.agent_type = kwargs['agent_type']
        self.started_at = kwargs['started_at']
        self.created_at = kwargs['created_at']
        self.configuration = None


class OVSAgent(NeutronAgents):
    def __init__(self, **kwargs):
        super(OVSAgent, self).__init__(**kwargs)

        if 'tunneling_ip' in kwargs['configurations'] and \
           kwargs['configurations']['tunneling_ip'] != '':
            self.configuration = OVSAgent.TunnelConfiguration(
                **kwargs['configurations'])
        else:
            self.configuration = kwargs['configurations']

    class TunnelConfiguration(object):
        def __init__(self, **kwargs):
            self.arp_responder_enabled = kwargs['arp_responder_enabled']
            self.tunneling_ip = kwargs['tunneling_ip']
            self.devices = kwargs['devices']
            self.l2_population = kwargs['l2_population']
            self.tunnel_types = kwargs['tunnel_types']
            self.enable_distributed_routing = kwargs[
                'enable_distributed_routing']
            self.bridge_mappings = kwargs['bridge_mappings']


class LBAgent(NeutronAgents):
    def __init__(self, **kwargs):
        super(LBAgent, self).__init__(**kwargs)
        self.configuration = LBAgent.Configuration(
            **kwargs['configurations'])

    class Configuration(object):
        def __init__(self, **kwargs):
            self.device_drivers = kwargs['device_drivers']
            self.instances = kwargs['instances']


class NovaHypervisor(object):
    def __init__(self, hv):
        super(NovaHypervisor, self).__init__()
        self.cpu_info = unicode_fmt(eval(hv.cpu_info))
        self.current_workload = int(hv.current_workload)
        self.disk_available_least = int(hv.disk_available_least)
        self.free_disk_gb = int(hv.free_disk_gb)
        self.free_ram_mb = int(hv.free_ram_mb)
        self.host_ip = unicode_fmt(hv.host_ip)
        self.hypervisor_hostname = unicode_fmt(hv.hypervisor_hostname)
        self.hypervisor_type = unicode_fmt(hv.hypervisor_type)
        self.hypervisor_version = int(hv.hypervisor_version)
        self.id = int(hv.id)
        self.local_gb = int(hv.local_gb)
        self.local_gb_used = int(hv.local_gb_used)
        self.memory_mb = int(hv.memory_mb)
        self.memory_mb_used = int(hv.memory_mb_used)
        self.running_vms = int(hv.running_vms)
        self.service = unicode_fmt(hv.service)
        self.state = unicode_fmt(hv.state)
        self.status = unicode_fmt(hv.status)
        self.vcpus = int(hv.vcpus)
        self.vcpus_used = int(hv.vcpus_used)
        self.servers = {}

    class Instances(object):
        def __init__(self, srv):
            self.name = unicode_fmt(srv['name'])
            self.uuid = unicode_fmt(srv['uuid'])


class LBMember(object):
    def __init__(self, **kwargs):
        super(LBMember, self).__init__()
        self.address = kwargs['address']
        self.admin_state_up = kwargs['admin_state_up']
        self.id = kwargs['id']
        self.pool_id = kwargs['pool_id']
        self.protocol_port = kwargs['protocol_port']
        self.status = kwargs['status']
        self.status_description = kwargs['status_description']
        self.tenant_id = kwargs['tenant_id']
        self.weight = kwargs['weight']
