from django.urls import path
from . import views 

urlpatterns = [
    path('', views.ajax_auto, name='autocomplete-ajax_auto'),
]