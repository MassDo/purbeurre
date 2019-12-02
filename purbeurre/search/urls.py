from django.urls import path
from . import views

urlpatterns = [
    path('', views.search, name='search-search'),
    path('results/', views.results, name='search-results'),
]