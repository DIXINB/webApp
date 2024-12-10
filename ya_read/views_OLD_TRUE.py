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
    client_id=os.getenv('CLIENT_ID')
    redirect_uri=os.getenv('REDIRECT_URI')
    context={'client_id':client_id, 'redirect_uri':redirect_uri}
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
    r=requests.get("https://cloud-api.yandex.net/v1/disk/resources/files?limit=7&media_type=document,text&fields=name",headers=headers)
    r_name_list=[]
    numbers=[0,1,2,3,4,5]
#    r_name_list=r.json()['items'][0]['name']
    [r_name_list.append(r.json()['items'][n]['name']) for n in numbers]
#    r_name=r.json()['items'][0]['name']
    return JsonResponse({'filename_list':r_name_list})
#    return JsonResponse({'filename':r_name})

def callback_2(token):
    tkn=token
    headers={"Authorization": f"OAuth {tkn}"}
    r=requests.get("https://cloud-api.yandex.net/v1/disk/resources/files?limit=7&media_type=document,text&fields=name,path,resource_id,file",headers=headers)

    r_name_list=[]
    r_path_list=[]
    numbers=[0,1,2,3,4,5]
    [r_name_list.append(r.json()['items'][n]['name']) for n in numbers]
    [r_path_list.append(r.json()['items'][n]['path']) for n in numbers]
    name_path=list(zip(r_name_list,r_path_list))
#    name_path_list=list(name_path)
#    return JsonResponse({'filename_list':r_name_list})
    return JsonResponse({'filename_list':name_path})
