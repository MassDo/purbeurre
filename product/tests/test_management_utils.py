import unittest, requests
from unittest.mock import patch
from django.test import TestCase
from product.management.commands.utils import (
    download_products,
    check_products,
    formatting_data
)

# This function will be used by the mock to replace requests.get
def mocked_requests_get(*args, **kwargs):
    # mocking the requests.get
    class MockResponse:
        def __init__(self, json_data, status_code):
            self.json_data = json_data
            self.status_code = status_code

        def json(self):
            return self.json_data

    # Mock config scenario:
    # If correct uri and payload return 5 prod with different quality
    if (
        args[0] == 'https://fr.openfoodfacts.org/cgi/search.pl?' and
        kwargs['params'] == {
                    "action": "process",
                    "tagtype_0": "categories",  
                    "tag_contains_0": "contains",
                    "tag_0": 'tapas',
                    "page_size": 5, # change here for more products by category
                    "json": 1
        }):
        # Returning 5 prod with different quality: best to worst
        return MockResponse(
            {
                "products": [
                    {
                        "product_name":'test_prod_1',
                        "image_url":'test_im_url_1',
                        "url":'test_url_1',
                        "nutrition_grades":'a',
                        "nutriments":{
                            "sugars_100g":'1',
                            "salt_100g":'2',
                            "fat_100g":'3'
                        }
                    },
                    {
                        "product_name":'test_prod_2',
                        "image_url":'test_im_url_2',
                        "url":'test_url_2',
                        "nutrition_grades":'b',
                        "nutriments":{
                            "sugars_100g":'1',
                            "salt_100g":'2',
                            "fat_100g":'3'
                        }
                    },
                    {
                        "product_name":'test_prod_3',
                        "image_url":'test_im_url_3',
                        "url":'test_url_3',
                        "nutrition_grades":'b',
                        "nutriments":{
                            "sugars_100g":'2',
                            "salt_100g":'2',
                            "fat_100g":'3'
                        }
                    },
                    {
                        "product_name":'test_prod_4',
                        "image_url":'test_im_url_4',
                        "url":'test_url_4',
                        "nutrition_grades":'b',
                        "nutriments":{
                            "sugars_100g":'2',
                            "salt_100g":'3',
                            "fat_100g":'3'
                        }
                    },
                    {
                        "product_name":'test_prod_5',
                        "image_url":'test_im_url_5',
                        "url":'test_url_5',
                        "nutrition_grades":'b',
                        "nutriments":{
                            "sugars_100g":'2',
                            "salt_100g":'3',
                            "fat_100g":'4'
                        }
                    }
                ]
            },
            200
        )
    # If correct uri and payload returned empty json with 200 status
    elif (
        args[0] == 'https://fr.openfoodfacts.org/cgi/search.pl?' and
        kwargs['params'] == {
                    "action": "process",
                    "tagtype_0": "categories",  
                    "tag_contains_0": "contains",
                    "tag_0": 'tapas',
                    "page_size": 6, # change here for more products by category
                    "json": 1
        }):
        # Returning empty json
        return MockResponse(
            {
                "products": [
                ]
            },
            200
        )
    # If correct uri and payload but non existing category.
    elif (
        args[0] == 'https://fr.openfoodfacts.org/cgi/search.pl?' and
        kwargs['params'] == {
                    "action": "process",
                    "tagtype_0": "categories",  
                    "tag_contains_0": "contains",
                    "tag_0": 'non existing category',
                    "page_size": 5, # change here for more products by category
                    "json": 1
        }):
        # Returning empty json with 200 status
        return MockResponse(
            {
                "products": [
                ]
            },
            200
        )
    return MockResponse(None, 404)

# This function will be used by the mock to replace requests.get
def mocked_requests_get_connection_error(*args, **kwargs):
    raise requests.exceptions.RequestException


class TestUtils(TestCase):

    @classmethod
    def setUpTestData(cls):
        # Product keys
        cls.prod_keys = [           
            "product_name",
            "image_url",
            "url",
            "nutrition_grades",
            "nutriments",
        ]
        cls.nutri_keys = [
            "sugars_100g",
            "salt_100g",     # Sub-fields of "nutriments" api fields
            "fat_100g"
        ]
        # Payloads for request.get
        cls.api_payload_valid = {
            "action": "process",
            "tagtype_0": "categories",
            "tag_contains_0": "contains",
            "tag_0": "tapas",
            "page_size": 5, 
            "json": 1
        }
        # Valid products_unchecked list returned by download_products
        cls.products_unchecked = [
            {
                'product_name': 'test_prod_1', 
                'image_url': 'test_im_url_1', 
                'url': 'test_url_1', 
                'nutrition_grades': 'a', 
                'nutriments': {'sugars_100g': '1', 'salt_100g': '2', 'fat_100g': '3'}
            },
            {
                'product_name': 'test_prod_2', 
                'image_url': 'test_im_url_2', 
                'url': 'test_url_2', 
                'nutrition_grades': 'b', 
                'nutriments': {'sugars_100g': '1', 'salt_100g': '2', 'fat_100g': '3'}
            },
            {
                'product_name': 'test_prod_3', 
                'image_url': 'test_im_url_3', 
                'url': 'test_url_3', 
                'nutrition_grades': 'b', 
                'nutriments': {'sugars_100g': '2', 'salt_100g': '2', 'fat_100g': '3'}
            },
            {
                'product_name': 'test_prod_4', 
                'image_url': 'test_im_url_4', 
                'url': 'test_url_4', 
                'nutrition_grades': 'b', 
                'nutriments': {'sugars_100g': '2', 'salt_100g': '3', 'fat_100g': '3'}
            },
            {
                'product_name': 'test_prod_5', 
                'image_url': 'test_im_url_5', 
                'url': 'test_url_5', 
                'nutrition_grades': 'b', 
                'nutriments': {'sugars_100g': '2', 'salt_100g': '3', 'fat_100g': '4'}
            }
        ]
        # Valid products_unchecked liste return by download_products
        cls.products_unchecked_empty_value_and_duplicate = [
            {
                'product_name': 'test_prod_1', 
                'image_url': 'test_im_url_1', 
                'url': 'test_url_1', 
                'nutrition_grades': 'a', 
                'nutriments': {'sugars_100g': '1', 'salt_100g': '2', 'fat_100g': '3'}
            },
            {
                'product_name': 'test_prod_1',  # Duplicate product
                'image_url': 'test_im_url_1', 
                'url': 'test_url_1', 
                'nutrition_grades': 'a', 
                'nutriments': {'sugars_100g': '1', 'salt_100g': '2', 'fat_100g': '3'}
            },
            {
                'product_name': '', # Empty name
                'image_url': 'test_im_url_2', 
                'url': 'test_url_2', 
                'nutrition_grades': 'b', 
                'nutriments': {'sugars_100g': '1', 'salt_100g': '2', 'fat_100g': '3'}
            },
            {
                'product_name': 'test_prod_3', 
                'image_url': 'test_im_url_3', 
                'url': 'test_url_3', 
                'nutrition_grades': 'b', 
                'nutriments': {'sugars_100g': '2', 'salt_100g': '', 'fat_100g': '3'} # Empty salt_100g value
            },
            {
                'product_name': 'test_prod_4', 
                'image_url': 'test_im_url_4', 
                'url': 'test_url_4', 
                'nutrition_grades': 'b', 
                'nutriments': {'': '2', 'salt_100g': '', 'fat_100g': '3'} # Empty nytriment key sugars_100g
            },
            {
                '': 'test_prod_5', # Empty key
                'image_url': 'test_im_url_5', 
                'url': 'test_url_5', 
                'nutrition_grades': 'a', 
                'nutriments': {'sugars_100g': '1', 'salt_100g': '2', 'fat_100g': '3'}
            }
            
        ]
        # Result list after check_product
        cls.products_checked_empty_value = [
            {
                'product_name': 'test_prod_1', 
                'image_url': 'test_im_url_1', 
                'url': 'test_url_1', 
                'nutrition_grades': 'a', 
                'nutriments': {'sugars_100g': '1', 'salt_100g': '2', 'fat_100g': '3'}
            },
            {
                'product_name': 'test_prod_1',  # Duplicate product
                'image_url': 'test_im_url_1', 
                'url': 'test_url_1', 
                'nutrition_grades': 'a', 
                'nutriments': {'sugars_100g': '1', 'salt_100g': '2', 'fat_100g': '3'}
            },
        ]
        # Result list after formatting_data
        cls.products_formatted= [
            {
                'product_name': 'test_prod_1', 
                'image_url': 'test_im_url_1', 
                'url': 'test_url_1', 
                'nutrition_grades': 'a', 
                'sugars_100g': '1',
                'salt_100g': '2',
                'fat_100g': '3'
            },
            {
                'product_name': 'test_prod_1', 
                'image_url': 'test_im_url_1', 
                'url': 'test_url_1', 
                'nutrition_grades': 'a', 
                'sugars_100g': '1',
                'salt_100g': '2',
                'fat_100g': '3'
            }
        ]

    @patch(
        'product.management.commands.utils.requests.get',
        side_effect=mocked_requests_get
    )
    def test_download_products(self, mock_get):
        """
            Mock request.get with VALID json response:
                * Test if download_prod get correct prod list with valid API Url
                * Test that download_products parameters are transmitted correctly
                * Test that None are returned if bad parameters.                  
        """
        prod_returned = download_products('tapas', 5)
        # Test if the correct uri is called and
        # If correct payload is transmitted
        mock_get.assert_called_with(
            "https://fr.openfoodfacts.org/cgi/search.pl?",
            params=self.api_payload_valid
        )
        # Test that the prod_returned from api request is ok
        self.assertEqual(prod_returned, self.products_unchecked)
        # Test that the number of products is corresponding to the argument given (5 here)
        self.assertEqual(len(prod_returned[1]), 5)
        # Test download product with bad URI return None
        self.assertEqual(download_products('bad_uri', 5), None)

    @patch(
        'product.management.commands.utils.requests.get',
        side_effect=mocked_requests_get_connection_error
    )
    def test_download_products_internet_break(self, mock_get):
        """
            Mock request.get with 'internet failure' error:
                * Test the exception is raised
        """
        self.assertRaises(
            requests.exceptions.RequestException,
            download_products('uri', 5)
        )

    def test_check_products(self):
        """
            Test the  partially empty products are removed
            and that check_products return list of lists.
        """
        prod_check = check_products(
            self.products_unchecked_empty_value_and_duplicate,
            self.prod_keys,
            self.nutri_keys
        )
        self.assertEqual(
            prod_check,
            self.products_checked_empty_value
        )

    def test_formating_data(self):
        product_formatted = formatting_data(
            self.products_checked_empty_value
        )
        self.assertEqual(product_formatted, self.products_formatted)
        

