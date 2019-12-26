
from django.core.management.base import BaseCommand
from .utils import download_products, check_products, formatting_data, del_duplicate
from product.models import Product

class Command(BaseCommand):
    """
        New command to implement the local database with products from
        OpenFoodFacts API. The products are download from the categories given
        as arguments to the command like the following exemple
        "python manage.py data_feed cat_1 cat_2 ... cat_n"

        The products attributes (prod_keys) use for checking data, cannot be changed,
        into the command line. They are set as handle method attributes.

        The report attr of the handle method is used for,
        console prompt report, and the tests.
    """
    help = 'Custom command that implement database from OpenFoodFact API product'

    def add_arguments(self, parser):
        # Positional arguments
        parser.add_argument(
            'categories', 
            nargs='+', 
            type=str, 
            help="Categorie of the OpenFoodFacts API products"
        )
        parser.add_argument(
            '--prod', 
            nargs='+', 
            type=int, 
            help="Number of product by category to download"
        )

    def handle(self, *args, **options):
        report = {}
        good_cat = {}
        bad_cat = []
        size_by_cat = options['prod']
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
        if size_by_cat:
            if size_by_cat[0] > 250: # Product seach size limitation
                size_by_cat = [250]
        else:
            size_by_cat = [5] # if no size given by command call
        products_all_categories_unchecked = []
        for cat in options['categories']:
            real_prod_implemented_by_cat = 0
            self.stdout.write(
                    self.style.NOTICE(
                        f'Please wait ...'
                    )
                )
            # Download data from OpenFoodFacts API
            size = size_by_cat[0]
            raw_data = download_products(cat, size)
            # Delete incomplete, or empty set into category
            data_checked = check_products(
                raw_data, 
                prod_keys, 
                nutri_keys
            )
            # Formating dict of nutriments
            final_data = formatting_data(data_checked)
            # Delete duplicate
            final_data = del_duplicate(final_data)
            # Adding cat to each product dict
            for prod in final_data:
                prod.update({"category":cat})
            products_all_categories_unchecked += final_data
            # Create prompt messages
            for prod in final_data:
                real_prod_implemented_by_cat += 1
                prod_name = prod['product_name']
                self.stdout.write(
                    self.style.WARNING(
                        f'Category: {cat} \t Product implemented: {prod_name}'
                    )
                )
            # SUCCES message if products are implemented from the cat
            if final_data:
                self.stdout.write(
                    self.style.SUCCESS(
                        f'\nSuccessfully implement database with products from categorie {cat}\n'
                    )
                )
                good_cat[cat] = real_prod_implemented_by_cat
            # ERROR message for bad cat input
            else:
                self.stdout.write(
                    self.style.ERROR(
                        f"\nThe category {cat} doesn't exist in the OpenFoodFact database\n"
                    )
                )
                bad_cat.append(cat)

        # Delete duplicates products from crossover categories
        products_all_categories_checked = del_duplicate(
            products_all_categories_unchecked
        )
        # Create products into local database
        for prod in products_all_categories_checked:
            Product.objects.create(
                name = prod['product_name'].lower(),
                category = prod['category'],
                image = prod['image_url'],
                link = prod['url'],
                nutriscore = prod['nutrition_grades'],
                fat = prod['fat_100g'],
                salt = prod['salt_100g'],
                sugars = prod['sugars_100g'],
            )
        # Final Report
        report['valid categories'] = good_cat
        report['incorrect'] = bad_cat
        self.stdout.write(
            self.style.WARNING(
                f'\n\t*****\tFINAL REPORT\t*****\n'
            ),
        )
        self.stdout.write(
            self.style.SUCCESS(
                f"\nThe following gategories are valids in OpenFoodFact database:\n"
            ),
        )
        for cat, prod in good_cat.items():
            self.stdout.write(
                self.style.SUCCESS(
                    f'\tCategory: {cat} || Total valids products implemented: {prod}/{size_by_cat[0]}, rejected products:{size_by_cat[0] - prod}'
                ),
            )
        if bad_cat:
            self.stdout.write(
                self.style.ERROR(
                    f"\nThe following gategories doesn't exist in OpenFoodFact database:\n"
                ),
            )
            for cat in bad_cat:
                self.stdout.write(
                    self.style.ERROR(
                        f'\t{cat}'
                    ),
                )

            


        