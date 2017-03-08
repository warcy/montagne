#!/usr/bin/env python

import logging
from montagne.common import hub
from montagne.common.log import getLogger
from montagne.common.app_manager import ApplicationManager
from montagne.collector.collector import NeutronCollector, NovaCollector
from montagne.scheduler.scheduler import Scheduler
from montagne.notifier.notifier import TestNotifier
from montagne.listener.listener import TestListener

LOG = getLogger()
LOG.setLevel(logging.DEBUG)


def main():
    LOG.info('Start Montage')
    app_mgr = ApplicationManager()

    # applications to run
    app_list = [
        # NeutronCollector, NovaCollector
        Scheduler, TestListener, TestNotifier
    ]

    # initiating application and add to application manager
    for app in app_list:
        app_mgr.register_app(app())

    try:
        hub.joinall(app_mgr.run())
    except KeyboardInterrupt:
        LOG.info("Keyboard Interrupt received. "
                 "Closing Montagne application manager...")
    finally:
        app_mgr.close()


if __name__ == '__main__':
    main()
