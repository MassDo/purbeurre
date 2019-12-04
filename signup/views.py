from django.shortcuts import render
from django.contrib import messages
from .forms import UserRegistrationForm
from search.forms import FoodSearchForm


def signup(request):

    form_search = FoodSearchForm()
    if request.method == 'POST':
            reg_form = UserRegistrationForm(request.POST)
            if reg_form.is_valid():
                reg_form.save()
                username = reg_form.cleaned_data.get('username')
                messages.success(request, f'{username}, your account has been created! You are now able to log in')
                return render(request, 'search/search.html', locals()) 
    else:
        reg_form = UserRegistrationForm()
    return render(request, 'signup/signup.html', locals())