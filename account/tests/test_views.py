from django.test import TestCase, Client
from django.urls import reverse
from users.models import CustomUser


class TestViews(TestCase):

    def setUp(self):
        # User 
        self.user = CustomUser.objects.create_user(
            email='testuser@testuser.com',
            username='testuser',
            password='Testuser123'
        )
        # Client
        self.c = Client()
        # Path
        self.account_url = reverse('account-account')
        
    def test_account_redirect_to_login_if_user_not_logged(self):        
        response = self.c.get(self.account_url)
        # test acces denial and redirect status
        self.assertEqual(response.status_code, 302)
        # test redirect to login then to account
        self.assertEqual(response.url, reverse('login') + '?next=/account/')

    def test_account_template_if_user_is_logged(self):  
        # User login     
        login = self.c.login(
            email='testuser@testuser.com',
            password='Testuser123'
        )
        response = self.c.get(self.account_url)

        # Test response status and correct template return
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'account/account.html')

