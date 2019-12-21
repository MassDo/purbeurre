from django.test import TestCase
from django.urls import reverse
from search.forms import FoodSearchForm
from signup.forms import UserRegistrationForm
from users.models import CustomUser


class TestView(TestCase):


    @classmethod
    def setUpTestData(cls):

        cls.signup_url = reverse('signup')
        cls.user = CustomUser.objects.create_user(
            email='user@test.com',
            username='username_test',
            password='123Testing'
        )

    def test_signup_get(self):
        response = self.client.get(self.signup_url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'signup/signup.html')
        self.assertTrue(isinstance(response.context['form_search'], FoodSearchForm))
        self.assertTrue(isinstance(response.context['reg_form'], UserRegistrationForm))

    def test_signup_post(self):
        data = {
            'email':'test@test.com',
            'username':'test',
            'password1':'123Testpass',
            'password2':'123Testpass',
        }
        response = self.client.post(self.signup_url, data)
        self.assertEqual(response.status_code, 200)
        
        username = response.context['username']
        self.assertEqual(username, 'test')
        message = list(response.context['messages'])
        self.assertEqual(str(message[0]), f'{username}, your account has been created! You are now able to log in')
        self.assertTemplateUsed(response, 'users/login.html')
        self.assertTrue(isinstance(response.context['form_search'], FoodSearchForm))
    
    def test_signup_post_logged(self):
        self.client.login(
            email='user@test.com',
            password='123Testing'
        )
        response = self.client.get(self.signup_url)
        self.assertRedirects(
            response=response,
            expected_url=reverse('account-account'),
            status_code=302,
            target_status_code=200, 
        )

