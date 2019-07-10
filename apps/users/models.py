from django.contrib.auth.models import AbstractUser
from django.db import models


# Create your models here.
class UserProfile(AbstractUser):
    mobile = models.CharField(max_length=11, null=True, blank=True, verbose_name='手机号码')
    birthday = models.DateField(null=True, blank=True, verbose_name='出生日期')
    gender = models.CharField(max_length=6, choices=(('male', '男'), ('female', '女')), verbose_name='性别')

    def __str__(self):
        return self.username

    class Meta:
        verbose_name = '用户表'
        verbose_name_plural = verbose_name


# 手机验证
class VerifyCode(models.Model):
    code = models.CharField(max_length=6, verbose_name='验证码')
    mobile = models.CharField(max_length=11, verbose_name='手机号码')
    send_time = models.DateTimeField(verbose_name='发送时间', auto_now=True)

    def __str__(self):
        return self.mobile

    class Meta:
        verbose_name = '验证码表'
        verbose_name_plural = verbose_name
