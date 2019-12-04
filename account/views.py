from django.shortcuts import render
from search.forms import FoodSearchForm


def account(request):
    """
        view of the user account
    """

    username = request.user.username
    email = request.user.email

    context = dict(
        username = username,
        email = email,
        form_search = FoodSearchForm()
    )

    return render(request, 'account/account.html', context)