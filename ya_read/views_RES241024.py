import os
import json
from django.views.decorators.csrf import csrf_exempt
from django.shortcuts import render
from django.http.response import JsonResponse
import requests

def chicken(request):
    return render(request, "ya_read/chicken.html")

@csrf_exempt
def my_homepage(request):
    
    if request.method=="POST":
        data = json.loads(request.body)
        token=data['tkn']
        print('token:', token)
        try:
          return callback_1(token)
        except Exception as e:
          return JsonResponse({'error':str(e)},status= 403)
    return render(request, "ya_read/my_homepage.html")

@csrf_exempt    
def chicken(request):
    return render(request, "ya_read/chicken.html")
    
def callback_1(token):
    tkn=token
    headers={"Authorization": f"OAuth {tkn}"}
    r=requests.get("https://cloud-api.yandex.net/v1/disk/resources/files?limit=1&media_type=document,text&fields=name",headers=headers)
    r_name=r.json()['items'][0]['name']
    return JsonResponse({'filename':r_name})
