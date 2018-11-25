# from dl_flask.services.process import process
from services.process import process

class shell():

    def __init__(self,bdd):
        self.process = process()
        self.bdd = bdd

    def process_test(self):
        print('start subprocess test')
        # self.controleur.set_process('start...')
        for line in self.process.process_command("ping -c 1 google.com"):
            line = line.decode("utf-8")
            print(line)
            self.bdd.add_line(line)
            # self.controleur.set_process(line)
        # self.controleur.set_process('...end')
        print('end subprocess')
