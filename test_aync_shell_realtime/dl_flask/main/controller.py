from flask import Blueprint
from flask import render_template



class controleur():

    def __init__(self, mode_debug):
        self._main = Blueprint('main', __name__)
        self.result = "start .."
        self.process = ""
        @self._main.route('/')
        def index():
            print('pass index')
            return render_template('index.html', result = self.result)
        @self._main.route('test_page/')
        def toto():
            print('pass toto')
            return render_template('page_test.html')

    @property
    def get_main(self):
        return self._main
