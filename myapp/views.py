import os

from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from .decorator import unauthorized_user,allowed_user
from .models import UserProfile
# Create your views here.


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

            # Process latitude and longitude here
            print("Latitude:", latitude)
            print("Longitude:", longitude)

            return JsonResponse({'message': 'Location received successfully'})
        except json.JSONDecodeError as e:
            return JsonResponse({'message': 'Invalid JSON format'}, status=400)
    else:
        return JsonResponse({'message': 'Invalid request method'}, status=400)

