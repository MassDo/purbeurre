from io import StringIO
from django.test import TestCase
from django.core.management import call_command
from unittest.mock import patch
from product.tests.test_management_utils import mocked_requests_get
from product.management.commands import data_feed


class TestDataFeedCustomCommand(TestCase):
    """
        Tests of the custom command 'data_feed'
    """
    @classmethod
    def setUpTestData(cls):
        # cls.categories = [
        #     'tapas', 
        #     'olives',
        #     'Boissons',
        #     'Viandes'
        # ]
        # cls.prod_keys = [           
        #     "product_name",
        #     "image_url",
        #     "url",
        #     "nutrition_grades",
        #     "nutriments"
        # ]
        # cls.nutri_keys = [
        #     "sugars_100g",
        #     "salt_100g",     # Sub-fields of "nutriments" api fields
        #     "fat_100g"
        # ]
        pass

    @patch(
        'product.management.commands.utils.requests.get',
        side_effect=mocked_requests_get
    )
    def test_data_feed_valid_category_and_products(self, mock_get):
        """
            Get the stdout as str, parsed it, and test if,
            the products added, are the same that the valid one,
            given by the mocked request.get.json response,
            (for ('tapas',5) as arguments).
        """
        buff = StringIO()
        call_command('data_feed', 'tapas', prod=[5], stdout=buff)
        stdout_str = buff.getvalue()
        print(stdout_str)
        # Parse the stdout_str and check the report ?
        self.assertIn('Category: tapas 	 Product implemented: test_prod_1', stdout_str)
        self.assertIn('Category: tapas 	 Product implemented: test_prod_2', stdout_str)
        self.assertIn('Category: tapas 	 Product implemented: test_prod_3', stdout_str)
        self.assertIn('Category: tapas 	 Product implemented: test_prod_4', stdout_str)
        self.assertIn('Category: tapas 	 Product implemented: test_prod_5', stdout_str)
        self.assertIn('Total valids products implemented: 5/5, rejected products:0', stdout_str)

    @patch(
        'product.management.commands.utils.requests.get',
        side_effect=mocked_requests_get
    )
    def test_data_feed_invalid_category(self, mock_get):
        buff = StringIO()
        call_command('data_feed', 'non existing category', prod=[5], stdout=buff)
        stdout_str = buff.getvalue()
        self.assertIn("The category non existing category doesn't exist in the OpenFoodFact database", stdout_str)







