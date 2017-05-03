#!/usr/bin/env python

from montagne.common import hub

hub.patch(thread=False)

from montagne import cfg
import sys
from montagne import version
from montagne.common.log import getLogger
from montagne.common.app_manager import ApplicationManager
from montagne.common import credentials, log
from montagne.openstack_client.nova_client import NovaClient
from montagne.openstack_client.neutron_client import NeutronClient
from montagne.collector.neutron_collector import NeutronCollector
from montagne.collector.nova_collector import NovaCollector
from montagne.scheduler.scheduler import Scheduler
from montagne.notifier.neutron_notifier import NeutronNotifier
from montagne.listener.physical_network_listener import PhysicalNetworkListener
from montagne.common import wsgi  # register CONF cli

CONF = cfg.CONF


def main(args=None, prog=None):
    try:
        CONF(args=args, prog=prog,
             project='montagne', version='montagne-manager %s' % version,
             default_config_files=['/usr/local/etc/montagne/montagne.conf'])
    except cfg.ConfigFilesNotFoundError:
        CONF(args=args, prog=prog,
             project='montagne', version='montagne-manager %s' % version)

    log.init_log()
    LOG = getLogger()
    LOG.setLevel(CONF.log_level)
    # read OpenStack authentication from system environment value.
    # if failed, try to read from conf file.
    credentials.set_openstack_auth()

    LOG.info('Start Montage')
    hub.patch(thread=True)
    app_mgr = ApplicationManager()

    # applications to run
    app_list = [
        NeutronClient, NovaClient,
        NeutronCollector, NovaCollector,
        Scheduler,
        NeutronNotifier,
        PhysicalNetworkListener
    ]

    # initiating application and add to application manager
    for app in app_list:
        try:
            app_inst = app()
        except Exception as e:
            LOG.exception(e)
            app_mgr.close()
            sys.exit(0)
        app_mgr.register_app(app_inst)

    app_mgr.run()
    app_mgr.run_service()

    try:
        hub.joinall(app_mgr.service_thread)
    except KeyboardInterrupt:
        LOG.info("Keyboard Interrupt received. "
                 "Closing Montagne application manager...")
    finally:
        app_mgr.close()


if __name__ == '__main__':
    main()
