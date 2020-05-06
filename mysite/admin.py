from django.contrib import admin

# Register your models here.

# from .forms import PetitionFormAdmin

from .models import (
    Petition,
    UserProfile,
    PetitionResponseFeedback,
    Commendation,
    CommendationResponseFeedback,
    Petition_Signer,
    AskedQuestions,
    WebBanner
)


# Petition Admin
class PetitionAdmin(admin.ModelAdmin):
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
    

    
# Petition Response Feedback Admin
class PetitionResponseFeedbackAdmin(admin.ModelAdmin):
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

# Commendation Admin
class CommendationAdmin(admin.ModelAdmin):
    list_filter=[
        'approve',
        # 'Petition_Category'
        'timestamp'
    ]
    date_hierarchy = 'timestamp'
    search_fields =[
        'Commendation_Title',
        'Commendation_Category',
        'Commendation_Category_Other',
        'Action_Person'
    ]
    
# Commendation Response Feedback Admin
class CommendationResponseFeedbackAdmin(admin.ModelAdmin):
    list_filter=[
        'commendation__approve',
        # 'Petition_Category'
        'timestamp'
    ]
    date_hierarchy = 'timestamp'
    # filter_horizontal = [
    #     'user'
    # ]
    search_fields =[
        'commendation__Commendation_Title',
        'commendation__Commendation_Category',
        'commendation__Commendation_Category_Other',
        'commendation__Action_Person'
    ]







admin.site.register(Petition, PetitionAdmin)
admin.site.register(UserProfile)
admin.site.register(PetitionResponseFeedback, PetitionResponseFeedbackAdmin)
admin.site.register(Commendation, CommendationAdmin)
admin.site.register(CommendationResponseFeedback, CommendationResponseFeedbackAdmin)
admin.site.register(Petition_Signer)
admin.site.register(AskedQuestions)
admin.site.register(WebBanner)