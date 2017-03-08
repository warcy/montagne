from montagne.common.log import getLogger
from montagne.common import hub
from montagne.common.event import BaseEvent, BaseRequest, BaseReply


class MontagneApp(object):
    def __init__(self):
        super(MontagneApp, self).__init__()
        self.name = self.__module__
        self.LOG = getLogger(self.__class__.__name__)
        self.app_mgr = None
        self.event_handlers = {}
        self.threads = []
        self.events = hub.Queue(128)
        self._events_sem = hub.BoundedSemaphore(self.events.maxsize)

        self.thread(self._event_loop)

        self.is_active = True

    def thread(self, function, *args, **kwargs):
        """run function by greenthread.

        :param function:
        """
        self.threads.append(
            hub.spawn(function, *args, **kwargs))

    def delay_thread(self, delay, function, *args, **kwargs):
        """run function by greenthread with delay.

        :param delay:
        :param function:
        """
        self.threads.append(
            hub.spawn_after(delay, function, *args, **kwargs))

    def serve(self):
        """run loop functions when montagne start. """
        pass

    def close(self):
        # TODO:
        for th in self.threads:
            hub.kill(th)

    def send_event(self, event):
        assert isinstance(event, BaseEvent)
        event.src = self.name
        instance = self.app_mgr.find_app(event.dst)
        if instance is not None:
            self.LOG.debug('EVENT: %s (%s => %s)',
                           event.src, event.dst, event.__class__.__name__)
            instance._send_event(event)
        else:
            self.LOG.error('EVENT LOST: %s (%s => %s)',
                           event.src, event.dst, event.__class__.__name__)

    def send_request(self, request):
        assert isinstance(request, BaseRequest)
        request.reply_queue = hub.Queue()
        self.send_event(request)
        return request.reply_queue.get()

    def reply_to_request(self, request, reply):
        assert isinstance(request, BaseRequest)
        assert isinstance(reply, BaseReply)
        reply.dst = request.src
        reply.src = self.name
        request.reply_queue.put(reply)

    def _event_loop(self):
        while self.is_active or not self.events.empty():
            ev = self.events.get()
            self._events_sem.release()
            ev_handler = self.event_handlers.get(ev.__class__)

            try:
                ev_handler(ev)
            except hub.TaskExit:
                # Normal exit.
                # Propagate upwards, so we leave the event loop.
                raise
            except:
                self.LOG.exception(
                    '%s: Exception occurred during handler processing. '
                    'Backtrace from offending handler '
                    '[%s] servicing event [%s] follows.',
                    self.name, None, None)

    def _send_event(self, event):
        self._events_sem.acquire()
        self.events.put(event)
