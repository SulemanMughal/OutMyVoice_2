
from django import template
from mysite.models import *
from django.contrib.auth.models import User

register = template.Library()


def FindCommendationResponse(user_value, commendation_id):
    return  CommendationResponseFeedback.objects.get(
            user=User.objects.get(id=user_value), 
            commendation = Commendation.objects.get(id=commendation_id)
        ).response

register.filter(FindCommendationResponse)