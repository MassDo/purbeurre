from django.shortcuts import render



def account(request):
    """
        view of the user account
    """

    username = request.user.username
    email = request.user.email

    context = dict(
        username = username,
        email = email
    )

    return render(request, 'account/account.html', context)