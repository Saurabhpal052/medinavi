from django.urls import path
from . import views

urlpatterns = [
    path('post_symtoms/', views.post_symtoms, name='post_symtoms'),
    path('', views.landingPage, name='landing'),
]