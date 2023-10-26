from django.shortcuts import render
from django.http import HttpResponse
from django.template import loader

def signup(request:HttpResponse):
    c={}
    return render(request,"signup.html",c)