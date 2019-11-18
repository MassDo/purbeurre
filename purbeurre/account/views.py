from django.shortcuts import render

# Create your views here.
def account(request):
    """
        view of the user account
    """
    return render(request, 'account/account.html')