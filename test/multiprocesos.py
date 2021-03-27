import multiprocessing
import time

def worker3(num):
    """thread worker function"""
    while True:
        print('Worker:', num)
        time.sleep(3)

def worker2(num):
    """thread worker function"""
    while True:
        print('Worker:', num)
        time.sleep(3)
        multiprocessing.Process(target=worker2, args=("c",)).start()

def worker(num):
    """thread worker function"""
    while True:
        print('Worker:', num)
        time.sleep(3)
        multiprocessing.Process(target=worker2, args=("b",)).start()

if __name__ == '__main__':
    jobs = []
    for i in range(10):
        p = multiprocessing.Process(target=worker, args=("a",))
        jobs.append(p)

    for proc in jobs:
        proc.start()
        print("proceso iniciado")
