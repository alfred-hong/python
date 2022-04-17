import requests
# 在百度翻译中,英文输入法输入dog，网络抓取得到sug点击预览能观察到json数据
# 在表头旁边的载荷中能看到post方式的数据kw: dog

url = "https://fanyi.baidu.com/sug"

s = input("请输入你要翻译的英文单词")
dat = {
    "kw": s
}

# 发送post请求, 发送的数据必须放在字典中, 通过data参数进行传递
resp = requests.post(url, data=dat)
print(resp.json())  # 将服务器返回的内容直接处理成json()  => dict

resp.close()