from django.test import SimpleTestCase
from django.urls import resolve, reverse
from product.views import product


class TestUrls(SimpleTestCase):

    def test_product_name_is_reversed_and_resolved_with_argument(self):
        """
            Check if the name of url is linked to the
            correct path. And if the correct template is returned
        """
        url = reverse('product-product', kwargs={'prod_id':1})
        # Test name linked to url
        self.assertEqual(resolve(url).view_name, 'product-product')
        # Test url linked to the correct view function
        self.assertEqual(resolve(url).func, product)
