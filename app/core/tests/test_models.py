from django.test import TestCase
from django.contrib.auth import get_user_model


class ModelTest(TestCase):

    def test_create_user_with_email_succesful(self):
        """Test creating a new user with email is succesful"""
        email = 'andresnoboa17@hotmail.com'
        password = 'hola123'
        user = get_user_model().objects.create_user(
            email=email,
            password=password
        )

        self.assertEqual(user.email, email)
        self.assertTrue(user.check_password(password))

    def test_new_user_email_normalize(self):

        email = 'andresnoboa17@HOTMAIL.COM'
        user = get_user_model().objects.create_user(email, 'hola123')

        self.assertEqual(user.email, email.lower())

    def test_new_user_invalid_email(self):

        with self.assertRaises(ValueError):
            get_user_model().objects.create_user(None, 'hola123')

    def test_superuser_is_created(self):

        user = get_user_model().objects.create_superuser(
            'andresnoboa17@hotmail.com', 'hola123')
        self.assertTrue(user.is_superuser)
        self.assertTrue(user.is_staff)
