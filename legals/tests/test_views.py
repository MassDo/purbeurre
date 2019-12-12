from django.test import TestCase, Client
from django.urls import reverse
from search.forms import FoodSearchForm


class TestViews(TestCase):

    def setUp(self):
        # Path
        self.legals_url = reverse('legals-legals')
        # Client
        self.c = Client()
        # Form transmitted
        self.form = FoodSearchForm()

    def test_legals_template_if_user_is_logged(self):  
        response = self.c.get(self.legals_url)

        # Test response status and correct template return
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'legals/legals.html')
        # Test if form in context is an instanciation of FoodSearchForm()
        self.assertEqual(type(response.context['form_search']), type(self.form))

