class User():

    def __init__(self):
        self.name = ""
        self.password = ""
        self.su = False
        self.auths_dict = {
                            'read': False,
                            'write': False,
                            'execute':False,
                        }



    def set_user(self, name, password, su):
        self.name = name
        self.password = password
        self.su = su

    def get_name(self):
        return self.name

    def get_password(self):
        return self.password

    def get_auths_dict(self):
        return self.auths_dict

    def set_su(self, boolean):
        self.su = boolean

    def get_su(self):
        return self.su
