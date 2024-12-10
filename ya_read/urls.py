from django.urls import path
from .views import my_homepage,chicken

urlpatterns = [
    path('chicken/', chicken),
    path('', my_homepage),
]
