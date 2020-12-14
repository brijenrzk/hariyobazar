from django.db import models
from django.contrib.auth.models import User
from datetime import datetime
# Create your models here.


class Category(models.Model):
    category_name = models.CharField(max_length=40)

    def __str__(self):
        return self.category_name


class SubCategory(models.Model):
    sub_category_name = models.CharField(max_length=40)
    category = models.ForeignKey(
        Category, related_name='sub_category', on_delete=models.CASCADE)

    def __str__(self):
        return self.sub_category_name


class Product(models.Model):
    name = models.CharField(max_length=80)
    description = models.TextField()
    price = models.DecimalField(max_digits=9, decimal_places=2)
    category = models.ForeignKey(
        Category, on_delete=models.SET_NULL, blank=True, null=True)
    sub_category = models.ForeignKey(
        SubCategory, on_delete=models.SET_NULL, blank=True, null=True)
    user = models.ForeignKey(User, null=True, on_delete=models.CASCADE)
    condition = models.CharField(max_length=20)
    warranty = models.IntegerField(null=True, default=0)
    premium = models.BooleanField(default=0)
    views = models.IntegerField(null=True, default=0)
    publish_date = models.DateField(default=datetime.now)


class ProductPhoto(models.Model):
    product = models.ForeignKey(Product, null=True, on_delete=models.CASCADE)
    product_photo = models.ImageField(upload_to='product_photos/', null=True)


class Wishlist(models.Model):
    user = models.ForeignKey(User, null=True, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, null=True, on_delete=models.CASCADE)
