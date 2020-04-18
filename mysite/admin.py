from django.contrib import admin

# Register your models here.

from .models import (
    Petition,
    UserProfile,
    PetitionResponseFeedback
)


class PetitionAadmin(admin.ModelAdmin):
    list_filter=[
        'approve',
        # 'Petition_Category'
        'timestamp'
    ]
    date_hierarchy = 'timestamp'
    # filter_horizontal = [
    #     'user'
    # ]
    search_fields =[
        'Petition_Title',
        'Petition_Category',
        'Petition_Category_Other',
        'Action_Person'
    ]
    


class PetitionResponseFeedbackAadmin(admin.ModelAdmin):
    list_filter=[
        'petition__approve',
        # 'Petition_Category'
        'timestamp'
    ]
    date_hierarchy = 'timestamp'
    # filter_horizontal = [
    #     'user'
    # ]
    search_fields =[
        'petition__Petition_Title',
        'petition__Petition_Category',
        'petition__Petition_Category_Other',
        'petition__Action_Person'
    ]

admin.site.register(Petition, PetitionAadmin)
admin.site.register(UserProfile)
admin.site.register(PetitionResponseFeedback, PetitionResponseFeedbackAadmin)