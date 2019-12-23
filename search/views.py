from django.shortcuts import render, redirect
from django.contrib import messages
from .forms import FoodSearchForm, FoodSearchFormMain
from product.models import Product


def search(request):
    """
        View linked to the home page
        for user_input
    """
    if request.method == 'POST':
        form_search = FoodSearchForm(request.POST)
        form_search_main = FoodSearchFormMain(request.POST) 
               
        if form_search.is_valid() and form_search.data.get('user_input'):
            user_input = form_search.cleaned_data.get('user_input')
            request.session['user_input'] = user_input

        elif form_search_main.is_valid() and form_search.data.get('main_form'):
            user_input = form_search_main.cleaned_data.get('main_form')
            request.session['user_input'] = user_input

        return redirect('search-results')

    else:
        form_search = FoodSearchForm()
        form_search_main = FoodSearchFormMain()

    return render(request, 'search/search.html',
        {'form_search':form_search, 'main_form':form_search_main}
    ) 

def results(request):
    """
        Views that display better products
        If the user is logged adding product to favorites is authorize.
    """
    form_search = FoodSearchForm()
    title = 'Résultats'
    user_input = request.session.get('user_input')
    user_prod = Product.objects.filter(name=user_input).first()
    best_prod = Product.objects.best_product(user_input)

    # if the user want to add a product
    if request.method == 'POST':        
        if request.user.is_authenticated:
            try:
                prod_id = request.POST.get('prod_id') 
                product = Product.objects.get(id=prod_id)
                current_user = request.user
                product.user.add(current_user)
                product.save()
                messages.success(request,'Produit ajouté à vos favoris !')
            except Product.DoesNotExist as err:
                print(f"Invalid product_id ERROR: {err}")
        else:
            messages.warning(request,'vous devez etre connecté pour enregistrer un aliment')
    elif best_prod:
        messages.success(request, 'Voici des aliments de comparables et de meilleurs qualité !')
    
    return render(request, 'search/results.html', locals())

