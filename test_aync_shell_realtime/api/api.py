from api import config
from dl_flask import app as flask_app

class api():

    def __init__(self):
        self.mode_debug = config.mode_debug
        if(config.framework == 'flask'):
            self.flask_init()

    def flask_init(self):
        if(config.framework == 'flask'):
            self.app = flask_app.app(self.mode_debug)


    def run(self):
        self.app.run()
