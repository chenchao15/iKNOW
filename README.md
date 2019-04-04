# iKNOW
## iKNOW---the college competition platform website


本项目基于vue前端, django rest framework后端实现了一个大学生竞赛平台网站：

![图片说明1](https://github.com/chenchao15/iKNOW/blob/master/doc/open.png)

iKNOW大学生竞赛平台，致力于实现当前市场现有竞赛平台网站所具有的基本功能,并在此基础上充分考虑用户需求,开发出新的功能,以提高竞争力。目前，已经实现了所有项目之初所定下的功能：

1.完整的注册、登录以及邮箱验证功能，包括参赛者和组织者两种类型

2.用户可以进行个人信息设置

3.用户可以查看当前各种比赛信息，并可收藏比赛

4.用户可以查看当前发布的各种教程，包括官方教程(由组织者发布)和(学友分享)

5.用户之间可以进行私信往来

##配置环境:

前端：

node.js　9.0.0

npm 5.5.1

vue.js 2.9.1

后端：

python 3.5.2

django 1.11.7

mysql 5.7.20

django-rest-framework 3.7.3

##系统部署:

在Ubuntu16.04 LTS中，我们当前情况下准备使用NGINX部署,如下：

sudo apt install nginx

service nginx restart

支持php文件解析：

sudo apt install php php-fpm

配置虚拟环境并运行:

sudo apt install python3-dev

sudo apt install python3-venv

python3 –m venv ./venv

Source .venv/bin/activate

安装uwsgi:

pip install uwsgi

安装django:

pip install Django

连接django到NGINX，运行uwsgi:

uwsgi –ini uwsgi.ini

启动nginx:

service nginx restart


