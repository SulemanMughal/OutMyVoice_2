
# ****************************************************************
# Find whether the petition response exists for a given petition 
# and Cadmin or not
# ****************************************************************

from django import template
from mysite.models import *
from django.contrib.auth.models import User

register = template.Library()


def FindResponseTrueID(user_value, petition_id):
    try:
        response = PetitionResponseFeedback.objects.get(
            user=User.objects.get(id=user_value), 
            petition = Petition.objects.get(id=petition_id)
        )
        return response.id
    except:
        return None

register.filter(FindResponseTrueID)