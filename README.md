# Python
A free, open-source blog system based on Django + MySql + jQuery + bootstrap + markdown

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
   pip install -r requirements.txt
   
2、创建MySql数据库  
   在linux shell中登陆mysql: $mysql -u root -p  
   创建Blog数据库:           myql>CREATE DATEBASE 'Blog'  DEFAULT CHARACTER SET utf8 COLLATE utf8_general_ci;  
   创建mysql普通用户:        mysql>INSERT INTO mysql.user(Host,User,Password) VALUES('localhost', 'your_username', password('your_password'));  
   为用户授权:               mysql>grant all on Blog.* to your_username@loacalhost identified by 'your_password';  
   退出数据库:               mysql>exit
   
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
