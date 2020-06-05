from rest_framework.test import APITestCase
from rest_framework import status
from django.urls import reverse


class LoginTestCase(APITestCase):
    """ Test module for POST login API """

    def test_login(self):
        data = {
          "username": "user1",
          "email": "",
          "password": "123456"
        }
        url = "http://0.0.0.0:8000/api/login/"
        response = self.client.post(url, data, format='json')
        print(response)
        self.assertEqual(response.status_code, status.HTTP_200_OK)


class RegistrationTEstCase(APITestCase):

    def test_registration(self):
        url = "/rest-auth/registration/"
        data = {
          "username": "karo",
          "email": "user@example.com",
          "password1": "Antos1920",
          "password2": "Antos1920"
        }

        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
# class RollDiceTests(APITestCase):
#     """ Test module for GET roll-dice API """
#
#     def setUp(self):