from django.shortcuts import render
from django.http.response import HttpResponse

# Create your views here.


def index(request):
    data = {"msg": "success"}
    return HttpResponse(data)
