# coding=utf-8
from django.db import models

# Create your models here.
class UserInfo(models.Model):
    uname=models.CharField(max_length=20)
    upwd=models.CharField(max_length=40)
    uemail=models.CharField(max_length=40)
    ushou = models.CharField(max_length=20, default='')
    uaddress = models.CharField(max_length=20, default='')
    uyoubian = models.CharField(max_length=6, default='')
    uphone = models.CharField(max_length=11, default='')
    # default 和 blank是python层面的约束,不影响数据库表结构



