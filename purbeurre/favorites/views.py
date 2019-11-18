from django.shortcuts import render

def favorites(request):
    """
        views of the products saved by the user
    """
    return render(request, 'favorites/favorites.html')