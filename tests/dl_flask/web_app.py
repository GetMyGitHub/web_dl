from flask import Flask, redirect, url_for
from flask import render_template
from flask import jsonify

import os
import threading

from dl_flask import bdd

# from subprocess import Popen, PIPE
import subprocess




class web_app():

    def __init__(self, host, port, mode_debug):
        self.host = host
        self.port = port
        self.mode_debug = mode_debug
        self.app = Flask(__name__)
        self.app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///models/bdd.dl'
        self.bdd = bdd.bdd(self.app)
        self.taches_ansible_execute = {}
        self.define_views()

        # Debug :
        self.num_tache = 1
        self.repertoire_ansible = '/home/christophe/ownCloud/christophe/exemple_ansible'
        self.tache_ansible = 'ansible-playbook -vvv -i ./inventaire.txt ./exemple.yml'

        # Run serveur
        self.run_server()


    def define_views(self):

        # Index
        @self.app.route('/')
        def index():
            return render_template('index.html')

        # Console
        @self.app.route('/console/')
        def accueil_console():
            return render_template('console.html')

        # Nouvelle tache
        @self.app.route('/console/nouvelle_tache/')
        def nouvelle_tache():
            id_nouvelle_tache = self.bdd.get_length_table_tache() + 1
            print(id_nouvelle_tache)
            self.bdd.c  reate_tache(id_nouvelle_tache, self.tache_ansible)
            thread_tache = threading.Thread(target=self.execution_ansible, args=(id_nouvelle_tache, self.tache_ansible,))
            thread_tache.start()
            tache_bdd = self.bdd.get_tache(id_nouvelle_tache)
            return jsonify({
                            'id':tache_bdd.id,
                            'tache':tache_bdd.tache,
                            'execution': tache_bdd.execution,
                            'date_debut': tache_bdd.date_debut,
                            'date_fin': tache_bdd.date_fin
                            })

        # Recupere le contenu de la tache
        @self.app.route('/console/lecture_tache/<int:numero_tache>/')
        def console(numero_tache):
            tache_bdd = self.bdd.get_tache(numero_tache)
            return jsonify({
                            'id':tache_bdd.id,
                            'tache':tache_bdd.tache,
                            'execution': tache_bdd.execution,
                            'date_debut': tache_bdd.date_debut,
                            'date_fin': tache_bdd.date_fin
                            })


        # Retourne 'True' si le processus est en cours
        @self.app.route('/console/tache_en_execution/<int:num_tache>')
        def tache_en_execution(num_tache):
            # return str(self.process_running)
            return jsonify(self.process_running)

        self.process_running = False
    # Lance le serveur Flask
    def run_server(self):
        self.mode_debug = True
        self.app.run(host=self.host, port=self.port, debug=self.mode_debug)


    # Execution de la tache ansible via thread
    # def execution_ansible(self, id_tache, tache_ansible):
    #     print('debut du thead')
    #     line_decode = ""
    #     final_line = b""
    #     for line in self.popen_env(tache_ansible):
    #         # line_decode += line.decode('utf-8')
    #         final_line += line
    #         # print(final_line)
    #         # self.bdd.update_tache(id_tache, line_decode)
    #         self.bdd.update_tache(id_tache, final_line)
    #     self.bdd.update_fin(id_tache)
    #     print('fin du thread')
    #
    # def popen_env(self, tache_ansible):
    #     env_pour_popen = os.environ
    #     env_pour_popen['ANSIBLE_FORCE_COLOR'] = 'true'
    #     process = Popen(tache_ansible, stdout=PIPE, shell=True, env=env_pour_popen, cwd=self.repertoire_ansible)
    #     while True:
    #         line = process.stdout.readline()
    #         if not line:
    #             break
    #         yield line

    def append_process_output_in_database(self, id_tache, content_to_add):
        content =  self.db.session.get_tache_sortie_execution(id_tache) + content_to_add
        self.bdd.update_tache(id_tache, content)

    def append_process_output_in_database_callback(self, content):
            self.append_process_output_in_database(content)

    def execution_ansible(self, id_tache, tache_ansible):
        env_pour_popen = os.environ
        env_pour_popen['ANSIBLE_FORCE_COLOR'] = 'true'
        env_pour_popen['ANSIBLE_STDOUT_CALLBACK'] = 'debug'

        #proc = subprocess.Popen(tache_ansible, shell=True, env=env_pour_popen, cwd=self.repertoire_ansible, stdin=None, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
        #final_line = b""
        #while proc.poll() is None or line in proc.stdout:
        #    print(proc.stdout.readline())
        #     print(proc.poll())
        #    final_line += proc.stdout.readline()
        #    self.bdd.update_tache(id_tache, final_line)
        #print("finished with return code : {}".format(proc.returncode))

        #final_line += proc.stdout.readline()
        #self.bdd.update_tache(id_tache, final_line)
        #self.bdd.update_fin(id_tache)

        #return_code = execute(tache_ansible, env_pour_popen, self.append_process_output_in_database_callback)
        #print("return_code = ", return_code)
        process = subprocess.Popen(tache_ansible, shell=True, env=env_pour_popen, cwd=self.repertoire_ansible, stdin=None, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
        content = b""
        while True:
            output = process.stdout.readline()
            if output == '' and process.poll() is not None:
                break
            if output:
                content += output
                self.bdd.update_tache(id_tache, content)
        rc = process.poll()
        print("return code: ", rc)
