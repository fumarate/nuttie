# autosign_python

此程序可以帮助你每日健康打卡。与之前的版本相比，此版本采用模拟请求方式，无需再安装一大堆<s>恶臭的</s>依赖了。

# 配置文件结构

请查看config-template.json5。

使用时，将其重命名为config.json5，并修改相关信息。

# 在你的计算机上测试

## 1. 安装python

进入[python官方网站](https://www.python.org/),点击“Downloads”并按提示进行下载。下载完成后打开安装包进行安装。

如果你使用Windows，则不要忘记在正式安装确认前，勾选“Add to PATH”以将python路径添加到PATH中。

如果你使用Unix，除官网下载安装包外，你可以使用操作系统对应的包管理器安装python。例如，在Debian/Ubuntu上使用`apt`，在Archlinux下使用`pacman`或在MacOS上使用`brew`。另外，在Unix中一般都是自动配置PATH环境变量的。

安装完成，打开你操作系统的终端，输入python，看看是否进入python交互式代码运行环境中。

## 2.下载项目代码

在项目页面，点击code，再点击Download zip，下载代码压缩包，并解压到合适的位置。

## 3.编辑配置

将config-template.json5重命名为config.json5并修改相应配置。

## 4.安装依赖

在项目文件夹，打开终端，执行`pip install -r requirements.txt`。

## 5.运行
在项目文件夹，打开终端。执行`python auto.py`。

# <s>部署到腾讯云函数</s>

尽管这个版本可以部署到云函数，但由于云函数不再免费了，所以不写了。

# 部署到github action

第一步，Fork本仓库。

第二步，进入你Fork所得到的仓库，点击Settings>Secrets>Actions。

第三步，点击New repository secret。新建USER_ID、PASSWORD变量。SC_KEY变量是可选的，用于发送微信通知。

如果你需要定制打卡时间，请自行修改.github/workflows/autosign.yaml中的cron表达式，并提交一次commit。含义如下：
```markdown
┌──────── 分钟 (0~59)
| ┌────── 小时 (0~23)
| | ┌──── 日期 (1~31)
| | | ┌── 月份 (1~12 or JAN~DEC)
| | | | ┌ 星期 (0~6 or SUN~SAT)
| | | | |
| | | | |
| | | | |
* * * * *
```
注意：

1、github action仅支持精确到分钟的五位cron表达式。

2、github action遵循的是UTC时间。也就是说，对小时位数值+8并对24取余，得到的才是真实时间。

请不要在高峰期打卡！

对应的yml配置文件未编写，请先不要尝试！

# 关于定时
定时功能并不在程序的实现范围内，本程序只将繁琐的登录点击流程集中自动化了。若你需要定时打卡，务必需要一台24h运行的PC或服务器，利用crontab等功能定时执行代码。