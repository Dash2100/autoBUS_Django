from django.contrib import admin
from django.urls import path
from django.http import HttpResponse
from django.shortcuts import render
import json
import requests

def notify(text):
    token = 'lVk4U4xqG6aYVTO7NG4Rp9VhO4nDEzgInmNCFxu1jDi'
    headers = { "Authorization": "Bearer " + token }
    data = {'message': text }
    requests.post("https://notify-api.line.me/api/notify",headers = headers, data = data)

def index(request):
    with open('log.txt','r',encoding='UTF-8') as f:
        log = f.readlines()
    with open('settings.json','r') as f:
        data = json.loads(f.read())
    return render(request, 'index.html', locals())

def on(request):
    with open('settings.json','w',encoding='UTF-8') as f:
        f.write('{"status":"on"}')
    notify('AutoBUS is now on.')
    return HttpResponse('on')

def off(request):
    with open('settings.json','w',encoding='UTF-8') as f:
        f.write('{"status":"off"}')
    notify('AutoBUS is now off.')
    return HttpResponse('on')


urlpatterns = [
    path('', index),
    path('on/', on),
    path('off/', off),
]
