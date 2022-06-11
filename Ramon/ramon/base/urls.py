from django.urls import path 
from .views import webhook, home

urlpatterns = [
    path('webhook/', webhook, name='webhook'),
    path('home/', home, name='home'),
]