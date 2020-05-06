# ****************************************************************
# Find check there exists a reponse objects exists for a petition
# and Cadmin
# ****************************************************************

from django import template
from mysite.models import *
from django.contrib.auth.models import User

register = template.Library()


def FindResponseTrue(user_value, petition_id):
    try:
        PetitionResponseFeedback.objects.get(
            user=User.objects.get(id=user_value), 
            petition = Petition.objects.get(id=petition_id)
        )
        return True
    except:
        return False

register.filter(FindResponseTrue)