from montagne.common import hub


class ApplicationManager(object):
    def __init__(self):
        self.apps = {}
        self.service_thread = []

    def run(self):
        for name, app in self.apps.items():
            app.serve()
            self.service_thread.extend(app.threads)
        return self.service_thread

    def close(self):
        # TODO:
        for th in self.service_thread:
            hub.kill(th)

    def register_app(self, app_instance):
        app_instance.app_mgr = self
        self.apps.setdefault(app_instance.name, app_instance)

    def find_app(self, app_name):
        return self.apps.get(app_name)
