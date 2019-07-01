from django.test import TestCase
from django.contrib.auth.models import User
from django.test.client import Client
from django.urls import reverse


# Create your tests here.
class LoginTestCase(TestCase):
   # fixtures = ['fixture.json',]

   def setUp(self):
       # self.user = User.objects.get(pk=1)
       self.client = Client()

   def test_login_incorrect(self):
       user = User.objects.create(email="test@gmail.com", password="goodpassword", username="user1")
       response = self.client.post(reverse('login'), {
           'email': user.email,
           'password': user.password,
           'username': user.username})

       self.assertEqual(response.status_code, 400)
       # self.assertEqual(response._container[0], '{"error": "Incorrect data"}')

   def test_login_correct(self):
       response = self.client.post(reverse('login'), {
           'email': "test@gmail.com",
           'password': "goodpassword",
           'username': "user1"})

       self.assertEqual(response.status_code, 200)


   def test_unique_email(self):
       user = User.objects.create(email="test@gmail.com", password="goodpassword", username="useramon")
       response = self.client.post(reverse('login'), {
           'email': "test@gmail.com",
           'password': "goodpassword",
           'username': "user1"})

       self.assertEqual(response.status_code, 400)
