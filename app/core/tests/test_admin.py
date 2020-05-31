from django.test import TestCase, Client
from django.contrib.auth import get_user_model
from django.urls import reverse


class AdminSiteTest(TestCase):
    """Class to test Admin"""

    def setUp(self):
        self.client = Client()
        self.admin_user = get_user_model().objects.create_superuser(
            email="andresnoboa17@hotmail.com",
            password="mmga1997"
        )
        self.client.force_login(self.admin_user)
        self.user = get_user_model().objects.create_user(
            email="emily@hotmail.com",
            password="hola123",
            name="Emily Blunt"
        )

    def test_users_listed(self):

        url = reverse('admin:core_user_changelist')
        res = self.client.get(url)

        self.assertContains(res, self.user.name)
        self.assertContains(res, self.user.email)

    def test_user_change_page(self):

        url = reverse('admin:core_user_change', args=[self.user.id])
        res = self.client.get(url)

        self.assertEqual(res.status_code, 200)
