from django.urls import path
from . import views

urlpatterns = [
    path('', views.legals, name='legals-legals')
]