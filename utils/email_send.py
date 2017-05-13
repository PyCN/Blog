import random
from django.core.mail import send_mail
import string
from users.models import EmailVerifyCode
from July.settings import EMAIL_FROM
from users.models import UserProfile


def send_password_email(email):
    email_record = EmailVerifyCode()
    code = ''.join(random.sample(string.ascii_letters + string.digits, 20))  # 注册获取16位长度的字符
    email_record.code = code  # 验证码
    email_record.email = email  # 邮箱
    email_record.save()  # 保存到数据库中
    nick_name = UserProfile.objects.get(email=email).nick_name
    email_title = "{0} - 重置密码".format(nick_name)
    email_body = "请点击下面的链接重置你的密码：http://127.0.0.1:8000/password?code={0}".format(code)
    send_status = send_mail(email_title, email_body, EMAIL_FROM, [email])
    return send_status
