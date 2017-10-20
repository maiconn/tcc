import threading
import time
from random import randint


lock = threading.Lock()

def func(thread):
    global lock
    while True:
        with lock:
            print("=====inicio func=====")
            print("THREAD: "+thread)
            time.sleep(randint(0,5))
            
            print("THREAD: "+thread)
            time.sleep(randint(0,5))
            
            print("THREAD: "+thread)
            time.sleep(randint(0,5))
            print("=======fim func======")
            

if __name__ == "__main__":
    t1 = threading.Thread(target=func, args=['t1'])
    t1.start()

    t2 = threading.Thread(target=func, args=['t2'])
    t2.start()

