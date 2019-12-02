from django.shortcuts import render
from search.forms import FoodSearchForm


def product(request, prod_id=None):

    form_search = FoodSearchForm()

    return render(request, 'product/product.html', locals())
