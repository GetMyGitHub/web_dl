from api import config
from dl_flask import web_app as flask_app

class api():

    def __init__(self):
        if(config.framework == 'flask'):
            self.flask_init()

    def flask_init(self):
        self.web_app = flask_app.web_app(config.host, config.port, config.mode_debug)

    # def run(self):
    #     pass
    #     # self.app.run(host='127.0.0.1', port=5000, debug=True)
    #     # self.web_app.run_server(config.host, config.port, config.mode_debug)
    #     self.web_app.run_server()
