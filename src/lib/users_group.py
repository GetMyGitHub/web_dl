from user import User
class Users_group():

    def __init__(self):
        self.name = ""
        self.users_dict = {}

    def set_group(self, name, users_dict):
        self.name = name
        self.users_dict = users_dict

    def add_user(self, user):
        self.users_dict[user.get_name] = user
