from django.test import TestCase
from .models import *
from django.urls import reverse
from http import HTTPStatus
from django.utils.text import slugify
# Create your tests here.


class BaseTest(TestCase):
    def setUp(self):
        self.blog = Blogs.objects.create(
            title="Test Blog", description="New blog is great.")
        return super().setUp()

    def testBlog(self):
        c = Blogs.objects.get(id=self.blog.id)
        self.assertEqual(c.title, 'Test Blog')

    def testBlogSlug(self):
        s = Blogs.objects.get(id=self.blog.id)
        self.assertEqual(s.slug, slugify("Test Blog", allow_unicode=True))
