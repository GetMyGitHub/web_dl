from subprocess import Popen

commands = [
    'date; df -h; sleep 3; date',
    'date; hostname; sleep 2; date',
    'date; uname -a; date',
]
# run in parallel
processes = [Popen("ping -c 2 google.com", shell=True)]
# do other things here..
print('nnljnjnjknkj')
# wait for completion
for p in processes: p.wait()
print ('hjbkbkbb')
