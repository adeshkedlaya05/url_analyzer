# models.py
from django.db import models
from django.contrib.auth.models import User
class URLHistory(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    url = models.CharField(max_length=500)
    result = models.CharField(max_length=20)
    timestamp = models.DateTimeField(auto_now_add=True)
