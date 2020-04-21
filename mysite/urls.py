from django.conf.urls import url
from django.urls import path
from django.views.generic import TemplateView
from django.contrib.auth.views import (
    PasswordResetView,
    PasswordResetDoneView, 
    PasswordResetConfirmView, 
    PasswordResetCompleteView
)

# App View Import Statements
from . import views

urlpatterns = [
    
    # Home View URL
    url(r'^$', 
        views.home, 
        name="home_page"
    ),
    
    # User Login View URL
    url(r'^login/$',
        views.login_User,
        name="login_user_url"
    ),
    
    # User Logout View URL
    url(r'^logout/$', 
        views.logout_User, 
        name= "logout_user_url"
    ),

    # User Dashboard View URL
    url(r'^dashbaord/$', 
        views.dashboard, 
        name = "dashboard"
    ),
    
    # User Registration View URL
    url(r'^register/$', 
        views.register_user, 
        name= "register"
    ),
    
    # Register Account Email Confirmation View URL
    url(r'^activate/(?P<uidb64>[0-9A-Za-z_\-]+)/(?P<token>[0-9A-Za-z]{1,13}-[0-9A-Za-z]{1,20})/$',
        views.activate, 
        name='activate'
    ),
    
    # -------------------------------------------------------------------------------------------------------
    # Password Reset URL(s)
    path('password_reset/', 
        PasswordResetView.as_view(), 
        name='password_reset' 
    ),
    path('password_reset/done/', 
        PasswordResetDoneView.as_view(), 
        name='password_reset_done'
    ),
    path('reset/<uidb64>/<token>/',
        PasswordResetConfirmView.as_view(), 
        name='password_reset_confirm'
    ),
    path('reset/done/', 
        PasswordResetCompleteView.as_view(), 
        name='password_reset_complete'
    ),
    
    # Profile View URL
    url(r'^profile/$', 
        views.profile_user, 
        name= "profile"
    ),
    
    # User Change Password View URL
    url(r'^change_password/$', 
        views.change_password, 
        name = "change_password"
    ),
    
    # Create Petition View URL
    path("petition_start/", 
        views.petition_start, 
        name="Start-a-Petition"
    ),
    
    # User (Itself) Petitions View URL
    path("view-petitions/", 
        views.User_Petitions, 
        name="Self-Petitions"
    ),
    
    # Petition Feedback Response View
    path("submit-a-response-petition/<int:petition_id>/",
        views.PetitionResponseFeedbackView,
        name="PetitionResponse"),

    # Create Commendation View URL
    path("commendation_start/", 
        views.commendation_start, 
        name="Start-a-Commendation"
    ),
    
    # User All Commendations View URL
    url(r'^all-commendations/$',
        views.All_Commendations,
        name="all-commendations-url"),
    
    # Uer Commendation Response Feedback View URL
    path("submit-a-response-commendation/<int:commendation_id>/",
        views.CommendationResponseFeedbackView,
        name="CommendationResponse"),
    
    # User (Itself) Commendation View URL
    path("view-commendation/", 
        views.User_Commendation, 
        name="Self-Commendation"
    ),

    # Global Admin Petitons Responses URL
    path("view-peition-responses-admin-global", views.globalAdminResponses, name="globalAdminResponses_URL"),

    # Global Admin Commendations Responses URL
    path("view-commendation-responses-admin-global", views.globalAdminResponsesCommendations, name="globalAdminResponsesCommendations_URL"),


    # Approve Petition by Global Admin
    path("approve-petition/<int:petition_id>", views.approved_petition, name="approved_petition_URL"),
    
    # Approve Commendation by Global Admin
    path("approve-commendation/<int:commendation_id>", views.approved_commendation, name="approved_commendation_URL"),
    
    # Specific Petition Responses View
    path("view-specific-petition-responses/<int:petition_id>", views.SpecificViewPetition, name="SpecificViewPetition_URL"),
    
    # Specific Commendation Responses View
    path("view-specific-Commendation-responses/<int:commendation_id>", views.SpecificViewCommendation, name="SpecificViewCommendation_URL"),

    # Petition Details View
    path('view-specific-peition/<int:petition_id>/', views.Petition_Details, name="Petition_Details"),

    # See Specific Petition Response View URL
    path("specific-petition-response/<int:petition_id>/", views.SpecificPetitonResponse, name="ViewSpecificPetitionResponse_URL"),
    
    # See Specific Commendation Response View URL
    path("specific-commendation-response/<int:commendation_id>/", views.SpecificCommendationResponse, name="ViewSpecificCommendationResponse_URL"),
    
    # Commendation Details View
    path('view-specific-commendation/<int:commendation_id>/', views.Commendation_Details, name="Commendation_Details"),
]