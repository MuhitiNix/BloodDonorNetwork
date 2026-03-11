from django.urls import path
from . import views

urlpatterns = [
    
    path('', views.search_donors, name='home'), 
    path('register/', views.register_page, name='register'),
    path('search/', views.search_donors, name='search'), 
]