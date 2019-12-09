from django.urls import reverse, resolve


def test_product_url():
    """
        test if url is given from view name and parameter,
        and if view name is resolve from this url.
    """
    path = reverse('product-product', kwargs={'prod_id':1})
    assert resolve(path).view_name == 'product-product'