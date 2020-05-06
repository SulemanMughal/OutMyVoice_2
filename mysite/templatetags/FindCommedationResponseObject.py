


# ****************************************************************
# Find Commendation Response Object
# ****************************************************************
from django import template
from mysite.models import *
from django.contrib.auth.models import User

register = template.Library()


def FindCommedationResponseObject(user_value, commendation_id):
    try:
        return  CommendationResponseFeedback.objects.get(
            user=User.objects.get(id=user_value), 
            commendation = Commendation.objects.get(id=commendation_id)
        )
    except:
        return None

register.filter(FindCommedationResponseObject)