from django.urls import path
from . import views


urlpatterns = [
    path('',views.index,name='index'),
    path('home/',views.home,name='home'),
    path('student_login',views.student_login,name='student_login'),
    path('faculty_login',views.faculty_login,name='faculty_login'),
    path('logout',views.user_logout,name='logout'),
    path('faculty_home',views.faculty_home,name='faculty_home'),
    path('take_attendance',views.take_attendance,name='take_attendance'),
    path('process_location',views.process_location,name='process_location'),
    path('student_attendance',views.student_attendance,name='student_attendance'),

]