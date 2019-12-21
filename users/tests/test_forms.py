from django.test import TestCase
from users.forms import UserLoginForm
from users.models import CustomUser

class TestForms(TestCase):

    @classmethod
    def setUpTestData(cls):
        # Create user:
        cls.test_user = CustomUser.objects.create_user(
            username='test_user',
            email='test@test.com',
            password='123Testpassword'
        )

    def test_forms(self):
        credentials = {
            'username': 'test@test.com',
            'password': '123Testpassword'
        }
        self.assertTrue(self.client.login(**credentials))
