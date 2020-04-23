from mysite.models import UserProfile
from django.contrib.auth.models import User
from django.shortcuts import redirect, reverse

def simple_decorator(func):
    def wrap(request, *args, **kwargs):
        # print()
        if request.user.is_authenticated:
            user = User.objects.get(username=request.user.username)
            print(UserProfile.objects.get(user = user))
        # else:
        #     return redirect("login_user_url")
        return func(request, *args, **kwargs)
    
    wrap.__doc__ = func.__doc__
    wrap.__name__ = func.__name__
    return wrap