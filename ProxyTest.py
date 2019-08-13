import requests

TestUrl = "https://www.baidu.com/"
Timeout = 50


def proxy_test(test_proxy):
    for i in range(3):
        try:
            response = requests.get(TestUrl, proxies=test_proxy, timeout=Timeout)
            web = response.text.encode(response.encoding).decode("utf-8")
            if response.status_code == 200 and "<!--STATUS OK-->" in web:
                return True
            else:
                pass
        except BaseException:
            # print(e)
            pass
    return False


if __name__ == "__main__":
    test_proxies = {"http": "http://localhost:8080", "https": "http://localhost:8080"}
    print(proxy_test(test_proxies))
