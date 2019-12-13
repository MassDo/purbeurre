from django.test import TestCase
from django.db.models.query import QuerySet
from product.models import Product
from users.models import CustomUser

class TestModels(TestCase):

    @classmethod
    def setUpTestData(cls):
        # Test products instantiation
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
        cls.prod_2 = Product.objects.create(
            name = 'name_p2',
            category = 'cat1',
            image = 'https://static.openfoodfacts.org/images/products/761/303/624/9928/front_fr.177.400.jpg',
            link = 'https://fr.openfoodfacts.org/produit/7613036249928/eau-de-vittel',
            nutriscore = 'a' ,
            fat = 2, # g for 100g
            salt = 2, # g for 100g
            sugars = 3, # g for 100g
        )
        cls.prod_3 = Product.objects.create(
            name = 'name_p2',
            category = 'cat1',
            image = 'https://static.openfoodfacts.org/images/products/761/303/624/9928/front_fr.177.400.jpg',
            link = 'https://fr.openfoodfacts.org/produit/7613036249928/eau-de-vittel',
            nutriscore = 'b' ,
            fat = 2, # g for 100g
            salt = 2, # g for 100g
            sugars = 3, # g for 100g
        )
        cls.prod_4 = Product.objects.create(
            name = 'name_p2',
            category = 'cat1',
            image = 'https://static.openfoodfacts.org/images/products/761/303/624/9928/front_fr.177.400.jpg',
            link = 'https://fr.openfoodfacts.org/produit/7613036249928/eau-de-vittel',
            nutriscore = 'b' ,
            fat = 3, # g for 100g
            salt = 2, # g for 100g
            sugars = 3, # g for 100g
        )
        cls.products = [
            cls.prod_1, 
            cls.prod_2, 
            cls.prod_3,
            cls.prod_4
        ]
        # User_1 favorites ==> all products
        cls.user_1 = CustomUser.objects.create_user(username='name_u1')
        # User_1 favorites ==> 0 products
        cls.user_2 = CustomUser.objects.create_user(
            username='name_u2',
            email='email2@email2.com'
        )
        # cls.user_3 = CustomUser.objects.create_user(username='name_u3')
        # Relation between product and user
        for prod in cls.products:
            # The user_1 has all the products in favorites
            prod.user.add(cls.user_1)

    def test_favorites_products_return_correct_queryset(self):
        """
            Serie of test with correct user and product associated to him.
        """
        # Test if QuerySet object is returned.
        self.assertTrue(
            isinstance(
                Product.objects.favorites_products(self.user_1),
                QuerySet
            )
        )
        # Test if the objects of the QuerySet are correct
        fav_prod = []
        for prod in Product.objects.favorites_products(self.user_1):
            fav_prod.append(prod)
        self.assertEqual(self.products, fav_prod)
    
    def test_favorites_products_user_no_products_return_empty_queryset(self):
        self.assertEqual(
            Product.objects.favorites_products(self.user_2).count(),
            0
        )

    def test_best_product_no_user_arg(self):

# Tester les méthodes du Manager
    # Si la BDD est vide
    # Si la BDD est implémentée
        # tester la méthode favorites_products
            # si pas d'utilisateur fournie en args
            # Si utilisateur qui n'est associé a aucun produits
            # Si utilisateur associé à des produits
        # Tester la méthode best_products
            # si args incorrect ou abscents
            # si arg ok
                # si le prod est déja le meilleur
                # si le produit n'est pas le meilleur