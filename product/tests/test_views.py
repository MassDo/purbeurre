from django.test import TestCase, Client
from django.urls import reverse
from search.forms import FoodSearchForm
from product.models import Product


class TestViews(TestCase):

    @classmethod
    def setUpTestData(cls):
        # Set up data fonce for all the tests of TestViews
        # Product creation
        cls.product = Product.objects.create(
            name = 'test_prod_name',
            category = 'test_prod_cat',
            image = 'https://static.openfoodfacts.org/images/products/761/303/624/9928/front_fr.177.400.jpg',
            link = 'https://fr.openfoodfacts.org/produit/7613036249928/eau-de-vittel',
            nutriscore = 'a',    
            fat = 0.0,
            salt = 0.0,
            sugars = 0.0,
        )
        cls.prod_id = cls.product.id
        # Client
        cls.c = Client()
        # Path woth correct prod_id
        cls.url_data = reverse('product-product', kwargs={'prod_id':cls.prod_id})    
        
    def test_product_template(self):
        response = self.c.get(self.url_data)
        # Test response status and correct template return
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'product/product.html') 

    def test_product_view_context_valid_if_correct_argument_id(self):
        response = self.c.get(self.url_data)
        # Test if through view context the product object is given
        self.assertEqual(response.context['product'], self.product)

    def test_product_ERR_404_if_incorrect_argument_prod_id(self):
        # prod_id = 2 doesn't exist in database
        product_url = reverse('product-product', kwargs={'prod_id':9999999})
        response = self.c.get(product_url)
        self.assertEqual(response.status_code, 404)
        