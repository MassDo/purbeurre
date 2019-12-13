
from django.core.management.base import BaseCommand, CommandError
from .utils import download_products,check_products, formating_data
from product.models import Product

class Command(BaseCommand):
    help = 'ma nouvelle commande'

    # def add_arguments(self, parser):
    #     parser.add_argument('poll_ids', nargs='+', type=int)

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
            "salt_100g",     # sub-fields of "nutriments" api fields
            "fat_100g"
        ]
        for cat in categories:
            # download data
            raw_data = download_products(cat)
            # delete incomplete or empty set or duplicate product
            data_checked = check_products(raw_data, prod_keys, nutri_keys)
            # formating
            final_data = formating_data(data_checked)
            # [{'key0': 1, 'key1': 2 },{'key0': 1, 'key1': 2}]
            for prod in final_data:
                # creer les lignes de la table
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
            


        