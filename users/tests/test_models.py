from django.test import TestCase
from users.models import CustomUser

class TestCustomUser(TestCase):
    
    @classmethod
    def setUpTestData(cls):
        # Create user:
        cls.test_user = CustomUser.objects.create_user(
            username='test_user',
            email='test@test.com',
            password='123Testpassword'
        )

    def test_user_attr(self):
        self.assertEqual(self.test_user.username, 'test_user')
        self.assertEqual(self.test_user.email, 'test@test.com')
        self.assertTrue(self.test_user.check_password('123Testpassword'))

    def test_user_str(self):
        self.assertEqual(
            self.test_user.__str__(),
            f' Username: {self.test_user.username} Email: {self.test_user.email}'
        )