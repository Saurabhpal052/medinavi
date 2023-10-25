from django.urls import path
from . import views

urlpatterns = [
    path('doctor_recom/',views.doctor_recom,name="doctor_recom"),
    path('post_symtoms/', views.post_symtoms, name='post_symtoms'),
    path('', views.landingPage, name='landing'),
]