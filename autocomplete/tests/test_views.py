import json
from django.test import TestCase
from django.urls import reverse
from product.models import  Product

class TestAutocompleteViews(TestCase):


    @classmethod
    def setUpTestData(cls):
        cls.url = reverse('autocomplete-ajax_auto')
        # Create product
        cls.prod = Product.objects.create(
            name = 'name_p1',
            category = 'cat1',
            image = 'https://static.openfoodfacts.org/images/products/761/303/624/9928/front_fr.177.400.jpg',
            link = 'https://fr.openfoodfacts.org/produit/7613036249928/eau-de-vittel',
            nutriscore = 'a' ,
            fat = 1, # g for 100g
            salt = 2, # g for 100g
            sugars = 3, # g for 100g
        )

    def test_ajax_auto_ajax(self):
        data = {
            'term':'name_p1',
        }
        json_data = json.dumps(data)
        response = self.client.get(
            self.url,
            json_data, 
            HTTP_X_REQUESTED_WITH='XMLHttpRequest'
        )
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.context['results'][0], self.prod)

