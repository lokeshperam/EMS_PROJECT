from django.db import models
from accounts.models import User

class Performance(models.Model):
    employee = models.ForeignKey(User, on_delete=models.CASCADE)
    rating = models.IntegerField()
    remarks = models.TextField()
