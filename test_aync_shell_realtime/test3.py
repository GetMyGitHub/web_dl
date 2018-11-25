import threading
import time

def my_job():
	print(threading.current_thread().name)


t=threading.Thread(target=my_job)
t.start()

t1=threading.Thread(target=my_job)
t1.start()

t2=threading.Thread(target=my_job)
t2.start()
