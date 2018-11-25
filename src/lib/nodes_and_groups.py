import pathlib
import yaml
from yaml_file_syncer import YamlFileSyncer

class NodeOrGroup():
    """
    Generic element object that will be inherited in node and group objects
    """

    def __init__(self, name, config_file_path):
        self.vars_dict = {}
        self.name = name
        self.__conf_file = None
        self.init_error_return = ""

        # Read the config file
        self.__conf_file = YamlFileSyncer(config_file_path)
        if self.__conf_file.init_error_return != "":
            self.init_error_return = self.__conf_file.init_error_return
        self.read()

    def read(self):
         (error_text, data) = self.__conf_file.read()
         if error_text != "" : return(error_text, None)
         if data == "" or data == None:
             self.vars_dict = {}
         else:
             self.vars_dict = data
         print("Loaded entity", self.name, "with vars: ", self.vars_dict)
         return("", None)


    def write(self):
        (error_text, nothing) = self.__conf_file.write(self.vars_dict)
        if error_text != "" : return(error_text, None)
        return("", None)



class Group(NodeOrGroup):

    def __init__(self, ansible_path, group_name):
        NodeOrGroup.__init__(self, group_name, ansible_path + "/groups_vars/" + group_name)
        self.nodes_list = []

    def add_node(self, node):
        if node not in self.nodes_list:
            self.nodes_list.append(node)

    def remove_node(self, node):
        if node in self.nodes_list:
            self.nodes_list.remove(node)

    def get_nodes_names_list(self):
        nodes_names_list = []
        for node in self.nodes_list:
            nodes_names_list.append(node.name)
        return(nodes_names_list)


class Node(NodeOrGroup):
    def __init__(self, ansible_path, node_name):
        NodeOrGroup.__init__(self, node_name, ansible_path + "/hosts_vars/" + node_name)



if __name__ == "__main__":
    group1 = Group("./", "groupe1")
    group1.vars_dict = {'var1': 'val1', 'var2': 'val2'}
    group1.write()
    node1 = Node("./", "node1")
    node2 = Node("./", "node2")
    node1.vars_dict = {'var1': 'val1', 'var2': 'val2'}
    node2.vars_dict = {'var1': 'val1', 'var2': 'val2'}
    node1.write()
    node2.write()
    node1.vars_dict = {}
    node1.read()
    print(node1.vars_dict)
