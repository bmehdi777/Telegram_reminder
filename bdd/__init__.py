from bdd import db
import os
actualDir = os.path.dirname(os.path.realpath(__file__))
database = db.Database(actualDir+"/bdd.db")