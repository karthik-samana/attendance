from django.http import HttpResponse
from django.shortcuts import redirect

def allowed_user(allowed_roles=[]):
    def decorator(view_func):
        def wrapper(request,*args, **kwargs):
            group=None
            if request.user.groups.exists():
                group=request.user.groups.all()[0].name
            if group in allowed_roles:
                return view_func(request,*args, **kwargs)
            else:
                if request.user.groups.all()[0].name=='faculty':
                    return redirect('faculty_home')
            return redirect('home')
        return wrapper
    return decorator

def unauthorized_user(func):
    def wrapper(request,*args, **kwargs):
        if(request.user.is_authenticated):
            if request.user.groups.all()[0].name=='faculty':
                return redirect('faculty_home')
            return redirect('home')
        else:
            return func(request,*args, **kwargs)
    return wrapper