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
        # Get the products corresponding to the user input
        try:
            user_product = self.get(name=user_input)
            # list of better products
            if user_product:
                # Get the products of the user category set in order 
                prods_of_cat_ordered = self.filter(
                    category=user_product.category
                ).order_by(
                    'nutriscore',
                    'fat',
                    'sugars',
                    'salt',
                )
                # Create a better products list
                better_prod = []
                for prod in prods_of_cat_ordered:
                    if prod == user_product:
                        if len(better_prod) == 0:
                            print ('pas de meilleur produit')
                            return better_prod
                        else:
                            return better_prod
                    else:
                        better_prod.append(prod)
        except Product.DoesNotExist as err:
            print(f"The user input give no result {err}")
    
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