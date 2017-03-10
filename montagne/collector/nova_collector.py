import time
from montagne.common import hub
from montagne.common.utils import unicode_fmt
from montagne.common.openstack_object import NovaHypervisor
from montagne.collector.collector import OpenStackCollector
from montagne.openstack_client.event import GetNovaClientRequest
from montagne.collector import event as cl_ev


class NovaCollector(OpenStackCollector):
    poll_instance_interval = 60

    def __init__(self):
        super(NovaCollector, self).__init__()
        self.nova = None
        self.hypervisors = {}
        self.event_handlers = {
            cl_ev.GetHypervisorRequest: self.reply_hypervisor
        }
        hub.spawn(self._get_nova_client)

    def serve(self):
        self.thread(self._sync_hypervisor_instances_loop)

    def reply_hypervisor(self, req):
        hostname = req.msg
        hypervisor = self.hypervisors.get(hostname)
        rep = cl_ev.GetHypervisorReply(hypervisor)
        self.reply_to_request(req, rep)

    def _sync_hypervisor_instances_loop(self):
        while True:
            timestamp = time.time()
            if self.nova:
                self.sync_hypervisor_instances()
                self.LOG.debug("get instance in hypervisor: %s",
                               self.hypervisors.keys())
            hub.sleep(self.poll_instance_interval - (time.time() - timestamp))

    def sync_hypervisors(self):
        deprecate_hostnames = set(self.hypervisors)
        for hyperv in self.nova.get_all_hypervisors():
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
            hv = self.nova.get_hypervisor_with_server(hostname)
            if not hv:
                # ignore hypervisor un-synchronized (hypervisor died after
                # function NovaCollector.sync_hypervisors() is called)
                continue
            for srv in hv[0].servers:
                hypervisor.servers.setdefault(
                    unicode_fmt(srv['uuid']), NovaHypervisor.Instances(srv))

    def _get_nova_client(self):
        while True and (not self.nova):
            reply = self.send_request(GetNovaClientRequest(msg=None))
            self.nova = reply.msg
            hub.sleep(0.5)
        self.sync_hypervisor_instances()
