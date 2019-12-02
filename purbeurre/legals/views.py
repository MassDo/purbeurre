from django.shortcuts import render
from search.forms import FoodSearchForm

def legals(request):
    """
        views of the legals mentions
    """

    form_search = FoodSearchForm()

    return render(request, 'legals/legals.html', locals())