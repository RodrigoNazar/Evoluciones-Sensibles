
import threading as th
import time


class Flag:
    def __init__(self, status=True, data=[]):
        self.status = status
        self.data = data

    def toggle(self):
        self.status = not self.status


def counter(flag):

    while 1:
        if len(flag.data) == 10:
            print('Lista llena')

            flag.data = []

        time.sleep(TIME)


def appender(flag):

    while 1:
        flag.data.append(1)

        print(f'Appendeando, con largo {len(flag.data)}')

        time.sleep(TIME)


TIME = .5
flag = Flag()


counter_thr = th.Thread(target=counter, args=[flag])
appender_thr = th.Thread(target=appender, args=[flag])

counter_thr.start()
appender_thr.start()
