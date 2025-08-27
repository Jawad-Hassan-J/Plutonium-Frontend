from django.db import models
from django.urls import reverse
from datetime import date
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver


# Create your models here.


class User(models.Model):
    username = models.CharField(max_length=100, unique=True)
    password = models.CharField(max_length=255) 

    def __str__(self):
        return self.username

class Tool(models.Model):
    name = models.CharField(max_length=100) 
    description = models.TextField(blank=True)
    examples = models.JSONField(default=list, blank=True)

    def __str__(self):
        return self.name