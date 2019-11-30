from django.shortcuts import render

def product(request, prod_id=None):
    return render(request, 'product/product.html')
