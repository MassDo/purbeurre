from django.test import TestCase
from search.forms import FoodSearchForm, FoodSearchFormMain


class TestForm(TestCase):

    def test_food_search_form_valid(self):
        data = {
            'user_input':'test string'
        }
        form = FoodSearchForm(data=data)
        self.assertEqual(form.is_valid(), True)

    def test_food_search_form_main_valid(self):
        data = {
            'main_form':'test string'
        }
        form = FoodSearchFormMain(data=data)
        self.assertEqual(form.is_valid(), True)
    