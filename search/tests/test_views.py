from django.test import TestCase
from django.db import models
from django.urls import reverse
from users.models import CustomUser
from product.models import Product
from search.forms import FoodSearchForm, FoodSearchFormMain


class TestViews(TestCase):

    @classmethod
    def setUpTestData(cls):
        # User 
        cls.user = CustomUser.objects.create_user(
            email='testuser@testuser.com',
            username='testuser',
            password='Testuser123'
        )
        # Path
        cls.search_url = reverse('search-search')
        cls.results_url = reverse('search-results')
        # Form transmitted
        cls.form = FoodSearchForm()
        cls.prod_1 = Product.objects.create(
            name = 'name_p1',
            category = 'cat1',
            image = 'https://static.openfoodfacts.org/images/products/761/303/624/9928/front_fr.177.400.jpg',
            link = 'https://fr.openfoodfacts.org/produit/7613036249928/eau-de-vittel',
            nutriscore = 'a' ,
            fat = 1, # g for 100g
            salt = 2, # g for 100g
            sugars = 3, # g for 100g
        )

    def test_search_get(self):
        response = self.client.get(self.search_url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'search/search.html')
        self.assertEqual(type(response.context['form_search']), FoodSearchForm)
        self.assertEqual(type(response.context['main_form']), FoodSearchFormMain)

    def test_search_post_food_search_form(self):
        data = {
            'user_input': 'test'
        }
        response = self.client.post(self.search_url, data)
        self.assertRedirects(
            response,
            self.results_url,
            302,
            200,
            msg_prefix='',
            fetch_redirect_response=True
        )

    def test_search_post_food_search_form_main(self):

        data = {
            'main_form': 'test'
        }
        response = self.client.post(self.search_url, data)
        self.assertRedirects(
            response,
            self.results_url,
            302,
            200,
            msg_prefix='',
            fetch_redirect_response=True
        )
    
    def test_results_post_logout(self):
        response = self.client.post(self.results_url, {'prod_id': 23})
        message = list(response.context['messages'])
        self.assertEqual(len(message), 1)
        self.assertEqual(str(message[0]), 'vous devez etre connecté pour enregistrer un aliment...')

    def test_results_post_logged_prod_id_invalid(self):
        self.client.login(
            email='testuser@testuser.com',
            password='Testuser123'
        )
        with self.assertRaises(Product.DoesNotExist):
            response = self.client.post(self.results_url, {'prod_id': 1})
            prod_id = response.context['prod_id']
            product_find = Product.objects.get(name=prod_id)
            
    def test_results_post_logged_prod_id_valid(self):
        self.client.login(
            email='testuser@testuser.com',
            password='Testuser123'
        )
        prod_id = self.prod_1.id
        response = self.client.post(self.results_url, {'prod_id': prod_id})
        prod_id_recover = response.context['prod_id']
        product_find = Product.objects.get(id=prod_id_recover)
        product_find.user.add(self.user)
        message = list(response.context['messages'])
        self.assertEqual(len(message), 1)
        self.assertEqual(str(message[0]), 'Produit ajouté à vos favoris !')
        self.assertEqual(product_find, self.prod_1)
    