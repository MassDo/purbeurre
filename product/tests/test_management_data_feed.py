from io import StringIO
from django.test import TestCase
from django.core.management import call_command
from unittest.mock import patch
from product.tests.test_management_utils import(
    mocked_requests_get, 
    mocked_requests_get_connection_error
)
from product.management.commands import data_feed
from product.management.commands.utils import(
    download_products, 
    check_products, 
    formatting_data
)

class TestDataFeedCustomCommand(TestCase):
    """
        Tests of the custom command 'data_feed'
    """
    @classmethod
    def setUpTestData(cls):
        cls.categories = [
            'tapas', 
            'olives',
            'Boissons',
            'Viandes'
        ]
        cls.prod_keys = [           
            "product_name",
            "image_url",
            "url",
            "nutrition_grades",
            "nutriments"
        ]
        cls.nutri_keys = [
            "sugars_100g",
            "salt_100g",     # Sub-fields of "nutriments" api fields
            "fat_100g"
        ]

    @patch(
        'product.management.commands.utils.requests.get',
        side_effect=mocked_requests_get
    )
    def test_data_feed(self, mock_get):
        out = StringIO()
        call_command('data_feed', 'tapas', prod=[5], stdout=out)
        self.assertIn(
            '\x1b[31mPlease wait ...\x1b[0m\n\x1b[33;1mCategory: tapas \t Product implemented: test_prod_1\x1b[0m\n\x1b[33;1mCategory: tapas \t Product implemented: test_prod_2\x1b[0m\n\x1b[33;1mCategory: tapas \t Product implemented: test_prod_3\x1b[0m\n\x1b[33;1mCategory: tapas \t Product implemented: test_prod_4\x1b[0m\n\x1b[33;1mCategory: tapas \t Product implemented: test_prod_5\x1b[0m\n\x1b[32;1m\nSuccessfully implement database with products from categorie tapas\n\x1b[0m\n\x1b[33;1m\n\t*****\tFINAL REPORT\t*****\n\x1b[0m\n\x1b[32;1m\nThe following gategories are valids in OpenFoodFact database:\n\x1b[0m\n\x1b[32;1m\tCategory: tapas || Total valids products implemented: 5/5, rejected products:0\x1b[0m\n',
            out.getvalue()
        )
        # out.seek(0)
        # print('lines == > ', out.readlines())
        out.close()




