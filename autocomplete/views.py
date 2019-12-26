import json
from django.shortcuts import render
from django.http import HttpResponse
from product.models import Product


def ajax_auto(request):
    """
        View returning names of the researched product (.json)
        via ajax request.
    """
    data = 'fail'
    if request.is_ajax():
        q = request.GET.get('term', '').lower()
        products = Product.objects.filter(name__icontains=q)
        results = []
        for prod in products:
            prod_json = {}
            prod_json = prod.name
            results.append(prod_json)
            data = json.dumps(results)
    mimetype = 'application/json'
    return HttpResponse(data, mimetype)