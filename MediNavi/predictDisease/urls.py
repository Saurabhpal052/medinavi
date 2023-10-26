from django.urls import path
from . import views

urlpatterns = [
    path('',views.yourMayHave,name="yourMayHave"),
]