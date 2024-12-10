import os
import json
from django.views.decorators.csrf import csrf_exempt
from django.shortcuts import render
from django.http.response import JsonResponse
import requests
from collections import namedtuple

def chicken(request):
    return render(request, "ya_read/chicken.html")

@csrf_exempt
def my_homepage(request):
    rnum=15
    client_id=os.getenv('CLIENT_ID')
    redirect_uri=os.getenv('REDIRECT_URI')
    context={'client_id':client_id, 'redirect_uri':redirect_uri, 'rnum':rnum}
    if request.method=="POST":
        data = json.loads(request.body)
        token=data['tkn']
        print('token:', token)
        try:
          return callback_2(token)
        except Exception as e:
          return JsonResponse({'error':str(e)},status= 403)
    return render(request, "ya_read/my_homepage.html",context=context)

@csrf_exempt    
def chicken(request):
    return render(request, "ya_read/chicken.html")
    
def callback_1(token):
    tkn=token
    headers={"Authorization": f"OAuth {tkn}"}
    r=requests.get("https://cloud-api.yandex.net/v1/disk/resources/files?limit=9&media_type=document,text&fields=name",headers=headers)
    r_name_list=[]
    numbers=[0,1,2,3,4,5,6,7]
    [r_name_list.append(r.json()['items'][n]['name']) for n in numbers]
    return JsonResponse({'filename_list':r_name_list})

def callback_2(token):
    tkn=token
    headers={"Authorization": f"OAuth {tkn}"}
    r=requests.get("https://cloud-api.yandex.net/v1/disk/resources/files?limit=12&media_type=document,text&fields=name,path,resource_id,file",headers=headers)
    numbers=len(r.json()['items'])
    print("len r:  ",numbers)
    obj=r.json()['items']
    Rec=namedtuple('Rec', 'name path')
    rec=[Rec(obj[n]['name'], obj[n]['path']) for n in range(numbers)]
    return JsonResponse({'filename_list':rec})
