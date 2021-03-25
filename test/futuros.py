import time


import multiprocessing
print("Number of cpu : ", multiprocessing.cpu_count())


from multiprocessing import Process


def proceso(fruta):
    while True:
        print("hola ", fruta)
        time.sleep(2)

def proceso2(fruta):
    while True:
        print("hola ", fruta)
        time.sleep(1)


def main():
    proc = Process(target=proceso, args=("guayaba",))
    proc.start()

    proc = Process(target=proceso2, args=("lulo",))
    proc.start()

    print("procesos iniciados")

    print(proc.join())


if __name__ == '__main__':
    main()