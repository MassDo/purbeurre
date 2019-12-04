from django.shortcuts import render
from product.models import Product
from search.forms import FoodSearchForm


def favorites(request):

    current_user = request.user
    context = dict(
        products = Product.objects.favorites_products(current_user),
        current_user = current_user,
        form_search = FoodSearchForm()
    )
    return render(request, 'favorites/favorites.html', context)