from typing import List
from django.shortcuts import render
from django.http import HttpRequest, HttpResponse
# Create your views here.


def index(request: HttpRequest):

    return HttpResponse("repath , ok")


def get_id(request: HttpResponse, uid):

    return HttpResponse(f"repath uid={uid}")


def  get_info(request: HttpRequest, uname, uage):

    return  HttpResponse(f"repath uname = {uname}, uage = {uage}")