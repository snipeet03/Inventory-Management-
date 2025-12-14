from django.contrib.auth.models import User
from django.db import models

# Create your models here.

# models.py
class ExardProduct(models.Model):
    alpha_number = models.CharField(max_length=100, unique=True)
    quantity = models.PositiveBigIntegerField()

    def __str__(self):
        return self.alpha_number

class ProjectType(models.Model) : 
    type = models.CharField(max_length=100)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.type
