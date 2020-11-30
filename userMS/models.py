from django.db import models
from datetime import datetime
from django.contrib.auth.models import User


# Create your models here.
User._meta.get_field('email')._unique = True


class Customer(models.Model):
    GENDER_CHOICES = [
        ('Male', 'Male'),
        ('Female', 'Female'),
        ('Other', 'Other'),
    ]
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    photo = models.ImageField(upload_to='uploads/', null=True)
    address = models.CharField(max_length=30, null=True, blank=True)
    contact = models.BigIntegerField(null=True, blank=True)
    dob = models.CharField(max_length=40)
    gender = models.CharField(
        max_length=10, choices=GENDER_CHOICES, default="Male")
    online_status = models.BooleanField(default=0)

    def __str__(self):
        return self.user.first_name

    def delete(self, *args, **kwargs):
        self.photo.delete()
        super().delete(*args, **kwargs)


class EmailVerification(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    verify_code = models.BigIntegerField(null=True, blank=True)
    verify_status = models.BooleanField(default=0)

    def __str__(self):
        return self.user.email
