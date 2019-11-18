from django.shortcuts import render


def legals(request):
    """
        views of the legals mentions
    """

    return render(request, 'legals/legals.html')