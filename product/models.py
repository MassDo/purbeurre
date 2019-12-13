from django.db import models
from users.models import CustomUser


class ProductManager(models.Manager):
    """
        Method used for operations at the "table" scale
    """

    def best_product(self, user_input):
        """
            return the best product list
            from the user input (product name)
        """
        # get the products corresponding to the user input
        # if there is multiple products for the same name it gives the worst product
        user_product = self.filter(name=user_input).last()
    
        # list of better products
        if user_product:
            # get the products of the category set in order 
            try:
                cat_ordered = self.filter(
                    category=user_product.category
                ).order_by(
                    'nutriscore',
                    'fat',
                    'sugars',
                    'salt',
                )
            except:
                print('erreur dans la requete de filtre de categorie et de trie')
            # adding better products to the list
            better_prod = []
            for prod in cat_ordered:
                if prod == user_product:
                    if len(better_prod) == 0:
                        print ('pas de meilleur produit')
                        return better_prod
                    else:
                        return better_prod
                else:
                    better_prod.append(prod)
        else:
            print('pas de produit')
    
    def favorites_products(self, user_logged):
        """
            Manager method that return the 
            query set of the favorites products of a user
        """

        fav = Product.objects.filter(user=user_logged)
        return fav
        

class Product(models.Model):
    """
        class representing the Product table
    """
    # Manager
    objects = ProductManager()
    # Attributes
    name = models.CharField(max_length=100)
    category = models.CharField(max_length=100)
    image = models.URLField(max_length=200)
    link = models.URLField(max_length=200) 
    nutriscore = models.CharField(max_length=50)  
    fat = models.FloatField() # g for 100g
    salt = models.FloatField() # g for 100g
    sugars = models.FloatField() # g for 100g
    user = models.ManyToManyField(CustomUser)
    
    class Meta:
        ordering = ['category', 'nutriscore', 'fat', 'sugars', 'salt']
    
    def __str__(self):
        return self.name