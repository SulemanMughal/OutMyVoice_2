from django import template
from mysite.models import *
from django.contrib.auth.models import User

register = template.Library()


def FindCommendationResponseTrueID(user_value, commendation_id):
    try:
        c = CommendationResponseFeedback.objects.get(
            user=User.objects.get(id=user_value), 
            commendation = Commendation.objects.get(id=commendation_id)
        )
        return c.id
    except:
        return False

register.filter(FindCommendationResponseTrueID)