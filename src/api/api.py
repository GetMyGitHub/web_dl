import yaml
from api import config
from dl_flask import manage as flask_app
from api.services import yaml_file_syncer
from api.services import hash_source


class Api():

    def __init__(self):
        conf_file = "./api/config/config.yml"
        syncer = yaml_file_syncer.YamlFileSyncer(conf_file)
        conf = syncer.read()
        if conf[1] is None:
            print('Fichier vide ou erreur : ({})'.format(conf[0]))
        else :
            try:
                if conf[1]['password'] != '':
                    conf[1]['hash'] = hash_source.hash(conf[1]['password'])
                    conf[1]['password'] = ''
                    # Uncomment this
                    syncer.write(conf[1])
                    flask_app.Manage(conf[1], init=True)
                else:
                    flask_app.Manage(conf[1], init=False)
            except OSError as err:
                print("Erreur: {0}".format(err))
