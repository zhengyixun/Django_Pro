# This is an auto-generated Django model module.
# You'll have to do the following manually to clean this up:
#   * Rearrange models' order
#   * Make sure each model has one field with primary_key=True
#   * Make sure each ForeignKey has `on_delete` set to the desired behavior.
#   * Remove `managed = False` lines if you wish to allow Django to create, modify, and delete the table
# Feel free to rename the models, but don't rename db_table values or field names.
from __future__ import unicode_literals

from django.db import models

class Userinfo(models.Model):
    user = models.CharField(max_length=32)
    pwd = models.CharField(max_length=32)
    ages = models.CharField(max_length=32, blank=True, null=True)
    sex = models.CharField(max_length=10, blank=True, null=True)
    last_login_time = models.DateTimeField(blank=True, null=True)
    token = models.CharField(max_length=100, blank=True, null=True)

class Image(models.Model):
    img = models.ImageField(upload_to='img')
    time = models.DateTimeField(auto_now_add=True)

