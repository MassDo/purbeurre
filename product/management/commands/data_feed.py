
from django.core.management.base import BaseCommand, CommandError
from .utils import download_products,check_products, formating_data
from product.models import Product

class Command(BaseCommand):
    """
        New command to implement the local database with products from
        OpenFoodFacts API. The products are download from the categories list
        into the folowing handle method. Use "python manage.py data_feed" or
        "./manage.py data_feed" to launch the script.
    """
    help = '''data_feed implement the database 
    with checked products from OpenfoodFacts API'''

    def handle(self, *args, **options):
        categories = [
            'tapas', 
            'olives',
            'Boissons',
            'Viandes'
        ]
        prod_keys = [           
            "product_name",
            "image_url",
            "url",
            "nutrition_grades",
            "nutriments"
        ]
        nutri_keys = [
            "sugars_100g",
            "salt_100g",     # Sub-fields of "nutriments" api fields
            "fat_100g"
        ]
        for cat in categories:
            # Download data from OpenFoodFacts API
            raw_data = download_products(cat, 25)
            # Delete incomplete, empty set or duplicate product
            data_checked = check_products(raw_data, prod_keys, nutri_keys)
            # Formating
            final_data = formating_data(data_checked)
            # Create the product object into local database
            for prod in final_data:
                Product.objects.create(
                    name = prod['product_name'],
                    category = cat,
                    image = prod['image_url'],
                    link = prod['url'],
                    nutriscore = prod['nutrition_grades'],
                    fat = prod['fat_100g'],
                    salt = prod['salt_100g'],
                    sugars = prod['sugars_100g'],
                )
            


        