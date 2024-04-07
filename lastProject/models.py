# models.py

from django.db import models

class User(models.Model):
    email = models.EmailField(max_length=254, default='example@example.com')
    username = models.CharField(max_length=100)
    password = models.CharField(max_length=100)
    password_repeat = models.CharField(max_length=100)
    profile_picture = models.ImageField(upload_to='profile_pics', blank=True, null=True)
