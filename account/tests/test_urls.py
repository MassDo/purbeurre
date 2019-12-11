from django.test import SimpleTestCase
from django.urls import reverse, resolve
from account.views import account


class TestUrls(SimpleTestCase):

    
    def test_account_name_is_reversed_and_resolved(self):
        """
            Check if the name of url is linked to the
            correct path. And if the correct template is returned
        """
        url = reverse("account-account")
        # name linked to url
        self.assertEqual(resolve(url).view_name, 'account-account')
        # url linked to the correct view function
        self.assertEqual(resolve(url).func, account)