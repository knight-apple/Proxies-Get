import threading
import time
import datetime
import queue
from random import randint


class WaitQueue(threading.Thread):
    def __init__(self, countq):
        threading.Thread.__init__(self)
        self.q = countq

    def run(self):
        strsize = -1
        maxn = self.q.qsize() + 1
        cnt = 0
        sec = 0
        print()
        while not self.q.empty():
            n = self.q.qsize()
            if cnt > 3:
                sec = cnt // (maxn - n) * n
            s = "\r[Queue][%s]: %d data left, need about %5s" % (
                time.strftime("%H:%M:%S"),
                n,
                datetime.timedelta(seconds=sec),
            )
            if len(s) > strsize:
                strsize = len(s)
            while len(s) < strsize + 1:
                s += " "
            print(s, end="", flush=True)
            time.sleep(1)
            cnt += 1
        print("\n")
        print("[Queue]: Total use %s" % datetime.timedelta(seconds=cnt))


if __name__ == "__main__":
    tq = queue.Queue()
    for i in range(10):
        tq.put(0)
    w = WaitQueue(tq).start()
    while not tq.empty():
        tq.get()
        time.sleep(2)
    if w != None:
        w.join()
