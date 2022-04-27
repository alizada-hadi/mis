from urllib import request
from django.http import HttpResponse
from django.shortcuts import redirect



def allowed_groups(groups=[]):
    def decorator(view_func):
        def wrapper_func(request, *args, **kwargs):
            group = None

            if request.user.groups.exists():
                group = request.user.groups.all()[0].name
            if group in groups:
                return view_func(request, *args, **kwargs)
            else:
                return redirect("unauthorize")
        return wrapper_func
    return decorator