from django.test import TestCase, Client
from django.contrib.auth import get_user_model
from django.urls import reverse

class AdminSiteTests(TestCase):

    def setUp(self):
        self.client = Client()
        payloads = {'email':'ah@gmail.com','password':'test1234'}
        payloads2 = {'email': 'aaaa@gmail.com', 'password': 'test12345'}
        self.admin_user = get_user_model().objects.create_superuser(**payloads)
        self.client.force_login(self.admin_user)
        self.user = get_user_model().objects.create_user(**payloads2)

    def test_user_listed(self):
        """Test if the user email is listed or not with a user email"""
        url = reverse("admin:core_account_changelist")
        response = self.client.get(url)
        self.assertContains(response, self.user.email)

    def test_user_listed_anonymous(self):
        """Test if the user email is listed or not with a user email"""
        url = reverse("admin:core_account_changelist")
        response = self.client.get(url)
        with self.assertRaises(AssertionError):
            """It should raise error"""
            self.assertContains(response, "fake_email@gmail.com")
    
    def test_user_change_page(self):
        """Test that hte user edit page works"""
        url = reverse('admin:core_account_change', args=[self.user.id])
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
    
    def create_user_page(self):
        """Test create user page"""
        url = reverse('admin:core_account_add')
        response = self.client.get(url)

        self.assertEqual(response.status_code,200 )