"""
    functions used in data_feed command
    In order to get data from OpenFoodFacts API into the 
    local database.
"""
import requests

def download_products(categorie, size):
    """
        get the rows products from a categorie 
        from the API in .json 
    """
    api_payload = {
                    "action": "process",
                    "tagtype_0": "categories",  
                    "tag_contains_0": "contains",
                    "tag_0": categorie,
                    "page_size": size, # change here for more products by category
                    "json": 1
    }
    try:
        response = requests.get("https://fr.openfoodfacts.org/cgi/search.pl?", params=api_payload)
        if response.status_code == 200:
            response = response.json()
            products_unchecked = response["products"]    
            return products_unchecked
        else:
            print(f'Bad response_status_code: {response.status_code} !')
    except requests.exceptions.RequestException as e:
        print(f"\nPlease check you internet connection ! \n\n {e}")


def check_products(products, prod_keys, nutri_keys):
    """
        products is a list.

        Delete product with incomplete fields from the products list
        and return a list of complete products with no duplicate product.
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
    # If duplicate products keep only one
    products_checked_unique = []
    known_prod_name = []
    for prod in products_checked:
        if prod["product_name"] not in known_prod_name:
            products_checked_unique.append(prod)
            known_prod_name.append(prod["product_name"])

    return products_checked_unique


def formatting_data(products):
    """
        Parameter products is a list of product(dict)
        This function is into each product of the parameter (products list),
        Merging the nutriment dict into product dict
        And deleting the nutriment key from product's keys.

        Example:
        
        >>> formating_data([{"key0":1, "key1":2, "nutriments":{"key3":3, "key4":4}}, {"key0":1, "key1":2, "nutriments":{"key3":3, "key4":4}}])
        [{'key0': 1, 'key1': 2, 'key3': 3, 'key4': 4}, {'key0': 1, 'key1': 2, 'key3': 3, 'key4': 4}]

    """
    products_format = []
    for prod in products:
        for key in list(prod):
            if key is "nutriments":
                temp_nutriments_dict = prod[key]
                del prod[key]
                prod = {**prod, **temp_nutriments_dict}
                products_format.append(prod)
                
    return products_format