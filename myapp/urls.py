from django.urls import path
from . import views


urlpatterns = [
    path('',views.index,name='index'),
    path('home/',views.home,name='home'),
    path('student_login',views.student_login,name='student_login'),
    path('faculty_login',views.faculty_login,name='faculty_login'),
    path('logout',views.user_logout,name='logout'),
    path('faculty_home',views.faculty_home,name='faculty_home'),
    path('class_selection',views.class_selection,name='class_selection'),
    path('take_attendance/<str:sem>/<str:sec>',views.take_attendance,name='take_attendance'),
    path('take_attendance_d/<str:sem>/<str:sec>',views.take_attendance_d,name='take_attendance_d'),
    path('process_location/<str:sem>/<str:sec>',views.process_location,name='process_location'),
    path('student_attendance',views.student_attendance,name='student_attendance'),
    path('grantAndrevoke/<str:x>/<str:t>',views.grantAndRevoke,name='grantAndRevoke'),
    path('reports/<str:code>',views.reports,name='reports'),
    path('view_reports',views.view_reports,name='view_reports'),
]