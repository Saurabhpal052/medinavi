from django.shortcuts import render
from django.http import HttpResponse
from django.template import loader
# from .forms import MyForm
from django.views.decorators.csrf import csrf_exempt


# Create your views here.
def landingPage(request):
    template=loader.get_template("index.html")
    # print(request)
    return HttpResponse(template.render())

@csrf_exempt
def post_symtoms(request:HttpResponse):
    a=request.POST['Symptoms']
    # return HttpResponse(a)
    f=open("symptoms.txt",'a')
    f.write(a)
    f.close()
    template=loader.get_template("index.html")
    return    HttpResponse(template.render())
