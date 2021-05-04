from django.db import models
from django.contrib.auth.models import User
from datetime import datetime
from django.utils.text import slugify
import itertools
# Create your models here.


class Category(models.Model):
    category_name = models.CharField(max_length=40)
    slug = models.SlugField(default="")

    def __str__(self):
        return self.category_name

    def save(self, *args, **kwargs):
        value = self.category_name
        self.slug = slugify(value, allow_unicode=True)
        super().save(*args, **kwargs)


class SubCategory(models.Model):
    sub_category_name = models.CharField(max_length=40)
    category = models.ForeignKey(
        Category, related_name='sub_category', on_delete=models.CASCADE)

    def __str__(self):
        return self.sub_category_name


class Product(models.Model):
    name = models.CharField(max_length=80)
    slug = models.SlugField(default="")
    description = models.TextField()
    price = models.DecimalField(max_digits=9, decimal_places=0)
    photo = models.ImageField(upload_to='product_photos/', null=True)
    category = models.ForeignKey(
        Category, on_delete=models.CASCADE, blank=True, null=True)
    sub_category = models.ForeignKey(
        SubCategory, on_delete=models.CASCADE, blank=True, null=True)
    user = models.ForeignKey(User, null=True, on_delete=models.CASCADE)
    condition = models.CharField(max_length=20)
    warranty = models.IntegerField(null=True, default=0)
    premium = models.BooleanField(default=0)
    views = models.IntegerField(null=True, default=0)
    publish_date = models.DateTimeField(default=datetime.now)
    show_contact = models.BooleanField(default=0)
    favourites = models.ManyToManyField(
        User, related_name='favourite', default=None, blank=True)
    sold = models.BooleanField(default=0)

    def _generate_slug(self):
        max_length = self._meta.get_field('slug').max_length
        value = self.name
        slug_candidate = slug_original = slugify(value, allow_unicode=True)
        for i in itertools.count(1):
            if not Product.objects.filter(slug=slug_candidate).exists():
                break
            slug_candidate = '{}-{}'.format(slug_original, i)

        self.slug = slug_candidate

    def save(self, *args, **kwargs):
        if not self.pk:
            self._generate_slug()

        super().save(*args, **kwargs)


class ProductPhoto(models.Model):
    product = models.ForeignKey(Product, null=True, on_delete=models.CASCADE)
    product_photo = models.ImageField(upload_to='product_photos/', null=True)

    def delete(self, *args, **kwargs):
        self.product_photo.delete()
        super().delete(*args, **kwargs)


class Banner(models.Model):
    name = models.CharField(max_length=80, null=True, unique=True)
    photo = models.ImageField(upload_to='banner_photos/', null=True)
    url = models.CharField(max_length=200, default="#", null=True)


class Questions(models.Model):
    question = models.TextField()
    answer = models.TextField(null=True, default="")
    user = models.ForeignKey(User, null=True, on_delete=models.CASCADE)
    product = models.ForeignKey(
        Product, null=True, on_delete=models.CASCADE, related_name='ques')
    publish_date = models.DateTimeField(default=datetime.now)
