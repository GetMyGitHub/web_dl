from api.entities_not_in_bdd.managers import permissions_manager

from flask_babel import gettext

import re

class Validator:

    def __init__(self):
        pass

    def is_valid_node(self,hostname, fx_permission_mgr, fx_permission_mgr_args, fx_operation, fx_operation_args):
        normalise_host = hostname.encode("idna").decode().split(":")[0]
        if not self.__is_valid_hostname(normalise_host):
            return("incorrect Value", None)
        else:
            return self.check_permission_and_run(fx_permission_mgr, fx_permission_mgr_args, fx_operation, fx_operation_args)


    def is_valid_user(self, user, fx_permission_mgr, fx_permission_mgr_args, fx_operation, fx_operation_args):
        regexp = "^[a-z0-9-]+$"
        if not re.match(regexp, user[0]):
            return("incorrect name value", None)
        else:
            regexp = "^[A-Za-z0-9-_.]+$"
            if not re.match(regexp, user[1]):
                return("incorrect password value", None)
            else:
                return self.check_permission_and_run(fx_permission_mgr, fx_permission_mgr_args, fx_operation, fx_operation_args)


    def is_valid_name(self,name, fx_permission_mgr, fx_permission_mgr_args, fx_operation, fx_operation_args):
        regexp = "^[a-z0-9-]+$"
        if not re.match(regexp, name):
            return("incorrect name value", None)
        else:
            return self.check_permission_and_run(fx_permission_mgr, fx_permission_mgr_args, fx_operation, fx_operation_args)


    def check_permission_and_run(self, fx_permission_mgr, fx_permission_mgr_args, fx_operation, fx_operation_args):
        result = fx_permission_mgr(tuple(fx_permission_mgr_args))
        if result is not None:
            return(result, None)
        else:
            if fx_operation is not None:
                if fx_operation_args is not None:
                    return(fx_operation(fx_operation_args))
                else:
                    return(fx_operation())
            return('', None)

    def __is_valid_hostname(self, hostname):
        if len(hostname) > 255:
            return False
        hostname = hostname.rstrip(".")
        allowed = re.compile("(?!-)[A-Z\d\-\_]{1,63}(?<!-)$", re.IGNORECASE)
        return all(allowed.match(x) for x in hostname.split("."))

    # convert your unicode hostname to punycode (python 3 )
    # Remove the port number from hostname
