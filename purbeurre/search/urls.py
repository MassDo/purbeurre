from django.urls import path
from . import views

urlpatterns = [
    path('', views.search, name='search-search'),
    path('results', views.results, name='search-results'),
    path('result2', views.result2, name='search-result2'),
    path('result3', views.result3, name='search-result3'),
]