# 爬虫: 通过编写程序来获取到互联网上的资源
# 百度
# 需求: 用程序模拟浏览器. 输入一个网址. 从该网址中获取到资源或者内容
# python搞定以上需求. 特别简单
from urllib.request import urlopen

url = "http://www.baidu.com"
resp = urlopen(url)

with open("mybaidu.html", mode="w") as f:
    f.write(resp.read().decode("utf-8"))  # 读取到网页的页面源代码
print("over!")

resp.close()

# web请求过程剖析
# 1.服务器渲染: 在服务器那边直接把数据和html整合在一起. 统一返回给浏览器
#   在页面源代码中能看到数据
# 2.客户端渲染:
#   第一次请求只要一个html骨架. 第二次请求拿到数据. 进行数据展示.
#   在页面源代码中, 看不到数据

# 熟练使用浏览器抓包工具
