from django.db import models
from datetime import datetime
from django.utils.text import slugify
from ckeditor.fields import RichTextField

# Create your models here.


class Blogs(models.Model):
    title = models.CharField(max_length=200, null=True)
    slug = models.SlugField(default="", max_length=200)
    photo = models.ImageField(upload_to='blogs_photos/', null=True)
    description = RichTextField(blank=True, null=True)
    publish_date = models.DateTimeField(default=datetime.now)

    def save(self, *args, **kwargs):
        value = self.title
        self.slug = slugify(value, allow_unicode=True)
        super().save(*args, **kwargs)
