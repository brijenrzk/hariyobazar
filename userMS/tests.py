from django.test import TestCase
from .models import *
from django.urls import reverse
from http import HTTPStatus
# Create your tests here.


class BaseTest(TestCase):
    def setUp(self):
        self.user = User.objects.create(
            first_name="Ram", last_name="Shrestha", username="ramu1", password="tech2020", email="ram@gmail.com")
        self.customer = Customer.objects.create(
            user=self.user, address="ktm", contact="9876463632", dob="Dec 11, 2001", gender="Male")

        return super().setUp()

    def testUser(self):
        c = Customer.objects.get(user_id=self.user.id)
        self.assertEqual(c.address, 'ktm')

    def testUserActive(self):
        c = User.objects.get(id=self.user.id)
        self.assertTrue(c.is_active)

    def testUserOnlineStatus(self):
        c = Customer.objects.get(id=self.user.id)
        self.assertFalse(c.online_status)
