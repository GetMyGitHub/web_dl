from subprocess import Popen, PIPE


class process():

    def __init__(self):
        print('instanciate')

    def process_command(self, command):
        process = Popen(command, stdin=PIPE, stderr=PIPE, stdout=PIPE, shell=True)
        while True:
            line = process.stdout.readline().rstrip()
            if not line:
                break
            yield line

    def test(self):
        print('pass')
