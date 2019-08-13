import queue
import threading
import json
import time
from ProxyTest import proxy_test
from QueueCount import WaitQueue

InputFile = "proxy.json"
OutputFile = "useful_proxy.json"
ThreadNum = 8


class TestThread:
    exitFlag = 0
    inqueueLock = threading.Lock()
    inQueue = queue.Queue()
    outQueue = queue.Queue()
    threads = []

    class subThread(threading.Thread):
        def __init__(self, fa, threadID, qin, qout):
            threading.Thread.__init__(self)
            self.fa = fa
            self.threadID = threadID
            self.qin = qin
            self.qout = qout

        def run(self):
            print("[Sub Thread %d]: Start" % self.threadID)
            self.fa.operator_queue(self.qin, self.qout)
            print("[Sub Thread %d]: Exit" % self.threadID)

    def __init__(self, InputFile, OutputFile, ThreadNum):
        self.InputFile = InputFile
        self.OutputFile = OutputFile
        self.ThreadNum = ThreadNum

        # 加载文件
        print("[Main Thread]: Load file")
        load_list = []
        try:
            with open(self.InputFile, "r") as f:
                load_list = json.load(f)["proxy"]
        except BaseException as e:
            print(e)

        # 填充队列
        print("[Main Thread]: Fill input queue")
        for tmp in load_list:
            self.inQueue.put(tmp)
        print("[Main Thread]: Load %d datas" % self.inQueue.qsize())

    def operator_queue(self, qin, qout):
        while not self.exitFlag:
            self.inqueueLock.acquire()
            if not qin.empty():
                data = qin.get()
                self.inqueueLock.release()
                if proxy_test(data):
                    qout.put(data)
            else:
                self.inqueueLock.release()

    def run(self):
        # 创建新线程
        print("[Main Thread]: Create threads")
        for threadID in range(self.ThreadNum):
            thread = self.subThread(self, threadID, self.inQueue, self.outQueue)
            thread.start()
            self.threads.append(thread)

        # 等待队列清空
        print("[Main Thread]: Waiting for input queue")
        wait = WaitQueue(self.inQueue)
        wait.start()
        wait.join()

        self.exitFlag = 1
        for t in self.threads:
            t.join()

        out_data = []
        while not self.outQueue.empty():
            out_data.append(self.outQueue.get())
        print("[Main Thread]: Get %d useful proxies" % len(out_data))
        print("[Main Thread]: Write to file")
        # 输出
        with open(self.OutputFile, "w") as f:
            json.dump(
                {
                    "date": time.strftime("%Y-%m-%d %H:%M:%S"),
                    "size": len(out_data),
                    "proxy": out_data,
                },
                f,
            )


if __name__ == "__main__":
    TestThread(InputFile, OutputFile, ThreadNum).run()

