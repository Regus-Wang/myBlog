from users.models import EmailVerifyRecord  # 这是邮箱验证记录的类
from django.core.mail import send_mail  # Django的封装邮件发送的方法
import random
import string


def random_str(randomLength=8):
    chars = string.ascii_letters + string.digits    # 生成a-z，0-9字符串
    captcha = ''.join(random.sample(chars, randomLength))    # 生成随机字符串（使用random方法随机拼接
    return captcha


def send_register_email(email, send_type='register'):
    email_record = EmailVerifyRecord()
    captcha = random_str()
    email_record.captcha = captcha
    email_record.email = email
    email_record.send_type = send_type
    email_record.save()

    if send_type == 'register':
        email_title = "Wang Zilong's Blogsite Verification Email"
        email_body = "My Dear Friend:\n" \
                     "Hi, my friend! This is Zilong Wang.\n" \
                     "Please click the link below to activate your account in my blog: " \
                     "http://127.0.0.8000/users/active/{0}".format(captcha)
        send_status = send_mail(email_title, email_body, 'zilongwangzlw@163.com', [email])
        return send_status

    elif send_type == 'forget':
        email_title = 'Wang Zilong Blogsite Password Reset Link Mail'
        email_body = "My Dear Friend:\n" \
                     "Hi, my friend! What, you forget your password? What a poor guy.\n" \
                     "Please click the link below to change your password: " \
                     "http://127.0.0.1:8000/users/forget_pwd_url/{0}".format(captcha)

        send_status = send_mail(email_title, email_body, 'zilongwangzlw@163.com', [email])
        if send_status:
            pass
