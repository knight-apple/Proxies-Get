import requests
from bs4 import BeautifulSoup
import json
import time
import datetime


class ProxyGet:
    proxies = {"http": "http://localhost:8080", "https": "http://localhost:8080"}

    def __init__(self, OutFile, proxies=None):
        self.OutFile = OutFile
        self.url = "https://www.youneed.win/proxy"
        if proxies != None:
            self.proxies = proxies

    # 下载网页
    def get_one_url(self, url):
        try:
            response = requests.get(url, verify=False, proxies=self.proxies, timeout=50)
            if response.status_code == 200:
                return response.text.encode(response.encoding).decode("utf-8")
            else:
                return None
        except BaseException:
            # print(e)
            return None

    # 解析目录网页
    def analyze(self, html):
        bs = BeautifulSoup(html, features="html.parser")
        tag = bs.find_all("table")[0]
        # print(tag)
        re = []
        if tag == None:
            return
        for i in tag.find_all("tr")[1:]:
            # print(i)
            tmp = i.find_all("td")
            dirt = {
                tmp[2].string: tmp[2].string
                + "://"
                + tmp[0].string
                + ":"
                + tmp[1].string
            }
            # print(dirt)
            re.append(dirt)
        return re

    def run(self):
        print("[Proxy Get]: Get web page")
        html = self.get_one_url(self.url)
        cnt = 0
        while html == None and cnt <= 5:
            print("[Proxy Get]: Get page error, try again now")
            html = self.get_one_url(self.url)
            cnt += 1

        # print(html[:5000])
        if html == None:
            print("[Proxy Get]: Can't get web page")
            exit(0)

        print("[Proxy Get]: Analyze page")
        proxy_list = self.analyze(html)
        print("[Proxy Get]: Get %d datas" % len(proxy_list))

        print("[Proxy Get]: Write to File")
        with open(self.OutFile, "w") as f:
            json.dump(
                {
                    "date": time.strftime("%Y-%m-%d %H:%M:%S"),
                    "size": len(proxy_list),
                    "proxy": proxy_list,
                },
                f,
            )


if __name__ == "__main__":
    ProxyGet("proxy.json").run()
