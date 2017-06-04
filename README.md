# Python
A free, open-source blog system based on Django + MySQL + jQuery + bootstrap + markdown

目前已实现功能：

1、用户注册、登陆、上传用户头像

2、文章发表，分类，标签集合,最热文章、最新评论展示

3、评论, 点赞, 显示用户评论过的文章

4、文件上传、下载

5、用户权限控制

6、二维码转换

7、站点缓存

8、完整的测试

9、jQuery, bootstrap, markdown支持

10、haystack + whoosh + jieba 搜索

11、logging记录log信息

12、主从数据库(详情可以进入网站http://cblog.xyz)

目前项目已部署在阿里云服务器中，<a href='http://cblog.xyz' target='_blank'>网址</a>为http://cblog.xyz



使用说明:

1、安装依赖包  
   $ sudo pip install -r requirements.txt  

   **ubuntu**  
   $ sudo apt-get install redis-server  
   $ sudo apt-get install rabbitmq-server  

   **centos**
```
   $ sudo yum install nginx
   $ sudo yum install redis
   $ sudo systemctl start redis.service
   $ sudo systemctl enable redis.service # 开机启动

   $ wget http://dev.mysql.com/get/mysql-community-release-el7-5.noarch.rpm
   $ sudo rpm -ivh mysql-community-release-el7-5.noarch.rpm
   $ sudo yum install mysql-community-server
   $ sudo yum install mysql-community-devel
   $ sudo service mysqld restart

   $ wget https://github.com/rabbitmq/rabbitmq-server/releases/download/rabbitmq_v3_6_10/rabbitmq-server-3.6.10-1.el7.noarch.rpm
   $ rpm --import https://www.rabbitmq.com/rabbitmq-release-signing-key.asc
   $ sudo yum install rabbitmq-server-3.6.10-1.el7.noarch.rpm

 ```

2、创建MySQL数据库  
```
   创建mysql root密码: $ mysqladmin -u root password "newpass"
   修改mysql时区 
   $ sudo vim /etc/my.conf # 在[mysqld]下添加:default-time-zone='+8:00'
   在linux shell中登陆mysql: $mysql -u root -p  
   创建Blog数据库:           myql>CREATE DATABASE `Blog` DEFAULT CHARACTER SET utf8 COLLATE utf8_general_ci;  
   为用户授权:               mysql>grant all on Blog.* to your_username@localhost identified by 'your_password';  
   退出数据库:               mysql>exit  
```
   
3、在settings.py所在目录创建个人配置文件mysettings.py(或者直接修改settings.py中的DATABASE配置)  
   #coding:utf-8  
   DEBUG = True  
   DATABASES = {  
       'default': {  
           'ENGINE': 'django.db.backends.mysql',  
           'NAME': 'Blog',  
           'USER': 'your_username',  
           'PASSWORD': 'your_password',  
           'HOST': '127.0.0.1',  
           'PORT': '3306'  
        }  
   }  
   
4、创建数据库table  
   在manage.py目录执行:python manage.py migrate
   
5、运行服务器  
   python manage.py runserver 8080
   
接下来就可以在浏览器访问localhost:8080

ps:如果用apache2或者nginx运行时，访问具体文章速度很慢时，可以查看apache2或者nginx的log。如果是jieba那边提示Operation not permitted，那么就查看/tmp/jieba.cache的权限是否为774，如果不是请修改为774
