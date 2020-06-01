from django.test import TestCase
from django.contrib.auth import get_user_model
from django.urls import reverse
from rest_framework.test import APIClient
from rest_framework import status


CREATE_USER_URL = reverse('user:create')
TOKEN_URL = reverse('user:token')


def create_user(**params):
    return get_user_model().objects.create_user(**params)


class PublicUserAPITest(TestCase):

    def setUp(self):
        self.client = APIClient()

    def test_valid_user_success(self):
        """Test creating user with valid payload is succesful"""
        payload = {
            'email': 'andresnoboa@gmail.com',
            'password': 'mmga17',
            'name': 'Andres'
        }
        res = self.client.post(CREATE_USER_URL, payload)
        self.assertEquals(res.status_code, status.HTTP_201_CREATED)
        user = get_user_model().objects.get(**res.data)
        self.assertTrue(user.check_password(payload['password']))
        self.assertNotIn('password', res.data)

    def test_user_exist(self):
        """Test that the user don't allready exist"""
        payload = {
            'email': 'andresnoboa17@gmail.com',
            'password': 'mmga1997',
            'name': 'Andres'
        }
        create_user(**payload)
        res = self.client.post(CREATE_USER_URL, payload)
        self.assertEquals(res.status_code, status.HTTP_400_BAD_REQUEST)

    def test_password_too_short(self):
        """Test that the password most be more than 5 characters"""
        payload = {
            'email': 'andresnoboa17@gmail.com',
            'password': 'mmg',
            'name': 'Andres'
        }

        res = self.client.post(CREATE_USER_URL, payload)
        self.assertEquals(res.status_code, status.HTTP_400_BAD_REQUEST)
        user_exist = get_user_model().objects.filter(
            email=payload['email']
        ).exists()
        self.assertFalse(user_exist)

    def test_create_token_for_user(self):
        """Test that a token is created for a user"""
        payload = {
            'email': 'andresnoboa@gmail.com',
            'password': 'emily6678'
        }
        create_user(**payload)
        res = self.client.post(TOKEN_URL, payload)
        self.assertIn('token', res.data)
        self.assertEquals(res.status_code, status.HTTP_200_OK)

    def test_invalid_credentials(self):
        """Test that token is not created is the credentials aren't rigth"""

        create_user(email='andresnoboa17@gmail.com', password='aja78')
        payload = {
            'email': 'andresnoboa17@gmail.com',
            'password': 'tommy77'
        }
        res = self.client.post(TOKEN_URL, payload)
        self.assertNotIn('token', res.data)
        self.assertEquals(res.status_code, status.HTTP_400_BAD_REQUEST)

    def test_create_token_no_user(self):
        """Test that token is not created is the user doesn't exist"""
        payload = {
            'email': 'andresnoboa17@gmail.com',
            'password': 'tommy77'
        }
        res = self.client.post(TOKEN_URL, payload)
        self.assertNotIn('token', res.data)
        self.assertEquals(res.status_code, status.HTTP_400_BAD_REQUEST)

    def test_create_token_missing_field(self):
        """Test that email and password are required"""
        res = self.client.post(TOKEN_URL, {'email': '', 'password': ''})
        self.assertNotIn('token', res.data)
        self.assertEquals(res.status_code, status.HTTP_400_BAD_REQUEST)
