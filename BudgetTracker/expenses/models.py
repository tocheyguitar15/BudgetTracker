from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class Tracker(models.Model):
    uname = models.CharField(max_length=100)
    quote = models.CharField(max_length=200)
    cost = models.IntegerField()

# class Users(models.Model):
#     username = models.CharField(max_length=60)
#     password = models.CharField(max_length=50)
