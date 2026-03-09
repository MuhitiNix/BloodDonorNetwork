from django.urls import path
from . import views

urlpatterns = [
    path('register/', views.register_page, name='register'),
    path('search/', views.search_donors, name='search'), 
]