from django.shortcuts import render, redirect
from .forms import FoodSearchForm
from product.models import Product
from django.contrib.auth.decorators import login_required


def search(request):
    if request.method == 'POST':
        form = FoodSearchForm(request.POST)
        if form.is_valid():
            user_input = form.cleaned_data.get('user_input')
            # vérifier que user_input est bien un produit
            # return temporaire
            # il faut retourner dans l'url de about user_input 
            return redirect('search-result', user_input=user_input)
    else:
        form = FoodSearchForm()
    return render(request, 'search/search.html', {'form':form}) 

def results(request, var=None):
    return render(request, 'search/results.html')
