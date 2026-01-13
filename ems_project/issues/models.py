from django.db import models
from accounts.models import User

class Issue(models.Model):
    employee = models.ForeignKey(User, on_delete=models.CASCADE)
    description = models.TextField()
    status = models.CharField(max_length=20, default='OPEN')
