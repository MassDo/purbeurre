from django.test import TestCase, Client
from django.db import models
from django.urls import reverse
from users.models import CustomUser
from product.models import Product
from search.forms import FoodSearchForm

class TestViews(TestCase):

    def setUp(self):
        # User 
        self.user = CustomUser.objects.create_user(
            email='testuser@testuser.com',
            username='testuser',
            password='Testuser123'
        )
        # Client
        self.c = Client()
        # Path
        self.favorites_url = reverse('favorites-favorites')
        # Form transmitted
        self.form = FoodSearchForm()
        
    def test_favorites_redirect_to_login_if_user_not_logged(self):        
        response = self.c.get(self.favorites_url)
        # test acces denial and redirect status
        self.assertEqual(response.status_code, 302)
        # test redirect to login then to account
        self.assertEqual(response.url, reverse('login') + '?next=/favorites/')

    def test_favorites_template_if_user_is_logged(self):  
        # User login     
        login = self.c.login(
            email='testuser@testuser.com',
            password='Testuser123'
        )
        response = self.c.get(self.favorites_url)

        # Test response status and correct template return
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'favorites/favorites.html')

    def test_favorites_context_attribute_exists_with_no_product(self):  
        login = self.c.login(
            email='testuser@testuser.com',
            password='Testuser123'
        )
        response = self.c.get(self.favorites_url)
        context = dict(
            products = response.context['products'],
            current_user = response.context['current_user'],
            form_search = response.context['form_search']
        )
        # Test if the queryset for empty prod database exists and is empty
        self.assertEqual(context['products'].count(), 0)
        # Test if the current user in the context is the user logged
        self.assertEqual(context['current_user'], self.user)
        # Test if form in context is an instanciation of FoodSearchForm()
        self.assertEqual(type(context['form_search']), type(self.form))
        # Test if the message send is unique (for no products)
        self.assertEqual(len(list(response.context.get('messages'))), 1)
        # Test if the message send is correct (for no products)
        self.assertEqual(str(list(response.context.get('messages'))[0]), 'vos favoris sont vides')

    def test_favorites_context_attribute_with_products(self):
        # Product creation
        product = Product.objects.create(
            name = 'test_prod_name',
            category = 'test_prod_cat',
            image = 'https://static.openfoodfacts.org/images/products/761/303/624/9928/front_fr.177.400.jpg',
            link = 'https://fr.openfoodfacts.org/produit/7613036249928/eau-de-vittel',
            nutriscore = 'a',    
            fat = 0.0,
            salt = 0.0,
            sugars = 0.0,
        )
        # Association product with his user
        product.user.add(self.user)
        # Client with user logged
        login = self.c.login(
            email='testuser@testuser.com',
            password='Testuser123'
        )
        response = self.c.get(self.favorites_url)
        # Test if through view context the product(s) of the user is given
        self.assertEqual(response.context['products'].first(), product)
        # Test if the message send is unique (for no products)
        self.assertEqual(len(list(response.context.get('messages'))), 1)
        # Test if the message send is correct (for no products)
        self.assertEqual(str(list(response.context.get('messages'))[0]), 'Voici vos aliments déja enregistrés.')


