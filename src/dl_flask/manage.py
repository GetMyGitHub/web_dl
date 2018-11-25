from flask import Flask, redirect, url_for, render_template, jsonify, session, request

# g for global var from Flask
from flask import g

from flask_babel import Babel, format_date, gettext

from dl_flask.models import bdd

from api.services.hash_source import hash

import os

# change this imports when they will works in bdd
# nodes ans groups manager in Ansible's files
from api.entities_not_in_bdd.managers.inventory import Inventory
# su group with user inself
from api.entities_not_in_bdd.managers.users_and_users_groups_manager import Users_and_users_groups_manager
# Temporary use Users_and_users_groups_manager for users/users groups rules
# Move it to framework directory
from api.entities_not_in_bdd.managers.permissions_manager import Permissions_manager

# services (don't change this)
from api.services.validator import Validator

class Manage():

    def __init__(self, conf, init):

        # import configuration_file from parametes
        self.host = conf['host']
        self.port = conf['port']
        self.debug_mode = conf['debug_mode']

        # use Flask as app and set app configuration :
        self.app = Flask(__name__)
        self.app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///models/sqlite_file/bdd.dl'
        self.app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True
        self.app.config['BABEL_DEFAULT_LOCALE'] = 'en'
        # self.app.config['SECRET_KEY'] = os.urandom(16)
        self.app.config['SECRET_KEY'] = 'test_key'

        # use Babel
        # see doc : https://pythonhosted.org/Flask-Babel/
        self.babel = Babel(self.app)

        # use SQLAlchemy
        # see doc : http://flask-sqlalchemy.pocoo.org/2.3/
        self.bdd = bdd.bdd(self.app)

        # use Flask session
        # see doc : https://pythonhosted.org/Flask-Session/

        # use managers :
        self.inventory_manager = Inventory(conf['ansible_dir_path'], conf['inventory_file_subpath'])
        # self.inventory_manager = Inventory()
        self.users_and_users_groups_manager = Users_and_users_groups_manager()
        self.manage_validator = Validator()
        self.permissions_manager = Permissions_manager(self.users_and_users_groups_manager, self.inventory_manager)

        # set global vars (lang):
        # use app_context -> see doc : http://flask.pocoo.org/docs/1.0/appcontext/ for details
        with self.app.app_context():
            g.lang = self.app.config['BABEL_DEFAULT_LOCALE']

        # print(self.users_and_users_groups_manager.add_user(
        #                                             conf['default_user'],
        #                                             conf['hash'],
        #                                             True
        #                                             ))
        #
        #
        # if init:
        #     self.users_and_users_groups_manager.add_user(
        #                                                 conf['default_user'],
        #                                                 conf['hash'],
        #                                                 True
        #                                                 )
        #
        #     self.users_and_users_groups_manager.add_users_group('group-1')
        #     self.users_and_users_groups_manager.add_user_in_users_group(
        #                                                                 conf['default_user'],
        #                                                                 'group-1'
        #                                                                 )
        #     self.inventory_manager.add_group('nodes-group-1')
        #
        #     self.permissions_manager.init_permission(
        #                                             'group-1',
        #                                             'nodes-group-1',
        #                                             {
        #                                                 'read': True,
        #                                                 'write':True,
        #                                                 'execute':True
        #                                             }
        #                                             )
        # if hash('DL_Lib_56270.') == conf['hash']:
        #     print('manage.py : line 93 : hash valid')

        print(self.users_and_users_groups_manager.add_user(
                                                    conf['default_user'],
                                                    conf['hash'],
                                                    True
                                                    ))
        # vars_dict ={"var1": "value1", "var2": "value2"}
        # self.inventory_manager.set_node_by_name_vars_dict(self, "node1", vars_dict)
        # print(self.users_and_users_groups_manager.get_user('admin'))
        #
        #



        # print(self.inventory_manager.add_node("node1"))
        # print(self.inventory_manager.add_node("node1"))
        # print(self.inventory_manager.add_node("node2"))
        # print(self.inventory_manager.add_node("node3"))
        # print(self.inventory_manager.add_group("group1"))
        # print(self.inventory_manager.add_group("group2"))
        # print(self.inventory_manager.add_group("group3"))
        #
        # print(self.inventory_manager.add_node("node5"))
        # print(self.inventory_manager.add_node("node6"))
        # print(self.inventory_manager.add_node("node7"))
        # print(self.inventory_manager.add_node("node8"))
        # print(self.inventory_manager.add_group("group5"))
        # print(self.inventory_manager.add_group("group6"))
        # print(self.inventory_manager.add_group("group7"))
        #
        #
        # print(self.inventory_manager.set_group_by_name_vars_dict("group2", {"var1": "value1", "var2": "value2"}))
        # print(self.inventory_manager.set_group_by_name_vars_dict("group1", {"var1": "value1", "var2": "value2"}))
        # print(self.inventory_manager.get_group_by_name_vars_dict("group2"))
        # print(self.inventory_manager.update_group_by_name_var("group2", "var1", "value1updated"))
        # print(self.inventory_manager.get_group_by_name_value("group2", "var1"))
        # print(self.inventory_manager.get_group_by_name_vars_dict("group2"))
        # print(self.inventory_manager.get_nodes_names_not_in_group_by_name("group2"))
        # print(self.inventory_manager.add_node_name_in_group_name("node2", "group2"))
        # print(self.inventory_manager.add_node_name_in_group_name("node", "group1"))
        # print(self.inventory_manager.get_nodes_not_in_group_by_name("group2"))
        # print(self.inventory_manager.get_nodes_names_not_in_group_by_name("group2"))
        # print(self.inventory_manager.get_nodes_names_in_group_by_name("group2"))
        # print(self.inventory_manager.get_nodes_names_not_in_group_by_name("group2"))




        # print(self.inventory_manager.remove_node_name_in_group_name("node2", "group2"))
        # print(self.inventory_manager.get_nodes_names_not_in_group_by_name("group2"))
        # print(self.inventory_manager.add_node_name_in_group_name("node2", "group2"))
        # print("")


        # use views :
        self.__define_views()

        # finally start the server
        self.__run_server()

        # override babel locale :
        # g.lang define with globals
        @self.babel.localeselector
        def get_locale():
            return g.lang

    def __run_server(self):
        self.app.run(host=self.host, port=self.port, debug=self.debug_mode)


    def __define_views(self):

        #home
        @self.app.route('/')
        def index():
            return render_template('index.html', results = ('', None))

        #connection
        @self.app.route('/connection/', methods=['POST'])
        def connection():
            assert request.method == 'POST'
            user = (request.form['username'], request.form['password'])
            results = self.manage_validator.is_valid_user(user,
                                            self.permissions_manager.connect,
                                            user,
                                            None,
                                            None)
            return render_template('index.html', results = results)


        #disconnect
        @self.app.route('/disconnect/', methods=['GET'])
        def disconnect():
            assert request.method == 'GET'
            try:
                session.pop('username')
                return render_template('index.html', results = ('', None))
            except:
                return render_template('index.html', results = ('', None))


        #tests
        @self.app.route('/tests/')
        def tests():
            return render_template('test.html')


        #nodes
        @self.app.route('/nodes/')
        def get_nodes():
            try:
                nodes_list_response = self.manage_validator.check_permission_and_run(
                        self.permissions_manager.get_node_names,
                        [session['username']],
                        self.inventory_manager.get_node_names,
                        None
                        )
            except:
                nodes_list_response = ('', [])

            message = ""
            nodes_list = sorted(nodes_list_response[1])
            vars_list = None

            return render_template('nodes.html',
                                    results=(message,
                                            nodes_list,
                                            vars_list,
                                            )
                                    )


            return render_template('nodes.html', results=('', None))

        @self.app.route('/nodes/add_node/', methods=['POST'])
        def add_node():

            assert request.method == 'POST'
            results = self.manage_validator.is_valid_node(
                        request.form['nodename'],
                        self.permissions_manager.add_node,
                        [session['username']],
                        self.inventory_manager.add_node,
                        request.form['nodename']
                        )

            nodes_list_response = self.manage_validator.check_permission_and_run(
                        self.permissions_manager.get_node_names,
                        [session['username']],
                        self.inventory_manager.get_node_names,
                        None
                        )

            message = ''
            nodes_list = sorted(nodes_list_response[1])
            vars_list = None

            return render_template('nodes.html',
                                    results=(message,
                                            nodes_list,
                                            vars_list,
                                            )
                                    )

        @self.app.route('/nodes/delete_node/')
        def delete_node():
            tuple_result = None
            return render_template('nodes.html', results=('', None))


        @self.app.route('/nodes/delete_var/')
        def delete_var():
            tuple_result = None
            return render_template('nodes.html', results=('', None))


        @self.app.route('/nodes/get_vars/')
        def get_node_vars():
            tuple_result = None
            return render_template('nodes.html', results=('', None))

        @self.app.route('/nodes/set_var/')
        def set_node_var():
            tuple_result = NoneNone
            return render_template('nodes.html', results=('', None))

        @self.app.route('/nodes/delete_var/')
        def delete_node_var():
            tuple_result = None
            return render_template('nodes.html', results=('', None))

        @self.app.route('/nodes/run_staging/')
        def run_staging():
            tuple_result = None
            return render_template('nodes.html', results=('', None))


        #nodes_groups
        @self.app.route('/nodes_groups/')
        def get_groups():

            try:
                groups_list_response = self.manage_validator.check_permission_and_run(
                        self.permissions_manager.get_group_names,
                        [session['username']],
                        self.inventory_manager.get_group_names,
                        None
                        )
            except:
                groups_list_response = ('', [])

            try:
                nodes_list_response = self.manage_validator.check_permission_and_run(
                        self.permissions_manager.get_node_names,
                        [session['username']],
                        self.inventory_manager.get_node_names,
                        None
                        )
            except:
                nodes_list_response = ('', [])

            try :
                nodes_list_in_group_response = self.manage_validator.check_permission_and_run(
                            self.permissions_manager.get_nodes_in_group_by_name,
                            [session['username']],
                            self.inventory_manager.get_nodes_names_in_group_by_name,
                            groups_list_response[1][0]
                            )
            except:
                nodes_list_in_group_response = ('', [])

            groups_list = sorted(groups_list_response[1])
            nodes_list = sorted(nodes_list_response[1])
            nodes_in_group_list = sorted(nodes_list_in_group_response[1])


            if groups_list_response is not "":
                message = groups_list_response[0]
            else:
                if nodes_list_response is not "":
                    message = nodes_list_response[0]
                else:
                    message = nodes_list_in_group_response[0]



            return render_template('nodes_groups.html',
                                    results=(message,
                                            groups_list,
                                            nodes_list,
                                            nodes_in_group_list
                                            )
                                    )


        @self.app.route('/nodes_groups/add_group/', methods=['POST'])
        def add_group():
            # self.inventory_manager.add_group(request.form['groupname'])

            assert request.method == 'POST'
            results = self.manage_validator.is_valid_name(
                        request.form['groupname'],
                        self.permissions_manager.add_group,
                        [session['username']],
                        self.inventory_manager.add_group,
                        request.form['groupname']
                        )

            groups_list_response = self.manage_validator.check_permission_and_run(
                        self.permissions_manager.get_group_names,
                        [session['username']],
                        self.inventory_manager.get_group_names,
                        None
                        )
            nodes_list_response = self.manage_validator.check_permission_and_run(
                        self.permissions_manager.get_node_names,
                        [session['username']],
                        self.inventory_manager.get_node_names,
                        None
                        )
            nodes_list_in_group_response = self.manage_validator.check_permission_and_run(
                        self.permissions_manager.get_nodes_in_group_by_name,
                        [session['username']],
                        self.inventory_manager.get_nodes_names_in_group_by_name,
                        groups_list_response[1][0]
                        )


            groups_list = sorted(groups_list_response[1])
            nodes_list = sorted(nodes_list_response[1])
            nodes_in_group_list = sorted(nodes_list_in_group_response[1])


            if results[0] is not "":
                message = results[0]
            else:
                if groups_list_response is not "":
                    message = groups_list_response[0]
                else:
                    if nodes_list_response is not "":
                        message = nodes_list_response[0]
                    else:
                        message = nodes_list_in_group_response[0]


            return render_template('nodes_groups.html',
                                    results=(message,
                                            groups_list,
                                            nodes_list,
                                            nodes_in_group_list
                                            )
                                    )


        @self.app.route('/nodes_groups/delete_group/')
        def delete_group():
            tuple_result = None
            return render_template('nodes_groups.html', results=('', None))


        @self.app.route('/nodes_groups/add_node/', methods=['POST'])
        def add_node_in_group():
            return 'dqdqzdqz'
            # return render_template('nodes_groups.html', results=('', None))


        @self.app.route('/nodes_groups/delete_node/')
        def delete_node_from_group():
            tuple_result = None
            return render_template('nodes_groups.html', results=('', None))


        @self.app.route('/nodes_groups/get_vars/')
        def get_groups_vars():
            tuple_result = None
            return render_template('nodes_groups.html', results=('', None))


        @self.app.route('/nodes_groups/set_var/')
        def set_group_var():
            tuple_result = None
            return render_template('nodes_groups.html', results=('', None))


        @self.app.route('/nodes_groups/delete_var/')
        def delete_group_var():
            tuple_result = None
            return render_template('nodes_groups.html', results=('', None))


        #users_manager
        @self.app.route('/users_manager/users/')
        def get_users():
            tuple_result = None
            return render_template('users.html', results=('', None))


        @self.app.route('/users_manager/users/add_user/')
        def add_user():
            tuple_result = None
            return render_template('users.html', results=('', None))


        @self.app.route('/users_manager/users/set_user/')
        def set_user():
            tuple_result = None
            return render_template('users.html', results=('', None))


        @self.app.route('/users_manager/users/delete_user/')
        def delete_user():
            tuple_result = None
            return render_template('users.html', results=('', None))


        @self.app.route('/users_manager/users_groups/')
        def get_users_groups():
            tuple_result = None
            return render_template('users_groups.html', results=('', None))


        @self.app.route('/users_manager/users_groups/set_user/')
        def set_user_in_users_group():
            tuple_result = None
            return render_template('users_groups.html', results=('', None))


        @self.app.route('/users_manager/users_groups/delete_user')
        def delete_user_from_users_group():
            tuple_result = None
            return render_template('users_groups.html', results=('', None))


        #playbook
        @self.app.route('/playbook/')
        def playbook():
            tuple_result = None
            return render_template('playbook.html', results=('', None))


        #permissions
        @self.app.route('/permissions/')
        def get_permissions():
            tuple_result = None
            return render_template('permissions.html', results=('', None))


        @self.app.route('/permissions/get_permission/')
        def get_permission():
            tuple_result = None
            return render_template('permissions.html', results=('', None))


        @self.app.route('/permissions/set_permission/')
        def set_permission():
            tuple_result = None
            return render_template('permissions.html', results=('', None))


        #task_list
        @self.app.route('/task_list/')
        def get_tasks():
            tuple_result = None
            return render_template('task_list.html', results=('', None))

        @self.app.route('/task_list/add_task/')
        def add_task():
            tuple_result = None
            return render_template('task_list.html', results=('', None))


        @self.app.route('/task_list/get_task/')
        def get_task():
            tuple_result = None
            return render_template('task_list.html', results=('', None))


        @self.app.route('/task_list/kill_task/')
        def kill_task():
            tuple_result = None
            return render_template('task_list.html', results=('', None))
