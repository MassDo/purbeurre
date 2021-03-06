from django.test import TestCase
from django.db.models.query import QuerySet
from product.models import Product, ProductManager
from users.models import CustomUser

class TestProduct(TestCase):

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
            name = 'name_p3',
            category = 'cat1',
            image = 'https://static.openfoodfacts.org/images/products/761/303/624/9928/front_fr.177.400.jpg',
            link = 'https://fr.openfoodfacts.org/produit/7613036249928/eau-de-vittel',
            nutriscore = 'b' ,
            fat = 2, # g for 100g
            salt = 2, # g for 100g
            sugars = 3, # g for 100g
        )
        cls.prod_4 = Product.objects.create(
            name = 'name_p4',
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
        cls.products_A = [
            cls.prod_1, 
            cls.prod_2, 
            cls.prod_3,
        ]
        # TEST USERS
        # User_1 favorites ==> all products
        cls.user_1 = CustomUser.objects.create_user(username='name_u1')
        # User_1 favorites ==> 0 products
        cls.user_2 = CustomUser.objects.create_user(
            username='name_u2',
            email='email2@email2.com'
        )
        # User_1 have all the products in favorites.
        for prod in cls.products:
            prod.user.add(cls.user_1)

    def test_product_manager(self):
        """
            Test that the custom manager class 'ProductManager',
            is called by 'objects' attribute
        """
        prod_man = Product.objects
        self.assertTrue(isinstance(prod_man, ProductManager))

    def test_product_str(self):
        self.assertEqual(self.prod_1.__str__(), self.prod_1.name)

    def test_product_creation(self):
        self.assertTrue(isinstance(self.prod_1, Product))

    def test_product_att_name(self):
        prod = Product.objects.get(name="name_p1")
        self.assertEqual('name_p1', prod.name)

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
        # Test if the objects into the QuerySet are correct for user_1
        fav_prod = []
        for prod in Product.objects.favorites_products(self.user_1):
            fav_prod.append(prod)
        self.assertEqual(self.products, fav_prod)
        # Test if the objects of the QuerySet are correct for user_2
        fav_prod = []
        for prod in Product.objects.favorites_products(self.user_1):
            fav_prod.append(prod)
        self.assertEqual(self.products, fav_prod)
    
    def test_favorites_products_user_no_products_return_empty_queryset(self):
        self.assertEqual(
            Product.objects.favorites_products(self.user_2).count(),
            0
        )

    def test_best_product(self):
        best = Product.objects.best_product('name_p4')
        self.assertEqual(best, self.products_A)

    def test_best_product_no_product(self):
        self.assertRaises(
            Product.DoesNotExist, 
            Product.objects.best_product('incorrect name for prod')
        )

    def test_best_product_no_better_prod(self):
        self.assertEqual(
            Product.objects.best_product(self.prod_1.name),
            []
        )
