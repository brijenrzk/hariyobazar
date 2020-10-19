from django.db import models
from datetime import datetime
from django.contrib.auth.models import User

# Create your models here.


class Customer(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    photo = models.ImageField(upload_to='uploads/', null=True)
    address = models.CharField(max_length=30)
    contact = models.BigIntegerField(null=True)
    dob = models.CharField(max_length=40)
    gender = models.CharField(max_length=10)

    def __str__(self):
        return self.user.first_name
