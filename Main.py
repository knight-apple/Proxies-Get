from ProxyGet import ProxyGet
from ProxyThread import TestThread


#####
## 设置
# 未验证的代理输出（以json格式保存）
get_file = "proxy.json"
# 验证后的代理输出（以json格式保存）
check_file = "useful_proxy.json"
# 多线程验证代理
# 由于每个代理需经过多次验证
# 线程数等于32时约 80条/min
thread_num = 32
# 使用代理抓取某网站代理池（需fq）
proxies = {"http": "http://localhost:8080", "https": "http://localhost:8080"}

#####

ProxyGet(get_file, proxies).run()

print()

# 使用 www.baidu.com 验证
# 可以通过修改 ProxyTest.py 验证修改验证方式
TestThread(get_file, check_file, thread_num).run()

