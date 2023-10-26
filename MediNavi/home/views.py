from django.shortcuts import render
from django.http import HttpResponse
from django.template import loader
# from .forms import MyForm

import requests
from django.http import JsonResponse


# Create your views here.
def landingPage(request):
    template=loader.get_template("index.html")
    # print(request)
    return HttpResponse(template.render())
def doctor_recom(request):
    tm=loader.get_template('doctor_recom.html')
    return HttpResponse(tm.render())

