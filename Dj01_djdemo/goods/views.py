from django.shortcuts import render
from django.http.response import HttpResponse

# Create your views here.


def index(request):
    data = "<h1>hello world</h1>"
    return HttpResponse(data, content_type="text/html")
