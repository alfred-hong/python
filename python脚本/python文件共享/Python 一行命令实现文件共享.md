# Python 一行命令实现文件共享

**HTTP服务**

这个功能从python2 就开始有了，python3以上自带这个功能。

```shell
# python2
python -m SimpleHTTPServer port_number

# python3
python -m http.server port_numbe

#`port_numbe`可以指定端口，如果不指定的话默认是8000。
```

然后在手机浏览器中打开即可访问。

但是访问目录是你当前执行文件的目录，因此需要写一个脚本。

```bat
@echo off
ipconfig /all
python -m http.server 80
```

```sh
#!/bin/bash
ifconfig | grep inet
python -m http.server 80
```

- 如果在浏览器输入的时候，不输入 :80 即端口号，也是可以的；
- 下载的时候，必须下载文件，建议先压缩，在借助浏览器下载；
- 如果手机端使用浏览器支持，可以在线播放mp4等文件，而且可以随意拖动进度条；
- ipad上的safari浏览器体验不佳；



**FTP服务**

```sh
pip install pyftpdlib (安装失败这里下载：https://pypi.python.org/pypi/pyftpdlib/)

python -m pyftpdlib

本机访问：ftp://127.0.0.1:2121

同一个局域网内访问ftp://<服务器IP>:2121
```

想展示哪个目录，直接在哪个目录下运行就好。



**ftp协议下载文件夹**

```sh
wget ftp://192.168.131.128/CODE --ftp-user=root --ftp-password=venwei -r
```

