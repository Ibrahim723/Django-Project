from django.db import models
from rest_framework import serializers

class User(models.Model):
    username = models.CharField(max_length=255, unique=True)
    balance = models.FloatField()

    def __str__(self):
        return self.username