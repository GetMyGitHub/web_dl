from user import User
from users_group import Users_group

from flask_babel import gettext

class Users_and_users_groups_manager():


    def __init__(self):
                self.users_dict = {}
                self.groups_dict = {}

    # user
    def add_user(self, name, password, su):
        try:
            user = User()
            user.set_user(name, password, su)
            self.users_dict[name] = user
            return (gettext('User %(name)s added successfully', name = name), user)
        except:
            return (gettext('Error encountered with adding user : %(name)s', name = name), None)


    def get_users(self):
        pass

    def get_user(self, name):
        try:
            return ("", self.users_dict[name])
        except KeyError:
            return (gettext('User %(name)s not found', name = name), None)

    def delete_user(self, name):
        pass

    # users_group
    def add_users_group(self, name):
        pass

    def get_users_groups(self):
        pass

    def get_users_group(self, name):
        pass

    def delete_users_group(self, name):
        pass

    def add_user_in_users_group(self, user_name, users_groups_name):
        pass
