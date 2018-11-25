
from sqlalchemy import Column, Integer, Text, String, DateTime, LargeBinary
from sqlalchemy.ext.declarative import declarative_base
from datetime import datetime

base = declarative_base()

class Tache(base):
    __tablename__ = 'taches'

    id = Column(Integer, primary_key=True)
    tache = Column(Text, unique=False)
    # execution = Column(Text, unique=False)
    execution = Column(LargeBinary, unique=False)
    date_debut = Column(DateTime, unique=False)
    date_fin = Column(DateTime, unique=False)

    def __init__(self, id, tache, execution=b"", date_fin=None, date_debut=datetime.now()):
        self.id = id
        self.tache = tache
        self.execution = execution
        self.date_debut = date_debut
        self.date_fin = date_fin

    def __repr__(self):
        return {'id':self.id, 'tache':self.tache, 'execution': self.execution}
