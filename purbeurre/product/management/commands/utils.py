"""
    functions used in data_feed command
    In order to get data from OFF API into the 
    local database.
"""
import requests

def download_products(categorie):
    """
        get the rows products from a categorie 
        from the API in .json
        
    """
    api_payload = {
                    "action": "process",
                    "tagtype_0": "categories",
                    "tag_contains_0": "contains",
                    "tag_0": categorie,
                    "page_size": 25, # change here for more products by category
                    "json": 1
    }

    try:
        resp = requests.get("https://fr.openfoodfacts.org/cgi/search.pl?", params=api_payload).json()
        products_unchecked = resp["products"]    
        return products_unchecked
    except:
        print("Error whith api request")


def check_products(products, prod_keys, nutri_keys):
    """
        products is a list.

        delete product with incomplete fields from the products list
        and return a list of complete products.
        nutri_keys and prod_keys are 
    """
    products_checked = []     

    for prod in products:
        prod_checked = {} 
        product_is_complete = True

        for key1 in prod_keys:
            try:
                if key1 == "nutriments":
                    nut_checked = {}
                    nutriment_is_complete = True 

                    for key2 in nutri_keys:
                        try:                    
                            if prod[key1][key2] is not "":
                                nut_checked[key2] = prod[key1][key2]
                            else:
                                nutriment_is_complete = False
                                break
                        except:
                            nutriment_is_complete = False
                            break

                    if nutriment_is_complete:
                        prod_checked[key1] = nut_checked
                elif key1 is not "nutriment" and prod[key1] is not "":
                    prod_checked[key1] = prod[key1]
                else:
                    product_is_complete = False
                    break
            except:
                product_is_complete = False
                break

        if product_is_complete and nutriment_is_complete:
            products_checked.append(prod_checked)

    return products_checked


def formating_data(products):
    """
        this function is into a dict of one product.
        Merging the nutriment dict into product dict
        and deleting the nutriment key from product's keys.

        Example:
        
        >>> formating_data([\
        {"key0":1, "key1":2, "nutriments":{"key3":3, "key4":4}},\
        {"key0":1, "key1":2, "nutriments":{"key3":3, "key4":4}}])
        [{'key0': 1, 'key1': 2, 'key3': 3, 'key4': 4},\
 {'key0': 1, 'key1': 2, 'key3': 3, 'key4': 4}]

    """
    products_format = []
    for prod in products:
        for key in list(prod):
            if key is "nutriments":
                temp = prod[key]
                del prod[key]
                prod = {**prod, **temp}
                products_format.append(prod)
    return products_format