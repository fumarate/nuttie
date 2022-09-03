# autosign_python

*谨以此仓库纪念你，我还未熟悉却已离去的朋友*

*Dedicated to you, who has gone before I am familiar with*

此程序可以帮助你每日健康打卡。与之前的版本相比，此版本采用模拟请求方式，无需再安装一大堆<s>恶臭的</s>依赖了。

# 程序特色

- [x] 多用户支持
- [x] 邮件通知打卡情况，支持管理员和用户模式
- [ ] TODO：各种伪装术，看起来更像“人”

# 配置文件结构

请查看 config-template.json5。

使用时，将其重命名为 config.json5，并修改相关信息。

# 在你的计算机上测试

## 1. 安装 python

进入[python 官方网站](https://www.python.org/),点击“Downloads”并按提示进行下载。下载完成后打开安装包进行安装。

如果你使用 Windows，则不要忘记在正式安装确认前，勾选“Add to PATH”以将 python 路径添加到 PATH 中。

如果你使用 Unix，除官网下载安装包外，你可以使用操作系统对应的包管理器安装 python。例如，在 Debian/Ubuntu 上使用`apt`，在 Archlinux 下使用`pacman`或在 MacOS 上使用`brew`。另外，在 Unix 中一般都是自动配置 PATH 环境变量的。

安装完成，打开你操作系统的终端，输入 python，看看是否进入 python 交互式代码运行环境中。

## 2.下载项目代码

在项目页面，点击 code，再点击 Download zip，下载代码压缩包，并解压到合适的位置。

## 3.编辑配置

将 config-template.json5 重命名为 config.json5 并修改相应配置。

## 4.安装依赖

在项目文件夹，打开终端，执行`pip install -r requirements.txt`。

## 5.运行

在项目文件夹，打开终端。执行`python auto.py`。

# 关于定时

定时功能并不在程序的实现范围内，本程序只将繁琐的登录点击流程集中自动化了。若你需要定时打卡，务必需要一台 24h 运行的 PC 或服务器，利用 crontab 等功能定时执行代码。

# 声明/Declaration

无论是此程序，还是健康日报平台，登陆后都会调用`com.sudytech.work.uust.zxxsmryb.xxsmryb.hdlgUtil.biz.ext`API，从而可以获得账号对应的各种个人信息，包括但不限于：

- 账号主人及所填写“紧急联系人”的姓名与联系方式
- 学院、专业、班级
- 家庭住址
- **身份证号码**

本程序已经开源，您可以阅读源码，了解本程序对于个人信息的处理流程。您如果在自己的计算机上运行，作者是不可能得到您的信息的。但无论您在什么平台上运行该程序，都请注意，不要泄露您的`config.json5`配置文件。

It is easy to get the private data of the account after login due to the calling of the API `com.sudytech.work.uust.zxxsmryb.xxsmryb.hdlgUtil.biz.ext` in both of the program and the platform of the school. These data includes, but not limited to:

- The name and the telephone number of the account owner and the "emergency contact"
- School, major and class
- Home address
- **Identity card number**

This program is open-source so you can view the codes to learn how the program process these data. Your data will not be transfered to the author if you only run it on your PC. However, it must be taken care of that your `config.json5` configuration file are not disclosed.
