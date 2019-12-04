from django.urls import path
from . import views

urlpatterns = [
    path('<int:prod_id>', views.product, name='product-product'),
]