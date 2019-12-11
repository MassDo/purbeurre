from django.shortcuts import render
from django.contrib import messages
from product.models import Product
from search.forms import FoodSearchForm


def favorites(request):

    current_user = request.user
    products = Product.objects.favorites_products(current_user)
    context = dict(
        products = products,
        current_user = current_user,
        form_search = FoodSearchForm()
    )
    if not products:
        messages.warning(request, 'vos favoris sont vides')
    else:
        messages.success(request,'Voici vos aliments déja enregistrés.')
        print("hello")
    return render(request, 'favorites/favorites.html', context)