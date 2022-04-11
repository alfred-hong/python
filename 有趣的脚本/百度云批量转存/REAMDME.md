1. 登陆百度云https://pan.baidu.com/disk/home，进入网页network复制出cookie粘贴到代码中

2. 将需要下载的文件保存到文本中

![图片](https://mmbiz.qpic.cn/mmbiz_png/SVEibGmlMicGeLrHppsMKySbibyFonZyfmW2kZ24HNOgmLZ1f6S5iczy5zmyZEg4KSL4Q1uu2mWj09sTU7bkhjnChw/640?wx_fmt=png&tp=webp&wxfrom=5&wx_lazy=1&wx_co=1)

3. 脚本使用方法

```
百度网盘文件批量转存 （如果检测到没有登录信息，会提示扫码登录）
optional arguments:  -h, --help            show this help message and exit  
-p PATH, --path PATH  必选，存有下载链接的文本文件路径                        
	1. 文本里面链接和密码不要在同一行                        
	2. 文本里面可以有多余的文字，目前支持一定程度的模糊匹配                        
	3. 链接所在的那一行，链接后面除了空格外不要有多余文字  
-s SAVE_FOLDER, --save_folder SAVE_FOLDER                       
	可选，在百度网盘中的存储路径，默认存储在根目录  
-c COOKIES, --cookies COOKIES                        
	可选，设置 Cookie  
-e {raise,ignore}, --errors {raise,ignore}                        
	可选，遇到错误的处理方式：                            
		raise: 报错然后停止程序，默认；                            
		ignore: 忽略而后进行下一个  
-H HEADER, --header HEADER                        
	可选，请求头
```

3. 使用脚本
```python
python 百度网盘转存.py  -p  download_links.txt  -s "/网盘路径（该路径需先创建，无-s参数默认为根目录）“
```



> 原文链接：https://mp.weixin.qq.com/s/hQAZ6ZxUqMOmo5j8Y97B2g