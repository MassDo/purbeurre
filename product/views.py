from django.shortcuts import render, get_object_or_404
from search.forms import FoodSearchForm
from product.models import Product


def product(request, prod_id=None):

    form_search = FoodSearchForm()
    product = get_object_or_404(Product, id=prod_id)

    return render(request, 'product/product.html', locals())
