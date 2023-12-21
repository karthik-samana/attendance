import os
from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from .decorator import unauthorized_user,allowed_user
from .models import UserProfile
from .models import Temp
# Create your views here.

from math import radians, sin, cos, sqrt, atan2

def calculate_distance(lat1, lon1, lat2, lon2):
    R = 6371.0 * 1000 
    lat1_rad = radians(lat1)
    lon1_rad = radians(lon1)
    lat2_rad = radians(lat2)
    lon2_rad = radians(lon2)
    
    dlat = lat2_rad - lat1_rad
    dlon = lon2_rad - lon1_rad

    a = sin(dlat / 2)**2 + cos(lat1_rad) * cos(lat2_rad) * sin(dlon / 2)**2
    c = 2 * atan2(sqrt(a), sqrt(1 - a))

    distance = R * c
    return distance


@unauthorized_user
def index(request):
    return render(request,'myapp/index.html')

@login_required(login_url='index')
def home(request):
    return render(request,'myapp/home.html')

@unauthorized_user
def student_login(request):
    if request.method=='POST':
        username=request.POST.get('username')
        password=request.POST.get('password')
        user =authenticate(username=username,password=password)
        if user is not None:
            login(request,user)
            return redirect('home')
    return render(request,'myapp/student_login.html')

@unauthorized_user
def faculty_login(request):
    if request.method=='POST':
        username=request.POST.get('username')
        password=request.POST.get('password')
        print("lolol")
        user =authenticate(username=username,password=password)
        if user is not None:
            login(request,user)
            print('hi')
            return redirect('faculty_home')
    return render(request,'myapp/faculty_login.html')

def user_logout(request):
    logout(request)
    return redirect('index')

@allowed_user(['faculty'])
def faculty_home(request):
    return render(request,'myapp/faculty_home.html')


import random

@allowed_user(['faculty'])
def take_attendance(request):
    x=random.randint(1,9999)
    
    return render(request,'myapp/location.html',{'x':x})


@allowed_user(['student'])
def student_attendance(request):
    if request.method=='POST':
        longitude=float(request.POST.get('longitude'))
        latitude=float(request.POST.get('latitude'))
        code=request.POST.get('code')
        x=Temp.objects.filter(code=code).values()
        if x:
            long=float(x[0].get('longitude'))
            lati=float(x[0].get('latitude'))
            distance=calculate_distance(latitude,longitude,lati,long)
            return HttpResponse(distance)
        else:
            return HttpResponse("INvalid code")
            
            
            
    return render(request,'myapp/student_attendance.html')


import json
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
@csrf_exempt
def process_location(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            latitude = data.get('latitude')
            longitude = data.get('longitude')
            x=data.get('x')
            Temp.objects.create(latitude=latitude,longitude=longitude,code=x)
            # Process latitude and longitude here
            print("Latitude:", latitude)
            print("Longitude:", longitude)
            
            return JsonResponse({'message': 'Location received successfully'})
        except json.JSONDecodeError as e:
            return JsonResponse({'message': 'Invalid JSON format'}, status=400)
    else:
        return JsonResponse({'message': 'Invalid request method'}, status=400)

