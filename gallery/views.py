from django.contrib.auth.models import User
from django.shortcuts import render
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
from django.core import serializers
from .models import Image
import json

# Create your views here.
@csrf_exempt
def index(request):
    images_list = Image.objects.all()
    return HttpResponse(serializers.serialize("json", images_list))

@csrf_exempt
def add_user_view(request):
    if request.method == 'POST':
        json_user = json.loads(request.body)
        username = json_user['username']
        first_name = json_user['first_name']
        last_name = json_user['last_name']
        password = json_user['password']
        email = json_user['email']

        user_model = User.objects.create_user(username=username, password=password)
        user_model.first_name = first_name
        user_model.last_name = last_name
        user_model.email = email
        user_model.save()
    return HttpResponse(serializers.serialize("json", [user_model]))

@csrf_exempt
def public_images_view(request, id):
    image_list = Image.objects.filter(user=id, is_public=True)
    return HttpResponse(serializers.serialize("json", image_list))

@csrf_exempt
def login(request):
    if request.method == 'POST':
        json_user = json.loads(request.body)
        username = json_user['username']
        password = json_user['password']

        user = User.objects.get(username=username, password=password)

        if user != None:
            return HttpResponse(serializers.serialize("json", [user]))

        return HttpResponse(serializers.serialize("json", []))

@csrf_exempt
def update_user(request, id):
    if request.method == 'PUT':
        json_user = json.loads(request.body)
        first_name = json_user['first_name']
        last_name = json_user['last_name']
        email = json_user['email']

        user = User.objects.get(id=id)
        user.first_name = first_name
        user.last_name = last_name
        user.email = email

        user.save()
        return HttpResponse(serializers.serialize("json",[user]))

@csrf_exempt
def edit_public(request):
    if request.method == 'PUT':
        json_images = json.loads(request.body)
        images = json_images['images']
        imagesnew = []

        for image in images:
            img = Image.objects.get(id=image['image'])
            img.is_public = image['is_public']
            img.save()
            imagesnew.append(img)

        return HttpResponse(serializers.serialize("json",imagesnew))

@csrf_exempt
def add_image(request, id):
    if request.method == 'POST':
        json_image = json.loads(request.body)
        name = json_image['name']
        url = json_image['url']
        description = json_image['description']
        type1 = json_image['type']
        is_public = json_image['is_public']

        user = User.objects.get(id=id)

        Image.objects.create(name=name, url=url, description=description, type=type1, user=user, is_public=is_public)

        return HttpResponse(serializers.serialize("json",Image.objects.filter(user=id)))