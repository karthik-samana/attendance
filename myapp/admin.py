from django.contrib import admin


from .models import UserProfile,Attendance,Class
# Register your models here.

admin.site.register([UserProfile,Attendance,Class])
