from django.db import models
from django.contrib.auth.models import User
# Create your models here.


class UserProfile(models.Model):
    USER_GENDER_TYPE = (
        ('male', 'male'),
        ('female', 'female'),
    )

    owner = models.OneToOneField(User, on_delete=models.CASCADE, verbose_name='user')
    nick_name = models.CharField("nick_name", max_length=23, blank=True, default='')
    description = models.TextField("description", max_length=200, blank=True, default='')
    motto = models.CharField("motto", max_length=100, blank=True, default='')
    birthday = models.DateField("birthday", null=True, blank=True, default='')
    gender = models.CharField("gender", max_length=6, choices=USER_GENDER_TYPE, default='male')
    address = models.CharField("address", max_length=100, blank=True, default='')
    image = models.ImageField(upload_to='images/%Y/%m', default='images/default.jpg', max_length=100, verbose_name='User Image')

    class Meta:
        verbose_name = '用户数据'
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.owner.username


# 邮箱验证记录
class EmailVerifyRecord(models.Model):

    SEND_TYPE_CHOICES = (
        ('register', 'register'),
        ('forget', 'forget'),
    )

    captcha = models.CharField('captcha', max_length=20)
    email = models.EmailField('email', max_length=50)
    send_type = models.CharField(choices=SEND_TYPE_CHOICES, max_length=10, default='register')
    send_time = models.DateTimeField('time', auto_now_add=True)

    class Meta:
        verbose_name = 'email captcha'
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.captcha
