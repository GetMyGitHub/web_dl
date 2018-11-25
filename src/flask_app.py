from flask import Flask, redirect, url_for, render_template, jsonify, session, request
# g for global var from Flask
from flask import g
from flask_babel import Babel, format_date, gettext
import os
from datetime import datetime

import sys
sys.path.append('./lib')
sys.path.append('./models')
from tasks_manager import Task_manager
from inventory_manager import Inventory
from users_and_users_groups_manager import Users_and_users_groups_manager
from permissions_manager import Permissions_manager
from validator import Validator
from models import sqladb, Task


class Manage():

    def __init__(self, conf):

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

        sqladb.app = self.app
        sqladb.init_app(self.app)

        # ! only for tests:
        # sqladb.drop_all()
        # sqladb.create_all()

        # sqladb.session.commit()
        # sqladb.session.add(Task(1, 'user1', 1, "test_command1"))
        # sqladb.session.add(Task(2, 'user2', 2, "test_command2"))
        # #sqladb.session.add(Task(2, 'user3', 3, "test_command3"))
        # sqladb.session.commit()
        # print("sqladb.session.query(Task): ", sqladb.session.query(Task))
        # print("sqladb.session.query(Task).all()", sqladb.session.query(Task).all())
        # print("Task.query.all()", Task.query.all())
        #
        # for taskobject in Task.query.all():
        #     print(taskobject.command)



        # use Babel
        # see doc : https://pythonhosted.org/Flask-Babel/
        self.babel = Babel(self.app)

        # use SQLAlchemy
        # see doc : http://flask-sqlalchemy.pocoo.org/2.3/
        #self.bdd = Database(self.app)

        # use Flask session
        # see doc : https://pythonhosted.org/Flask-Session/

        # use managers :
        self.inventory_manager = Inventory(conf['ansible_dir_path'], conf['inventory_file_subpath'])
        self.users_and_users_groups_manager = Users_and_users_groups_manager()
        self.manage_validator = Validator()
        self.permissions_manager = Permissions_manager(self.users_and_users_groups_manager, self.inventory_manager)
        self.task_manager = Task_manager(sqladb)


        # set global vars (lang):
        # use app_context -> see doc : http://flask.pocoo.org/docs/1.0/appcontext/ for details
        with self.app.app_context():
            g.lang = self.app.config['BABEL_DEFAULT_LOCALE']

        print(self.users_and_users_groups_manager.add_user(
                                                    conf['default_user'],
                                                    conf['hash'],
                                                    True
                                                    ))

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
            results = self.manage_validator.is_valid_user(
                                            user,
                                            self.permissions_manager.connect,
                                            user,
                                            None,
                                            None)
            session['error_message'] = results[0]
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


        #session message error
        @self.app.route('/set_error_message/<string:message>', methods=['GET'])
        def error_message(message):
            session['error_message'] = message
            return ''


        #tests
        @self.app.route('/tests/', methods=['POST'])
        def tests():
            return render_template('test.html')


        #nodes
        @self.app.route('/nodes/')
        def get_nodes():
            message = ""
            nodes_list = None
            vars_in_node = None
            nodes_list_response = ['']
            vars_in_node_response = ['']

            try:
                nodes_list_response = self.manage_validator.check_permission_and_run(
                        self.permissions_manager.get_node_names,
                        session['username'],
                        self.inventory_manager.get_node_names,
                        [None]
                        )
                nodes_list = sorted(nodes_list_response[1])
            except:
                session['error_message'] = nodes_list_response[0]


            try:
                nodename = session['selected_node']
            except:
                try:
                    if nodes_list[0] is not None:
                        session['selected_node'] = nodes_list[0]
                except:
                    pass


            try:
                vars_in_node_response = self.manage_validator.check_permission_and_run(
                                self.permissions_manager.get_node_by_name_vars_dict,
                                session['username'],
                                self.inventory_manager.get_node_by_name_vars_dict,
                                [session['selected_node']]
                                )
                vars_in_node = vars_in_node_response[1]
            except:
                pass



            session['error_message'] = vars_in_node_response[0]
            if nodes_list_response[0] != '':
                session['error_message'] = nodes_list_response[0]

            return render_template('nodes.html',
                                    results=(message,
                                            nodes_list,
                                            vars_in_node,
                                            )
                                    )



        @self.app.route('/nodes/set_active_node/<string:nodename>', methods=['GET'])
        def set_active_node(nodename):
            session['selected_node'] = nodename
            return nodename


        @self.app.route('/nodes/add_node/', methods=['POST'])
        def add_node():
            message = ""
            nodes_list = None
            vars_in_node = None

            assert request.method == 'POST'
            results = self.manage_validator.is_valid_node(
                        request.form['nodename'],
                        self.permissions_manager.add_node,
                        session['username'],
                        self.inventory_manager.add_node,
                        [request.form['nodename']]
                        )

            try:
                nodes_list_response = self.manage_validator.check_permission_and_run(
                        self.permissions_manager.get_node_names,
                        session['username'],
                        self.inventory_manager.get_node_names,
                        [None]
                        )
                nodes_list = sorted(nodes_list_response[1])
            except:
                pass

            session['error_message'] = nodes_list_response[0]
            if results[0] != '':
                session['error_message'] = results[0]



            return render_template('nodes.html',
                                    results=(message,
                                            nodes_list,
                                            vars_in_node,
                                            )
                                    )

        @self.app.route('/nodes/delete_node/')
        def delete_node():

            results = self.manage_validator.check_permission_and_run(
                                self.permissions_manager.del_node_by_name_,
                                session['username'],
                                self.inventory_manager.del_node_by_name_,
                                [session['selected_node']]
                                )

            try:
                nodes_list_response = self.manage_validator.check_permission_and_run(
                        self.permissions_manager.get_node_names,
                        session['username'],
                        self.inventory_manager.get_node_names,
                        [None]
                        )
                nodes_list = sorted(nodes_list_response[1])
            except:
                pass


            try:
                if nodes_list[0] is not None:
                    session['selected_node'] = nodes_list[0]
            except:
                session.pop('selected_node')



            return results[0]


        @self.app.route('/nodes/get_vars/')
        def get_node_vars():
            tuple_result = None
            return render_template('nodes.html', results=('', None))

        @self.app.route('/nodes/set_var/', methods=['POST'])
        def set_node_var():
            message = ''
            nodes_list = None
            vars_list = None
            nodes_list_response = ['']
            vars_in_node_response = ['']

            assert request.method == 'POST'

            results = self.manage_validator.check_permission_and_run(
                                self.permissions_manager.update_node_by_name_var,
                                session['username'],
                                self.inventory_manager.update_node_by_name_var,
                                [
                                    session['selected_node'],
                                    request.form['varName'],
                                    request.form['varValue']
                                ])

            try:
                nodes_list_response = self.manage_validator.check_permission_and_run(
                        self.permissions_manager.get_node_names,
                        session['username'],
                        self.inventory_manager.get_node_names,
                        [None]
                        )
                nodes_list = sorted(nodes_list_response[1])
            except:
                pass

            try:
                nodename = session['selected_node']
            except:
                try:
                    if nodes_list[0] is not None:
                        session['selected_node'] = nodes_list[0]
                except:
                    pass

            try :
                vars_in_node_response = self.manage_validator.check_permission_and_run(
                            self.permissions_manager.get_node_by_name_vars_dict,
                            session['username'],
                            self.inventory_manager.get_node_by_name_vars_dict,
                            [session['selected_node']]
                            )
                vars_in_node = vars_in_node_response[1]
            except:
                pass


            session['error_message'] = vars_in_node_response[0]
            if nodes_list_response[0] != '':
                session['error_message'] = nodes_list_response[0]
            if results[0] != '':
                session['error_message'] = results[0]


            return render_template('nodes.html',
                                    results=(message,
                                            nodes_list,
                                            vars_in_node,
                                            )
                                    )

        @self.app.route('/nodes/delete_var/<string:var_name>', methods=['GET'])
        def delete_node_var(var_name):

            results = self.manage_validator.check_permission_and_run(
                                self.permissions_manager.del_node_by_name_var,
                                session['username'],
                                self.inventory_manager.del_node_by_name_var,
                                [session['selected_node'], var_name]
                                )
            return results[0]



        @self.app.route('/nodes/run_staging/')
        def run_staging():
            tuple_result = None
            return render_template('nodes.html', results=('', None))


        #nodes_groups
        @self.app.route('/nodes_groups/')
        def get_groups():

            message = ''
            groups_list = None
            nodes_not_in_group = None
            nodes_in_group = None
            vars_in_group = None
            groups_list_response = ['']
            nodes_not_in_group_response = ['']
            nodes_in_group_response = ['']
            vars_in_group_response = ['']

            try:
                groups_list_response = self.manage_validator.check_permission_and_run(
                        self.permissions_manager.get_group_names,
                        session['username'],
                        self.inventory_manager.get_group_names,
                        [None]
                        )
                groups_list = sorted(groups_list_response[1])
            except:
                pass


            try:
                groupname = session['selected_group']
            except:
                try:
                    if groups_list[0] is not None:
                        session['selected_group'] = groups_list[0]
                except:
                    pass


            try:
                nodes_not_in_group_response = self.manage_validator.check_permission_and_run(
                        self.permissions_manager.get_nodes_names_not_in_group_by_name,
                        session['username'],
                        self.inventory_manager.get_nodes_names_not_in_group_by_name,
                        [session['selected_group']]
                        )
                nodes_not_in_group = sorted(nodes_not_in_group_response[1])
            except:
                pass



            try :
                nodes_in_group_response = self.manage_validator.check_permission_and_run(
                            self.permissions_manager.get_nodes_names_in_group_by_name,
                            session['username'],
                            self.inventory_manager.get_nodes_names_in_group_by_name,
                            [session['selected_group']]
                            )
                nodes_in_group = sorted(nodes_in_group_response[1])
            except:
                pass

            try :
                vars_in_group_response = self.manage_validator.check_permission_and_run(
                            self.permissions_manager.get_group_by_name_vars_dict,
                            session['username'],
                            self.inventory_manager.get_group_by_name_vars_dict,
                            [session['selected_group']]
                            )
                vars_in_group = vars_in_group_response[1]
            except:
                pass

            session['error_message'] = vars_in_group_response[0]
            if nodes_in_group_response[0] != '':
                session['error_message'] = nodes_in_group_response[0]
            if nodes_not_in_group_response[0] != '':
                session['error_message'] = nodes_not_in_group_response[0]
            if groups_list_response[0] != '':
                session['error_message'] = groups_list_response[0]

            return render_template('nodes_groups.html',
                                    results=(message,
                                            groups_list,
                                            nodes_not_in_group,
                                            nodes_in_group,
                                            vars_in_group
                                            )
                                    )


        @self.app.route('/nodes_groups/set_active_group/<string:groupname>', methods=['GET'])
        def set_active_group(groupname):
            session['selected_group'] = groupname
            return groupname


        @self.app.route('/nodes_groups/add_group/', methods=['POST'])
        def add_group():

            message = ''
            groups_list = None
            nodes_not_in_group = None
            nodes_in_group = None
            vars_in_group = None
            groups_list_response = ['']
            nodes_not_in_group_response = ['']
            nodes_in_group_response = ['']
            vars_in_group_response = ['']


            assert request.method == 'POST'
            results = self.manage_validator.is_valid_name(
                        request.form['groupname'],
                        self.permissions_manager.add_group,
                        session['username'],
                        self.inventory_manager.add_group,
                        [request.form['groupname']]
                        )

            try:
                groups_list_response = self.manage_validator.check_permission_and_run(
                        self.permissions_manager.get_group_names,
                        session['username'],
                        self.inventory_manager.get_group_names,
                        [None]
                        )
                groups_list = sorted(groups_list_response[1])
            except:
                pass

            try:
                nodes_not_in_group_response = self.manage_validator.check_permission_and_run(
                        self.permissions_manager.get_nodes_names_not_in_group_by_name,
                        session['username'],
                        self.inventory_manager.get_nodes_names_not_in_group_by_name,
                        [session['selected_group']]
                        )
                nodes_not_in_group = sorted(nodes_not_in_group_response[1])
            except:
                pass

            try:
                groupname = session['selected_group']
            except:
                try:
                    if groups_list[0] is not None:
                        session['selected_group'] = groups_list[0]
                except:
                    pass

            try :
                nodes_in_group_response = self.manage_validator.check_permission_and_run(
                            self.permissions_manager.get_nodes_names_in_group_by_name,
                            session['username'],
                            self.inventory_manager.get_nodes_names_in_group_by_name,
                            [session['selected_group']]
                            )
                nodes_in_group = sorted(nodes_in_group_response[1])
            except:
                pass

            try :
                vars_in_group_response = self.manage_validator.check_permission_and_run(
                            self.permissions_manager.get_group_by_name_vars_dict,
                            session['username'],
                            self.inventory_manager.get_group_by_name_vars_dict,
                            [session['selected_group']]
                            )
                vars_in_group = sorted(vars_in_group_response[1])
            except:
                pass

            session['error_message'] = vars_in_group_response[0]
            if nodes_in_group_response[0] != '':
                session['error_message'] = nodes_in_group_response[0]
            if nodes_not_in_group_response[0] != '':
                session['error_message'] = nodes_not_in_group_response[0]
            if groups_list_response[0] != '':
                session['error_message'] = groups_list_response[0]
            if results[0] != '':
                session['error_message'] = results[0]

            return render_template('nodes_groups.html',
                                    results=(message,
                                            groups_list,
                                            nodes_not_in_group,
                                            nodes_in_group,
                                            vars_in_group
                                            )
                                    )



        @self.app.route('/nodes_groups/delete_group/')
        def delete_group():

            results = self.manage_validator.check_permission_and_run(
                                self.permissions_manager.del_group_by_name_,
                                session['username'],
                                self.inventory_manager.del_group_by_name_,
                                [session['selected_group']]
                                )

            try:
                groups_list_response = self.manage_validator.check_permission_and_run(
                        self.permissions_manager.get_group_names,
                        session['username'],
                        self.inventory_manager.get_group_names,
                        [None]
                        )
                groups_list = sorted(groups_list_response[1])
            except:
                pass


            try:
                if groups_list[0] is not None:
                    session['selected_group'] = groups_list[0]
            except:
                session.pop('selected_group')

            return results[0]


        @self.app.route('/nodes_groups/add_node/<string:nodename>/', methods=['GET'])
        def add_node_in_group(nodename):

            results = self.manage_validator.check_permission_and_run(
                                self.permissions_manager.add_node_name_in_group_name,
                                session['username'],
                                self.inventory_manager.add_node_name_in_group_name,
                                [nodename, session['selected_group']]
                                )
            return results[0]


        @self.app.route('/nodes_groups/delete_node/<string:nodename>', methods=['GET'])
        def delete_node_from_group(nodename):

            results = self.manage_validator.check_permission_and_run(
                                self.permissions_manager.remove_node_name_in_group_name,
                                session['username'],
                                self.inventory_manager.remove_node_name_in_group_name,
                                [nodename, session['selected_group']]
                                )
            return results[0]


        @self.app.route('/nodes_groups/set_var/', methods=['POST'])
        def set_group_var():

            message = ''
            groups_list = None
            nodes_not_in_group = None
            nodes_in_group = None
            vars_in_group = None
            groups_list_response = ['']
            nodes_not_in_group_response = ['']
            nodes_in_group_response = ['']
            vars_in_group_response = ['']


            assert request.method == 'POST'

            results = self.manage_validator.check_permission_and_run(
                                self.permissions_manager.update_group_by_name_var,
                                session['username'],
                                self.inventory_manager.update_group_by_name_var,
                                [
                                    session['selected_group'],
                                    request.form['varName'],
                                    request.form['varValue']
                                ])

            try:
                groups_list_response = self.manage_validator.check_permission_and_run(
                        self.permissions_manager.get_group_names,
                        session['username'],
                        self.inventory_manager.get_group_names,
                        [None]
                        )
                groups_list = sorted(groups_list_response[1])
            except:
                pass

            try:
                nodes_not_in_group_response = self.manage_validator.check_permission_and_run(
                        self.permissions_manager.get_nodes_names_not_in_group_by_name,
                        session['username'],
                        self.inventory_manager.get_nodes_names_not_in_group_by_name,
                        [session['selected_group']]
                        )
                nodes_not_in_group = sorted(nodes_not_in_group_response[1])
            except:
                pass

            try:
                groupname = session['selected_group']
            except:
                try:
                    if groups_list[0] is not None:
                        session['selected_group'] = groups_list[0]
                except:
                    pass

            try :
                nodes_in_group_response = self.manage_validator.check_permission_and_run(
                            self.permissions_manager.get_nodes_names_in_group_by_name,
                            session['username'],
                            self.inventory_manager.get_nodes_names_in_group_by_name,
                            [session['selected_group']]
                            )
                nodes_in_group = sorted(nodes_in_group_response[1])
            except:
                pass

            try :
                vars_in_group_response = self.manage_validator.check_permission_and_run(
                            self.permissions_manager.get_group_by_name_vars_dict,
                            session['username'],
                            self.inventory_manager.get_group_by_name_vars_dict,
                            [session['selected_group']]
                            )
                vars_in_group = vars_in_group_response[1]
            except:
                pass

            session['error_message'] = vars_in_group_response[0]
            if nodes_in_group_response[0] != '':
                session['error_message'] = nodes_in_group_response[0]
            if nodes_not_in_group_response[0] != '':
                session['error_message'] = nodes_not_in_group_response[0]
            if groups_list_response[0] != '':
                session['error_message'] = groups_list_response[0]
            if results[0] != '':
                session['error_message'] = results[0]

            return render_template('nodes_groups.html',
                                    results=(message,
                                            groups_list,
                                            nodes_not_in_group,
                                            nodes_in_group,
                                            vars_in_group
                                            )
                                    )


        @self.app.route('/nodes_groups/delete_var/<string:var_name>', methods=['GET'])
        def delete_group_var(var_name):

            results = self.manage_validator.check_permission_and_run(
                                self.permissions_manager.del_group_by_name_var,
                                session['username'],
                                self.inventory_manager.del_group_by_name_var,
                                [session['selected_group'], var_name]
                                )
            return results[0]


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
            message = ''
            groups_list = None
            nodes_in_group = None
            playbooks_list = None
            groups_list_response = ['']
            nodes_in_group_response =['']
            plybooks_list_response = ['']

            try:
                groups_list_response = self.manage_validator.check_permission_and_run(
                        self.permissions_manager.get_group_names,
                        session['username'],
                        self.inventory_manager.get_group_names,
                        [None]
                        )
                groups_list = sorted(groups_list_response[1])
            except:
                pass

            try :
                nodes_in_group_response = self.manage_validator.check_permission_and_run(
                            self.permissions_manager.get_nodes_names_in_group_by_name,
                            session['username'],
                            self.inventory_manager.get_nodes_names_in_group_by_name,
                            [session['selected_group']]
                            )
                nodes_in_group = sorted(nodes_in_group_response[1])
            except:
                pass




            return render_template('playbook.html',
                                                    results=(message,
                                                    groups_list,
                                                    nodes_in_group,
                                                    playbooks_list
                                                    )
                                    )


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
