from django.shortcuts import render


def search(request):
    return render(request, 'search/search.html')

def results(request, var=None):
    return render(request, 'search/results.html')

def result2(request, var=None):
    return render(request, 'search/result2.html')

def result3(request, var=None):
    return render(request, 'search/result3.html')