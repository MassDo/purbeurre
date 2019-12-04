from django.shortcuts import render
from search.forms import FoodSearchForm
from product.models import Product


def product(request, prod_id=None):

    form_search = FoodSearchForm()
    product = Product.objects.get(id=prod_id)    

    return render(request, 'product/product.html', locals())
