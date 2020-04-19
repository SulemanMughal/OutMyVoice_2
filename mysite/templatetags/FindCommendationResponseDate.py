from django import template
from mysite.models import *
from django.contrib.auth.models import User
from datetime import datetime, timezone
from datetime import timedelta

register = template.Library()


def FindCommendationResponseDate( commendation_id):
    try:
        time1 = Commendation.objects.get(id=commendation_id).timestamp
        time2 = datetime.now(timezone.utc)
        elapsedTime = time2 - time1
        if elapsedTime < timedelta(days = 1):
            return True
        else:
            return False
    except Exception as e:
        return False

register.filter(FindCommendationResponseDate)



# >>> time1 = datetime.datetime.now()
# >>>  # waited a few minutes before pressing enter
# >>> elapsedTime = time2 - time1
# >>> elapsedTime
# datetime.timedelta(0, 125, 749430)
# >>> divmod(elapsedTime.total_seconds(), 60)
# (2.0, 5.749430000000004) # divmod returns quotient and remainder
# # 2 minutes, 5.74943 seconds

# time3 = time1  + timedelta(days=1)
# print(type(elapsedTime)) 
# print( elapsedTime - timedelta(days=1))

        # time3 = time1 + timedelta(days = 1)
        # print(time2 - time1)