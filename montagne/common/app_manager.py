from montagne.common import hub
from montagne.common.wsgi import WSGIServer, WSGIApplication


class ApplicationManager(object):
    def __init__(self):
        self.apps = {}
        self.service_thread = []

    def run(self):
        for name, app in self.apps.items():
            app.serve()
            self.service_thread.extend(app.threads)

    def run_service(self):
        wsgi_services = {}
        for name, app in self.apps.items():
            if app.wsgi_controller is None:
                continue
            wsgi_services[app.wsgi_controller] = app

        if len(wsgi_services) == 0:
            return

        wsgi_app = WSGIApplication()
        for controller, app in wsgi_services.items():
            wsgi_app.register(controller, data={app.__class__.__name__: app})

        wsgi_srv = WSGIServer(wsgi_app)
        wsgi_thread = hub.spawn(wsgi_srv)
        self.service_thread.append(wsgi_thread)

    def close(self):
        # TODO:
        for name, app in self.apps.items():
            app.close()
        for th in self.service_thread:
            hub.kill(th)

    def register_app(self, app_instance):
        app_instance.app_mgr = self
        self.apps.setdefault(app_instance.name, app_instance)

    def find_app(self, app_name):
        return self.apps.get(app_name)
