import os
from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from .decorator import unauthorized_user,allowed_user
from .models import UserProfile,Class,Attendance
from .models import Temp
from datetime import datetime,timedelta
from django.utils import timezone
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
@allowed_user(['student'])
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
        user =authenticate(username=username,password=password)
        if user is not None:
            login(request,user)
            return redirect('faculty_home')
    return render(request,'myapp/faculty_login.html')

def user_logout(request):
    logout(request)
    return redirect('index')

@allowed_user(['faculty'])
def faculty_home(request):
    return render(request,'myapp/faculty_home.html')


u_code=''
u_time=datetime.now()
check=True
import secrets

def class_selection(request):
    if request.method == 'POST':
        branch = request.POST.get('branch')
        semester = request.POST.get('semester')
        section = request.POST.get('section')
        def generate_unique_code():
            while True:
                new_code = secrets.randbelow(1000000)
                formatted_code = f'{new_code:06}'
                global u_code,u_time
                u_code=formatted_code
                u_time=datetime.now()
                print(u_code)
                try:
                    Temp.objects.get(code=formatted_code)
                except Temp.DoesNotExist:
                    return formatted_code
                except Temp.MultipleObjectsReturned:
                    pass 
        generate_unique_code()
        global check
        check =True
        return redirect('take_attendance',sem=semester,sec=section)
        # return render(request, 'myapp/dynamic_update.html', {'x': u_code,'sem':semester,'sec':section})

    return render(request,'myapp/class_selection.html')


@allowed_user(['faculty'])
def take_attendance(request, sem, sec):
    expire_time=u_time+ timedelta(minutes=2)
    print(expire_time)
    return render(request, 'myapp/dynamic_update.html', {'x': u_code,'sem':sem,'sec':sec,'expire_time':expire_time})



# @allowed_user(['faculty'])
# def take_attendance(request, sem, sec):
#     q = UserProfile.objects.filter(sem=sem, section=sec).select_related('user').order_by('user__username')
#     status = Attendance.objects.filter(class_attended_id='-1')
#     try:
#         status = Attendance.objects.filter(class_attended_id=Class.objects.get(code=u_code))
#     except:
#         pass
#     data = []
#     for i in q:
#         found = False
#         for j in status:
#             if j.student_id == i.user.id:
#                 data.append({'user': i.user, 'status': j.status})
#                 found = True
#                 break
        
#         if not found:
#             data.append({'user': i.user, 'status': 'False'})
    
#     return render(request, 'myapp/dynamic_update.html', {'x': u_code, 'data': data,'sem':sem,'sec':sec})

from django.http import JsonResponse
import json

@allowed_user(['faculty'])
def take_attendance_d(request, sem, sec):
    q = UserProfile.objects.filter(sem=sem, section=sec).select_related('user').order_by('user__username')
    status = Attendance.objects.filter(class_attended_id='-1')
    try:
        status = Attendance.objects.filter(class_attended_id=Class.objects.get(code=u_code))
    except:
        pass
    data = []
    for i in q:
        found = False
        for j in status:
            if j.student_id == i.user.id:
                data.append({'user': i.user.username, 'status': j.status})  # Adjust data structure as needed
                found = True
                break
        
        if not found:
            data.append({'user': i.user.username, 'status': 'False'}) 
    
    # Return data as JSON response
    return JsonResponse({'data': data})


import json
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt

@csrf_exempt
def process_location(request,sem,sec):
    if request.method == 'POST':
        try:
            global check
            data = json.loads(request.body)
            latitude = data.get('latitude')
            longitude = data.get('longitude')
            if check:
                check=False
                Temp.objects.create(latitude=latitude,longitude=longitude,code=u_code)
                Class.objects.create(faculty=UserProfile.objects.get(id=request.user.id),date=datetime.now().date(),code=u_code,class_id=sem+sec)
            print("Latitude:", latitude)
            print("Longitude:", longitude)
            print(sem,sec)
            
            return JsonResponse({'message': 'Location received successfully'})
        except json.JSONDecodeError as e:
            return JsonResponse({'message': 'Invalid JSON format'}, status=400)
    else:
        return JsonResponse({'message': 'Invalid request method'}, status=400)

def grantAndRevoke(request,x,t):
    id=User.objects.get(username=x)
    if t=='G':
        Attendance.objects.create(student=UserProfile.objects.get(user_id=id),class_attended=Class.objects.get(code=u_code),status=True)
    else:
        d=Attendance.objects.filter(student=UserProfile.objects.get(user_id=id),class_attended=Class.objects.get(code=u_code)).delete()
        
    return JsonResponse({'message': 'Function called successfully'})
    
def get_data(request,sem,sec):
    q = UserProfile.objects.filter(sem=sem, section=sec).select_related('user').order_by('user__username')
    status = Attendance.objects.filter(class_attended_id='-1')
    try:
        status = Attendance.objects.filter(class_attended_id=Class.objects.get(code=u_code))
    except:
        pass
    data = []
    for i in q:
        found = False
        for j in status:
            if j.student_id == i.user.id:
                data.append({'user': i.user, 'status': j.status})
                found = True
                break
        
        if not found:
            data.append({'user': i.user, 'status': 'False'})
    return JsonResponse({'data'})
    

@allowed_user(['student'])
def student_attendance(request):
    if request.method=='POST':
        longitude=float(request.POST.get('longitude'))
        latitude=float(request.POST.get('latitude'))
        code=request.POST.get('code')
        u=UserProfile.objects.get(user_id=request.user.id)
        y=Class.objects.filter(code=code,class_id=u.sem+u.section)
        x=Temp.objects.filter(code=code).values() 
        if y:
            long=float(x[0].get('longitude'))
            lati=float(x[0].get('latitude'))
            distance=calculate_distance(latitude,longitude,lati,long)
            if distance<8:
                flag=Attendance.objects.filter(student=UserProfile.objects.get(user_id=request.user.id),class_attended=Class.objects.get(code=code))
                print(flag.values())
                if flag:
                    return HttpResponse("Your Attendace Already Recorded")
                else:
                    if(datetime.now()>x[0].get('expire')+timedelta(minutes=2,seconds=10)):
                        return HttpResponse("Code Expired⏳")
                    else:
                        Attendance.objects.create(student=UserProfile.objects.get(user_id=request.user.id),class_attended=Class.objects.get(code=code),status=True)
                        return HttpResponse("Your Attendance has been Recorded")
            else:
                return HttpResponse("Go to class 😏")
        else:
            return HttpResponse("INvalid code")
                
            
    return render(request,'myapp/student_attendance.html')




def reports(request, code):
    sem_sec = Class.objects.get(code=code)
    sem, sec = sem_sec.class_id[0], sem_sec.class_id[1]
    students = UserProfile.objects.filter(sem=sem, section=sec).order_by('user__username')
    attendance_records = Attendance.objects.filter(class_attended__code=code, student__in=students)
    
    present_students = {}
    overall_students = {}

    for student in students:
        student_id = student.id
        attendance_record = attendance_records.filter(student_id=student_id).first()
        student_name = User.objects.get(username=student.user.username).first_name
        
        overall_students[student.user.username] = {'name': student_name, 'status': 'Absent'}

        if attendance_record:
            present_students[student.user.username] = {'name': student_name, 'status': 'Present'}
            overall_students[student.user.username]['status'] = 'Present'

    context = {
        'present_students': present_students,
        'overall_students': overall_students,
    }
    
    return render(request, 'myapp/reports.html', context)
    

def view_reports(request):
    classes_taught = Class.objects.filter(faculty_id=request.user.id).order_by('-date')

    class_data = [
        {'date': class_obj.date, 'sem': class_obj.class_id[0], 'section': class_obj.class_id[1],'code':class_obj.code}
        for class_obj in classes_taught
    ]


    context = {'class_data': class_data}

    return render(request, 'myapp/view_reports.html', context)

    





