from django.test import TestCase
from .models import *
from django.urls import reverse
from http import HTTPStatus
# Create your tests here.


class BaseTest(TestCase):
    def setUp(self):
        self.category = Category.objects.create(
            category_name="furniture")
        self.subCategory = SubCategory.objects.create(
            category=self.category, sub_category_name="home")
        self.product = Product.objects.create(
            name="bed", description="good product", price=500, category=self.category, sub_category=self.subCategory, condition=2)

        return super().setUp()

    def testCategory(self):
        c = Category.objects.get(id=self.category.id)
        self.assertEqual(c.category_name, 'furniture')

    def testProductPremium(self):
        a = Product.objects.get(id=self.product.id)
        self.assertFalse(a.premium)

    def testProductSubCategory(self):
        p = Product.objects.get(id=self.product.id)
        self.assertEqual(p.sub_category.sub_category_name, 'home')
