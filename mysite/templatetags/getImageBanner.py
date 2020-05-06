


# ****************************************************************
# Find Commendation Response Object
# ****************************************************************
from django import template
from mysite.models import *
from django.contrib.auth.models import User



register = template.Library()


def getImageBanner(user):
    try:
       return WebBanner.objects.all()[0]
    except:
        return None

register.filter(getImageBanner)