Please run
```sh
$ source /opt/anaconda/bin/activate root
$ source /opt/anaconda/bin/deactivate root
```
to activate and deactivate the anaconda enviroment.

```sh
编辑 vim /etc/profile

#Anacondaexport 
PATH=$PATH:/opt/anaconda/bin

source /etc/profile

输入conda命令确认
```

有时候可能由于你安装的时候回车有点猛，会导致终端有个（base），可以执行下面命令去除：
conda deactivate
当然，如果你觉得这个base看着也挺舒服的，那可以使用conda activate base增加base。

    想永久修改的话，可以通过修改conda的配置来实现永久更改。使用下面命令查看conda的配置情况，如下：
conda config --show

可以发现，之所以会出现base，是因为框中参数auto_activate_base在作妖，即默认启动base，使用 下面命令将auto_activate_base设置为False即可。

conda config --set auto_activate_base False
当然，我们需要重新登录服务器才看得到改为False。

二.conda的使用

Conda 是一个开源的软件包管理系统和环境管理系统，用于安装多个版本的软件包及其依赖关系，并在它们之间轻松切换。Conda 是为 Python 程序创建的，适用于 Linux，OS X 和Windows，也可以打包和分发其他软件。conda分为anaconda和miniconda。anaconda是包含一些常用包的版本，miniconda则是精简版（miniconda官网：https://conda.io/miniconda.html），需要啥装啥，有人推荐使用miniconda。根据自己需求吧，生信可能接触最多的2种语言就是R和Python，既然我们装了anaconda，那就先用anaconda

添加频道

这个道理跟家里的电视机是一样一样的，conda就相当于买了一台电视机，但是有电视了不意味着你就能看节目了，你要手动添加频道才能看你想看的电视节目，官方名称叫channel：

conda config --add channels biocondaconda config --add channels conda-forge
通常情况下，上面2个channel已经够使啦，不过我们还可以再加一个r。

conda config --add channels r
如果国内下载慢，想换成清华的镜像，那就执行下面命令。

conda config --add channels https://mirrors.tuna.tsinghua.edu.cn/anaconda/pkgs/free/
conda config --add channels https://mirrors.tuna.tsinghua.edu.cn/anaconda/pkgs/main/
conda config --set show_channel_urls yes
conda config --add channels
对于生物信息学来说，需要介绍一下Bioconda，是conda上一个分发生物信息的频道。而conda是最初为管理python包而建立的。所以我们添加了bioconda这个channel后，我们就可以安装各种生物信息学相关软件啦。

不过，要通过conda安装软件，首先得确定该软件是否被conda支持。可以通过搜索查询。

 conda search 软件名
也可以从conda网页内查找：http://bioconda.github.io/conda-package_index.html

如果支持，只需输入以下命令即可安装：
```sh
conda install 软件名
更新指定软件：

conda update 软件名
卸载指定软件：

conda remove 软件名
我们要安装软件：fastqc，首先我们确定该软件是否支持conda

conda search fastqc

确定有该软件，就可以利用conda安装啦。

conda install fastqc
安装过程中可能需要安装或更新一下相关包，会提示，输入y就行。       


安装成功如下：


通常情况下我们需要补上直接在base环境中安装软件的，而是创建一个环境，可能你用R的时候，某些包不适合R版本，所以我们通常会安装几个R的版本。这就给包的管理带来麻烦，我们就可以用conda创建不同环境的R版本。下面我就用R的安装来演示。

和环境相关的命令

conda info --envs # 查看环境
conda create -n R3.5  # 创建名为R3.5的环境
source activate R3.5  
conda list            #查看当前安装的软件
conda install r-base #安装R语言
conda install r-stringi # R包 以 r- 开头 
conda deactivate # 退出当前环境
其他的一些命令：

1. conda --version #查看conda版本，验证是否安装
2. conda update conda #更新至最新版本，也会更新其它相关包
3. conda update --all #更新所有包
4. conda update package_name #更新指定的包
5. conda create -n env_name package_name #创建名为env_name的新环境，并在该环境下安装名为package_name 的包，可以指定新环境的版本号，例如：conda create -n python2 python=python2.7 numpy pandas，创建了python2环境，python版本为2.7，同时还安装了numpy pandas包
6. source activate env_name #切换至env_name环境
7. source deactivate #退出环境
8. conda info -e #显示所有已经创建的环境
9. conda create --name new_env_name --clone old_env_name #复制old_env_name为new_env_name
10. conda remove --name env_name –all #删除环境
11. conda list #查看所有已经安装的包
12. conda install package_name #在当前环境中安装包
13. conda install --name env_name package_name #在指定环境中安装包
14. conda remove -- name env_name package #删除指定环境中的包
15. conda remove package #删除当前环境中的包
16. conda create -n tensorflow_env tensorflow
conda activate tensorflow_env #conda 安装tensorflow的CPU版本
17. conda create -n tensorflow_gpuenv tensorflow-gpu
conda activate tensorflow_gpuenv #conda安装tensorflow的GPU版本
18. conda env remove -n env_name #采用第10条的方法删除环境失败时，可采用这种方法
创建一个环境

conda create -n R

激活环境，并查看该环境下有没有安装软件，当然没有安装啦。

毕竟是我们刚创建的。

source activate R
conda list

我们虽然在R官网指定目前R的最新版本是4.0，不过我们还是要搜索一下。

conda search R
的确有4.0的版本，我们就可以安装4.0的版本啦。安装和上面安装fastqc一样。

conda install r=4.0
```

### conda细节
```shell
conda activate py36
conda deactivate

# conda ssh报错 conda init <SEHLL>
source activate
source deactivate
```


### pip
```sh
pip install markdown -i https://pypi.tuna.tsinghua.edu.cn/simple

# 清华源
pip config set global.index-url https://pypi.tuna.tsinghua.edu.cn/simple

# 或：
# 阿里源
pip config set global.index-url https://mirrors.aliyun.com/pypi/simple/
# 腾讯源
pip config set global.index-url http://mirrors.cloud.tencent.com/pypi/simple
# 豆瓣源
pip config set global.index-url http://pypi.douban.com/simple/


python -m pip install --upgrade pip
pip show pip
```