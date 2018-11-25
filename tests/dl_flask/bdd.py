from flask_sqlalchemy import SQLAlchemy
from dl_flask.models.models import base, Tache
from datetime import datetime

class bdd():

    def __init__(self, app):
        self.app = app
        self.db = SQLAlchemy(self.app)
        self.base = base

        # ! only for tests:
        self.base.metadata.drop_all(bind=self.db.engine)
        #
        self.base.metadata.create_all(bind=self.db.engine)


    def update_tache(self, id, line):
        tache_id = self.db.session.query(Tache).get(id)
        tache_id.execution = line
        self.db.session.commit()

    def update_fin(self, id):
        tache_id = self.db.session.query(Tache).get(id)
        tache_id.date_fin = datetime.now()
        self.db.session.commit()

    def get_tache(self, id):
        return self.db.session.query(Tache).get(id)

    def get_tache_sortie_execution(self, id):
        return self.db.session.query(Tache).get(id).execution


    def create_tache(self, id, tache):
        self.db.session.add(Tache(id, tache))
        self.db.session.commit()

    def get_length_table_tache(self):
        return self.db.session.query(Tache).count()
