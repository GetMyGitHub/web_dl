from flask import session

from api.services import hash_source

from flask_babel import gettext

class Permissions_manager():

    def __init__(self,user_manager, inventory):
        self.user_manager = user_manager
        self.inventory = inventory
        self.permission_dict = {}

    def set_permission(fx_permission_mgr_args):
        self.permission_dict[
                            (
                            fx_permission_mgr_args[0],
                            fx_permission_mgr_args[1]
                            )
                            ]:fx_permission_mgr_args[2]


    def connect(self, fx_permission_mgr_args):
        request = self.user_manager.get_user(fx_permission_mgr_args[0])
        if request[1] is not None:
            if request[1].get_password() == hash_source.hash(fx_permission_mgr_args[1]):
                session['username'] = request[1].get_name()
            else:
                return gettext('wrong password')
        return request[0]

    # nodes
    def get_node_names(self, fx_permission_mgr_args):
        return self.__is_su(fx_permission_mgr_args[0])

    def add_node(self, fx_permission_mgr_args):
        return self.__is_su(fx_permission_mgr_args[0])

    def delete_node(self, fx_permission_mgr_args):
        return self.__is_su(fx_permission_mgr_args[0])

    def get_vars_node(self, fx_permission_mgr_args):
        return self.__is_su(fx_permission_mgr_args[0])

    def set_var_node(self, fx_permission_mgr_args):
        return self.__is_su(fx_permission_mgr_args[0])

    def run_staging(self, fx_permission_mgr_args):
        return self.__is_su(fx_permission_mgr_args[0])

    # nodes_groups
    def get_nodes_groups(self, fx_permission_mgr_args):
        return self.__is_su(fx_permission_mgr_args[0])

    def set_nodes_group(self, fx_permission_mgr_args):
        return self.__is_su(fx_permission_mgr_args[0])

    def get_group_names(self, fx_permission_mgr_args):
        return self.__is_su(fx_permission_mgr_args[0])

    def add_group(self, fx_permission_mgr_args):
        return self.__is_su(fx_permission_mgr_args[0])

    def get_nodes_in_group_by_name(self, fx_permission_mgr_args):
        return self.__is_su(fx_permission_mgr_args[0])

    def delete_nodes_group(self, fx_permission_mgr_args):
        return self.__is_su(fx_permission_mgr_args[0])

    def add_node_name_in_group_name(self, fx_permission_mgr_args):
        return self.__is_su(fx_permission_mgr_args[0])

    def delete_node_from_nodes_group(self, fx_permission_mgr_args):
        return self.__is_su(fx_permission_mgr_args[0])

    def get_vars_nodes_group(self, fx_permission_mgr_args):
        return self.__is_su(fx_permission_mgr_args[0])

    def set_var_to_nodes_group(self, fx_permission_mgr_args):
        return self.__is_su(fx_permission_mgr_args[0])

    def delete_var_from_nodes_group(self, fx_permission_mgr_args):
        return self.__is_su(fx_permission_mgr_args[0])

    #users_manager
    def get_users(self, fx_permission_mgr_args):
        return self.__is_su(fx_permission_mgr_args[0])

    def add_user(self, fx_permission_mgr_args):
        return self.__is_su(fx_permission_mgr_args[0])

    def set_user(self, fx_permission_mgr_args):
        return self.__is_su(fx_permission_mgr_args[0])

    def delete_user(self, fx_permission_mgr_args):
        return self.__is_su(fx_permission_mgr_args[0])

    def set_auth(self, fx_permission_mgr_args):
        return self.__is_su(fx_permission_mgr_args[0])

    def playbookk(self, fx_permission_mgr_args):
        return self.__is_su(fx_permission_mgr_args[0])

    def get_tasks(self, fx_permission_mgr_args):
        return self.__is_su(fx_permission_mgr_args[0])

    def get_task(self, fx_permission_mgr_args):
        return self.__is_su(fx_permission_mgr_args[0])

    def kill_task(self, fx_permission_mgr_args):
        return self.__is_su(fx_permission_mgr_args[0])


    def __is_su(self, user):
        request = self.user_manager.get_user(user)
        if request[1] is not None:
            if request[1].get_su():
                return None
            else:
                return gettext('permission denied')
        else :
            return request[0]
