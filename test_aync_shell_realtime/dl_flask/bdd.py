from flask_sqlalchemy import SQLAlchemy


class bdd():

    def __init__(self, app):
        print('instanciation')
        self.app = app
        self.db = SQLAlchemy(self.app)
