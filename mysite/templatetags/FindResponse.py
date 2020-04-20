

from django import template
from mysite.models import *
from django.contrib.auth.models import User

register = template.Library()


def FindResponse(user_value, petition_id):
    return PetitionResponseFeedback.objects.get(
            user=User.objects.get(id=user_value), 
            petition = Petition.objects.get(id=petition_id)
            ).response

register.filter(FindResponse)