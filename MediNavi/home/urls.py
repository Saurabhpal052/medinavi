from django.urls import path
from . import views

urlpatterns = [
    path('doctor_recom/',views.doctor_recom,name="doctor_recom"),
    path('', views.landingPage, name='landing'),
]