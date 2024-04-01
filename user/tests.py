from rest_framework.test import APITestCase
from django.test import TestCase
from django.urls import reverse
from user.models import User


class UserCreateTest(APITestCase):
    url = reverse("user_creator")

    def setUp(self):
        self.user_data = {"email": "test@gmail.com", "password": "testpassword"}
       

    def test_user_creator(self):
        """
        계정생성 테스트
        """
        response = self.client.post(path=self.url, data=self.user_data)
        self.assertEqual(response.status_code, 201)

class ProfileAPIViewTest(APITestCase):
    url = reverse("user_creator")

    def setUp(self):
        self.user_data = {"email": "test@gmail.com", "password": "testpassword"}
        self.user = User.objects.create("email": "test@gmail.com", "nickname": "test1","password": "testpassword")
        

