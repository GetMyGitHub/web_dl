from flask import Flask
from dl_flask.main.controller import controleur
from subprocess import Popen, PIPE
import threading
from dl_flask import bdd


class app():

    def __init__(self, mode_debug):
        self.mode_debug = mode_debug
        self.controleur = controleur(self.mode_debug)
        self.app = Flask(__name__)
        self.app.register_blueprint(self.controleur._main, url_prefix='/')
        self.app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///models/bdd.dl'

        self.bdd = bdd.bdd(self.app)

    def run(self):
        thread_app1 = threading.Thread(target=self.run_test2)
        thread_app1.start()
        self.app.run()


    def run_test1(self):
        print('initialisation subprocess ...')
        process = [Popen("ping -c 2 google.com", shell=True)]
        print('subprocess en route ...')
        for p in process:
            print('step')
            p.wait()
        print ('fin du subprocess')

    def run_test2(self):
        for path in self.process("ping -c 5 google.com"):
            print(path.decode("utf-8"))

    def process(self, command):
        process = Popen(command, stdout=PIPE, shell=True)
        while True:
            line = process.stdout.readline().rstrip()
            if not line:
                break
            yield line




"""
from subprocess import Popen, PIPE

def run(command):
    process = Popen(command, stdout=PIPE, shell=True)
    while True:
        line = process.stdout.readline().rstrip()
        if not line:
            break
        yield line


if __name__ == "__main__":
    for path in run("ping -c 5 google.com"):
        print path
"""
