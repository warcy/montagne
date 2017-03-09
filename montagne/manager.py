#!/usr/bin/env python

from montagne.common import hub
hub.patch(thread=False)

from montagne import cfg

import logging
from montagne import version
from montagne.common.log import getLogger
from montagne.common.app_manager import ApplicationManager
from montagne.collector.collector import NeutronCollector, NovaCollector
from montagne.scheduler.scheduler import Scheduler
from montagne.notifier.notifier import TestNotifier
from montagne.listener.listener import TestListener
from montagne.common import wsgi

CONF = cfg.CONF

LOG = getLogger()
LOG.setLevel(logging.DEBUG)


def main(args=None, prog=None):
    try:
        CONF(args=args, prog=prog,
             project='montagne', version='montagne-manager %s' % version,
             default_config_files=['/usr/local/etc/montagne/montagne.conf'])
    except cfg.ConfigFilesNotFoundError:
        CONF(args=args, prog=prog,
             project='montagne', version='montagne-manager %s' % version)

    LOG.info('Start Montage')
    hub.patch(thread=True)
    app_mgr = ApplicationManager()

    # applications to run
    app_list = [
        NeutronCollector, NovaCollector,
        Scheduler, TestListener, TestNotifier
    ]

    # initiating application and add to application manager
    for app in app_list:
        app_mgr.register_app(app())

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
