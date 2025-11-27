from django.shortcuts import render
from django.views import View
from django.http import HttpRequest, HttpResponse, JsonResponse
from mycomponent import models
from django.contrib import staticfiles
import orjson
import os

class SoftwareView(View):
    def get(self, request: HttpRequest):

        return render(request, "software_index.html", locals())

    def post(self, request: HttpRequest):
        print(request.POST)

        software_data = {
            "name": request.POST.get("name"),
            "version": request.POST.get("version"),
            "website": request.POST.get("website"),
            "picture": request.FILES.get("picture"),
            "downloads": request.FILES.get("downloads"),
        }

        software_obj = models.Software.objects.create(**software_data)
        print(software_obj)
        # print(software_data)
        return JsonResponse({})

    def delete(self, request: HttpRequest):
        print(models.Software.objects.all())
        request_data = orjson.loads(request.body)
        id = request_data.get("id")
        software = models.Software.objects.get(id=id)
        # print(software)
        if software:
            soft_downloads_path = software.downloads.path
            soft_picture_path = software.picture.path
            if os.path.exists(soft_downloads_path):
                os.remove(soft_downloads_path)
            if os.path.exists(soft_picture_path):
                os.remove(soft_picture_path)
            software.delete()

        print(models.Software.objects.all())
        return HttpResponse("delete ok")