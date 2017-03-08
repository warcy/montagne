# Copyright (C) 2013 Nippon Telegraph and Telephone Corporation.
# Copyright (C) 2013 YAMAMOTO Takashi <yamamoto at valinux co jp>
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#    http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or
# implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#
# modified from ryu.lib.hub

import os
from montagne.common.log import getLogger

import eventlet
import eventlet.event
import eventlet.queue
import eventlet.semaphore
import eventlet.timeout
import eventlet.wsgi
from eventlet import websocket
import greenlet
import socket
import traceback

LOG = getLogger(__name__)


getcurrent = eventlet.getcurrent
patch = eventlet.monkey_patch
sleep = eventlet.sleep
listen = eventlet.listen
connect = eventlet.connect


def spawn(*args, **kwargs):
    raise_error = kwargs.pop('raise_error', False)

    def _launch(func, *args, **kwargs):
        # Mimic gevent's default raise_error=False behaviour
        # by not propagating an exception to the joiner.
        try:
            return func(*args, **kwargs)
        except TaskExit:
            pass
        except BaseException as e:
            if raise_error:
                raise e
            # Log uncaught exception.
            # Note: this is an intentional divergence from gevent
            # behaviour; gevent silently ignores such exceptions.
            LOG.error('hub: uncaught exception: %s',
                      traceback.format_exc())

    return eventlet.spawn(_launch, *args, **kwargs)


def spawn_after(seconds, *args, **kwargs):
    raise_error = kwargs.pop('raise_error', False)

    def _launch(func, *args, **kwargs):
        # Mimic gevent's default raise_error=False behaviour
        # by not propagating an exception to the joiner.
        try:
            return func(*args, **kwargs)
        except TaskExit:
            pass
        except BaseException as e:
            if raise_error:
                raise e
            # Log uncaught exception.
            # Note: this is an intentional divergence from gevent
            # behaviour; gevent silently ignores such exceptions.
            LOG.error('hub: uncaught exception: %s',
                      traceback.format_exc())

    return eventlet.spawn_after(seconds, _launch, *args, **kwargs)


def kill(thread):
    thread.kill()


def joinall(threads):
    for t in threads:
        # This try-except is necessary when killing an inactive
        # greenthread.
        try:
            t.wait()
        except TaskExit:
            pass

Queue = eventlet.queue.LightQueue
QueueEmpty = eventlet.queue.Empty
Semaphore = eventlet.semaphore.Semaphore
BoundedSemaphore = eventlet.semaphore.BoundedSemaphore
TaskExit = greenlet.GreenletExit


class StreamServer(object):
    def __init__(self, listen_info, handle=None):
        if ':' in listen_info[0]:
            self.server = eventlet.listen(listen_info,
                                          family=socket.AF_INET6)
        else:
            self.server = eventlet.listen(listen_info)

        self.handle = handle

    def serve_forever(self):
        while True:
            sock, addr = self.server.accept()
            spawn(self.handle, sock, addr)


class LoggingWrapper(object):
    def write(self, message):
        LOG.info(message.rstrip('\n'))


class WSGIServer(StreamServer):
    def serve_forever(self):
        self.logger = LoggingWrapper()
        eventlet.wsgi.server(self.server, self.handle, self.logger,
                             log_output=True,
                             debug=False)

WebSocketWSGI = websocket.WebSocketWSGI

Timeout = eventlet.timeout.Timeout
