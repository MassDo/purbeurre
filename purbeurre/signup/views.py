from django.shortcuts import render
from django.contrib import messages
# from django.contrib.auth import authenticate, login
from .forms import UserRegistrationForm


def signup(request):
    if request.method == 'POST':
            form = UserRegistrationForm(request.POST)
            if form.is_valid():
                form.save()
                username = form.cleaned_data.get('username')
                messages.success(request, f'{username}, your account has been created! You are now able to log in')
                return render(request, 'search/search.html')
    else:
        form = UserRegistrationForm()
    return render(request, 'signup/signup.html', {'form':form})