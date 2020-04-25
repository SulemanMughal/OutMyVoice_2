from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.core.mail import EmailMessage
from django.contrib.sites.shortcuts import get_current_site
from django.template.loader import render_to_string
from django.contrib.auth.models import User

from django.core.paginator import (
    Paginator, 
    EmptyPage, 
    PageNotAnInteger
)

from django.http import (
    HttpResponse,
    HttpResponseRedirect
)

from django.contrib.auth.forms import (
    UserChangeForm, 
    PasswordChangeForm
)

from django.shortcuts import (
    render, 
    redirect,
    reverse
)

from django.contrib.auth import (
    authenticate, 
    login,
    logout,
    update_session_auth_hash
)

from django.utils.http import (
    urlsafe_base64_encode, 
    urlsafe_base64_decode
)

from django.utils.encoding import (
    force_bytes, 
    force_text
)

# Import APP Forms
from .forms import (
    loginForm,
    registerForm,
    EditProfileForm,
    Petitionform,
    PetitionResponseForm,
    Commendationform, 
    PetitionSignerform,
    CommendationSignerform
)

# Import APP Tokens
from .tokens import account_activation_token

# Import APP Models
from .models import (
    UserProfile,
    Petition,
    PetitionResponseFeedback,
    Commendation,
    CommendationResponseFeedback,
    Commendation_Signer
)

# User App Decorators
from .decorators import simple_decorator

# Helper Functions
@login_required
def findUserProfile(request):
    try:
        return UserProfile.objects.get(
            user = User.objects.get(
                email = request.user.email
                )
            )
    except UserProfile.DoesNotExist:
        if request.user.is_superuser:
            profile = UserProfile.objects.create(
                user = User.objects.get(
                    email = request.user.email
                    ),
                golbal_Admin = "True"
                )
            return profile
        else:
            return None



# -----------------------------------------USER SECTION---------------------------------------

# Home View 
def home(request):
    template_name = "mysite/index.html"
    context={
        'home_section':True
    }
    return render(request,
                template_name,
                context
            )

# Login View    
def login_User(request):
    template_name="mysite/login.html"
    if request.method!= 'POST':
        form = loginForm()
    else:
        form = loginForm(request.POST)
        if form.is_valid():
            user = authenticate(request, 
                        username = form.cleaned_data['username'], 
                        password = form.cleaned_data['password']
                    )
            if user is not None:
                login(request, 
                    user
                )
                return redirect('dashboard')
            else:
                messages.warning(request, 'Usename or password may have been entered incorrectly.')
    context={
        'form': form,
        'login_section': True
    }
    return render(request, 
                template_name, 
                context
            )

# Logout View
def logout_User(request):
    logout(request)
    return redirect('home_page')

# Registration View
def register_user(request):
    try:
        template_name= "mysite/register.html"
        message_template_name = "mysite/acc_active_email.html"
        active_email_confirm_template_name = "mysite/acc_active_email_confirm.html"
        if request.method!='POST':
            form = registerForm()
        else:
            form = registerForm(request.POST)
            if form.is_valid():
                user = form.save(commit=False)
                user.is_active = False
                user.set_password(form.cleaned_data['password2'])
                user.email = form.cleaned_data['email']
                user.username = form.cleaned_data['email'].split("@")[0]
                user.save()
                UserProfile.objects.create(user = user)
                current_site = get_current_site(request)
                message = render_to_string(message_template_name, {
                    'user':user, 'domain':current_site.domain,
                    'uid': urlsafe_base64_encode(force_bytes(user.pk)),
                    'token': account_activation_token.make_token(user),
                })
                mail_subject = 'Activate your account.'
                to_email = form.cleaned_data.get('email')
                email = EmailMessage(mail_subject, message, to=[to_email])
                email.send()
                context={
                    'reigster_section' : True
                }
                return render(request, 
                            active_email_confirm_template_name,
                            context
                        )
        context={
            'form' : form,
            'reigster_section': True
        }
        return render(request, template_name, context)
    except Exception as e:
        # print(e)
        messages.success(request, str(e))
        context={
            'form' : form,
            'reigster_section': True
        }
        return render(request, template_name, context)

# Register Account Email Confirmation View
def activate(request, uidb64, token):
    try:
        uid = force_text(urlsafe_base64_decode(uidb64))
        user = User.objects.get(pk=uid)
    except(TypeError, ValueError, OverflowError, User.DoesNotExist):
        user = None
    if user is not None and account_activation_token.check_token(user, token):
        user.is_active = True
        user.save()
        messages.success(request, "User has been registered successfully.")
        return redirect('login_user_url')
    else:
        messages.error(request, "Invalid Registration Activation Link")
        return redirect("login_user_url")

# Profile View
@login_required
def profile_user(request):
    template_name = "mysite/profile.html"
    profile = findUserProfile(request)
    if request.method!='POST':
        form = EditProfileForm(instance = request.user)
    else:
        form = EditProfileForm(request.POST, instance = request.user)
        if form.is_valid():
            try:
                form.save()
                messages.success(request, "Profile has been updated successfully.")
                return redirect(reverse("profile"))
            except Exception as e:
                messages.success(request, str(e))
                return redirect(reverse("profile"))
        else:
            messages.success(request, str(form.errors))
            return redirect(reverse("profile"))
    context={
        'form': form,
        'profile_section': True,
        'profile': profile
    }
    return render(request,
                template_name,
                context
            )

# User Password Change View
def change_password(request):
    template_name="mysite/change_password.html"
    if request.method!='POST':
        form = PasswordChangeForm(user = request.user)
    else:
        form = PasswordChangeForm(data = request.POST, user = request.user)
        if form.is_valid():
            form.save()
            update_session_auth_hash(request, form.user)
            return HttpResponseRedirect(reverse('profile'))
    try:
        profile = UserProfile.objects.get(user = User.objects.get(username=request.user.username))
    except:
        profile = None
    context={
        'form': form,
        'change_password_section': True,
        'profile': profile
    }
    return render(request,
                template_name,
                context
            )


# *******************************************USER SECTION****************************************




# --------------------------------------- PETITION SECTION --------------------------------------
# Dashboard View
@login_required()
def dashboard(request):
    template_name = "mysite/dashboard.html"
    responses = []      #Variable used to store petition responses
    try:
        profile = findUserProfile(request)  #Find Profile of a user
        if request.user.is_superuser:
            petitions = Petition.objects.all()      #Find Results for a superuser
        else:
            petitions = Petition.objects.filter(Petition_Coverage = profile.Coverage_Admin)     #Find Results for a specific coverage admin
        
        # Find petition responses
        for i in petitions:
            j = i.petitionresponsefeedback_set.filter(
                    petition__id = i.id, 
                    user=User.objects.get(
                        username=request.user.username
                    )
                )
            if len(j) != 0:
                responses.append(j)
    except :
        profile = None
        petitions = None
    context={
        'dashboard_section':True,
        'all_petitions_section': True,
        'profile': profile,
        'petitions' : petitions,
        'responses': responses
    }
    return render(request, 
                template_name,
                context
            )




# Create Petition View
@login_required
def petition_start(request):
    template_name= 'mysite/create_petition.html'
    form=Petitionform()
    if request.method == 'POST':
        form=Petitionform(request.POST,request.FILES)
        # print(request.POST)
        if form.is_valid():
            try:
                new = form.save(commit=False)
                new.user=request.user
                new.save()
                form.save()
                # --------------------------------------------------------------
                # Email Settings
                current_site = get_current_site(request)
                message = '''“Thank you for submitting your petition. 
                                Your submission is under review for appropriate action, 
                                we may contact you for clarifications, if necessary. 
                                You will be notified once your petition is made available for public viewing 
                                and signing. Together, we will build our Nation”'''
                message += "\n\n\nFollowing is the link for the petition review\n\n\n"
                mail_subject = 'VoiceItOut Team.'
                build_link =  str(request.scheme) + str("://") + str( current_site.domain) + str(reverse("Petition_Details", args = [new.id]))
                message += str(build_link)
                to_email = []
                for i in UserProfile.objects.filter(Coverage_Admin = new.Petition_Coverage):
                    to_email.append(str(i.user.email))
                print(to_email)
                email = EmailMessage(mail_subject, message, to=[to_email])
                email.send()
                # ---------------------------------------------------------------
                messages.success(request, "Email has been send to all Coverage Admin")
                return redirect(reverse("Start-a-Petition"))
            except Exception as e:
                messages.success(request, str(e))
                return redirect(reverse("Start-a-Petition"))
        else:
            # print(form.errors)
            messages.success(request, str(form.errors))
            return redirect(reverse("Start-a-Petition"))
    try:
        profile = UserProfile.objects.get(user = User.objects.get(username=request.user.username))
    except:
        profile = None

    context={
        'create_petition_section': True,
        'form':form,
        'profile': profile
    }
    return render(request,template_name ,context)






# User (Itself) View Petitions View
@login_required
def User_Petitions(request):
    template_name = "mysite/dashboard.html"
    petitions = Petition.objects.filter(user = request.user)
    try:
        profile = UserProfile.objects.get(user = User.objects.get(username=request.user.username))
    except:
        profile = None
    context = {
        'petitions': petitions,
        'profile': profile,
        'my_petition_view': True
    }
    return render(request,
                template_name,
                context
            )





# Petition Feedback Response View
@login_required
def PetitionResponseFeedbackView(request, petition_id):
    if request.method == "GET":
        return redirect(reverse("dashboard"))
    else:
        try:
            petition = Petition.objects.get(id = petition_id)
            feedback_obj, created =  PetitionResponseFeedback.objects.get_or_create(
                user = request.user,
                petition = petition,
                Coverage_Admin = UserProfile.objects.get(user=request.user).Coverage_Admin,
            )
            if created:
                feedback_obj.Feedback = request.POST['Feedback']
                feedback_obj.response = request.POST['response']
                feedback_obj.save()
                return redirect("dashboard")
            feedback_obj.save()
            return redirect("dashboard")
        except:
            return redirect(reverse("dashboard"))








# Global Admin see all responses
@login_required
def globalAdminResponses(request):
    template_name = "mysite/dashboard.html"
    try:
        profile = UserProfile.objects.get(user=User.objects.get(username=request.user.username))
        if profile.golbal_Admin == "True":
            petitions = PetitionResponseFeedback.objects.all()
        else:
            petitions = PetitionResponseFeedback.objects.filter(user=User.objects.get(username=request.user.username))
    except:
        profile = None

    context = {
        'profile': profile,
        'petitions': petitions,
        'global_admin_section_petitions' :True
    }
    return render(request,
                  template_name,
                  context)








# Approved Petiton By Global Admin
@login_required
def approved_petition(request, petition_id):
    if request.method != "POST":
        return redirect("globalAdminResponses_URL")
    else:
        try:
            profile = UserProfile.objects.get(user = User.objects.get(username=request.user.username))
            if profile.golbal_Admin == "True":
                petition = Petition.objects.get(id=petition_id)
                if request.POST.get("response", None) is None:
                    petition.approve = False
                elif "on" in request.POST['response']:
                    petition.approve = True
                    petition.save()
                    # return redirect("globalAdminResponses_URL")
                    # Email settings --------------------------------------------------------
                    current_site = get_current_site(request)
                    message = '''“Petition has now go on live.”'''
                    message += "\n\n\nFollowing is the link for the petition review\n\n\n"
                    mail_subject = 'VoiceItOut Team.'
                    build_link =  str(request.scheme) + str("://") + str( current_site.domain) + str(reverse("LivePetitionsDetails_URL", args = [petition.id]))
                    message += str(build_link)
                    to_email = []
                    for i in UserProfile.objects.filter(Coverage_Admin = new.Petition_Coverage):
                        to_email.append(str(i.user.email))
                    to_email.append(petition.user.email)
                    email = EmailMessage(mail_subject, message, to=[to_email])
                    email.send()
                # ---------------------------------------------------------------------
                return redirect(reverse("SpecificViewPetition_URL", args=[petition_id]))
            else:
                return redirect("globalAdminResponses_URL")
        except:
            return redirect("dashboard")


@login_required
def approved(request, petition_id):
    try:
        profile = UserProfile.objects.get(user = User.objects.get(username=request.user.username))
        if profile.golbal_Admin == "True":
            petition = Petition.objects.get(id=petition_id)
            petition.approve = True
            petition.save()
            messages.success(request, "Petition has been approved")
            current_site = get_current_site(request)
            message = '''“Petition has now go on live.”'''
            message += "\n\n\nFollowing is the link for the petition review\n\n\n"
            mail_subject = 'VoiceItOut Team.'
            build_link =  str(request.scheme) + str("://") + str( current_site.domain) + str(reverse("LivePetitionsDetails_URL", args = [petition.id]))
            message += str(build_link)
            to_email = []
            for i in UserProfile.objects.filter(Coverage_Admin = petition.Petition_Coverage):
                to_email.append(str(i.user.email))
            to_email.append(petition.user.email)
            email = EmailMessage(mail_subject, message, to=[to_email])
            email.send()
            return redirect(reverse("Petition_Details",args = [petition_id]))
        else:
            messages.success(request, "You don't have the right to approve it.")
            return redirect(reverse("Petition_Details",args = [petition_id]))
    except:
        messages.success(request, "Invalid Request")
        return redirect("dashboard")








        
# Specific Peition View Responses
@login_required
def SpecificViewPetition(request, petition_id):
    template_name = "mysite/dashboard.html"
    profile  =findUserProfile(request)
    try:
        obj = Petition.objects.get(id=petition_id)
        petitions = obj.petitionresponsefeedback_set.all()
        context = {
            'petitions': petitions,
            'profile': profile,
            'specific_petition_view': True,
            'title' : obj.Petition_Title,
            'obj' : obj
        }
        # print(context)
        return render(request,
                    template_name,
                    context
        )
    except:
        messages.success(request, "Invalid Request")
        return redirect("dashboard")







# Specific Petition Details
@login_required
def Petition_Details(request, petition_id):
    template_name="mysite/petition_details.html"
    profile = findUserProfile(request)
    try:
        obj = Petition.objects.get(id=petition_id)
        context={
            'profile' : profile,
            'obj' : obj,
            'petition_detail_section' : True,
        }
        return render(request,
                        template_name,
                        context)
    except:
        messages.success(request, "Invalid Request")
        return redirect("dashboard")







# See Specific Petition Response 
@login_required
def SpecificPetitonResponse(request, petition_id ):
    template_name="mysite/petition_response_single.html"
    try:
        profile = UserProfile.objects.get(user=User.objects.get(username=request.user.username))
        petition_response = PetitionResponseFeedback.objects.get(id=petition_id, user=request.user)
        context={
            'profile':profile,
            'petition_response': petition_response,
            'view_specific_petiton_response_only': True
        }
        return render(request, template_name, context)
    except Exception as e:
        redirect("dashboard")







# Live Petition View Both(Auth and Unauth)
def LivePetitions(request):
    petitions = Petition.approved_objects.all()
    profile = None
    template_name="mysite/petition-list-sidebar.html"
    if request.user.is_authenticated:
        # template_name="mysite/live_petitions.html"    
        try:
            profile = UserProfile.objects.get(user=User.objects.get(username=request.user.username))
        except Exception as e:
        # print(e)
            return redirect("dashboard")
        # context=  {
        # 'petitions': petitions,
        # 'profile' : profile,
        # 'livePetition_Section': True
        # }
        # return render(request,
        #                 template_name,
        #                 context)
    paginator = Paginator(petitions ,10, allow_empty_first_page=True)
    page = request.GET.get('page', 1)
    try:
        petitions = paginator.page(page)
    except PageNotAnInteger:
        petitions = paginator.page(1)
    except EmptyPage :
        petitions = paginator.page(paginator.num_pages)
    context = {
        'petitions':petitions,
        'livePetition_Section': True,
        'paginator': paginator,
    }
    return render(request,template_name,context)

from django.db.models import Q
@login_required
def searchPetition(request):
    query=request.GET.get('query',None)
    petitions = Petition.approved_objects.all()
    if query is not None:
        petitions=petitions.filter(
        Q(Petition_Title__icontains=query)|
        Q(Petition_Category__icontains=query)|
        Q(Expalnation__icontains=query)|
        Q(id__iexact=query)
        )
    profile = None
    template_name="mysite/petition-list-sidebar.html"
    if request.user.is_authenticated:
        # template_name="mysite/live_petitions.html"    
        try:
            profile = UserProfile.objects.get(user=User.objects.get(username=request.user.username))
        except Exception as e:
        # print(e)
            return redirect("dashboard")
        # context=  {
        # 'petitions': petitions,
        # 'profile' : profile,
        # 'livePetition_Section': True
        # }
        # return render(request,
        #                 template_name,
        #                 context)
    paginator = Paginator(petitions ,10, allow_empty_first_page=True)
    page = request.GET.get('page', 1)
    try:
        petitions = paginator.page(page)
    except PageNotAnInteger:
        petitions = paginator.page(1)
    except EmptyPage :
        petitions = paginator.page(paginator.num_pages)
    context = {
        'petitions':petitions,
        'livePetition_Section': True,
        'paginator': paginator,
        'search_section': True,
        'query' : query,
    }
    return render(request,template_name,context)







# Live Petition View (Only Unauth)
def LivePetitionsDetailView(request, petition_id):
    profile = None
    if request.user.is_authenticated:
        # template_name="mysite/live_petitions.html"    
        try:
            profile = UserProfile.objects.get(user=User.objects.get(username=request.user.username))
        except Exception as e:
        # print(e)
            return redirect("dashboard")
    template_name="mysite/petition-single.html"
    try:
        petition = Petition.approved_objects.get(id=petition_id)
        template_name="mysite/petition-single.html"
        context={
            'livePetition_Section_detail': True,
            'petition': petition,
            'profile' : profile   
        }
        return render(request, template_name, context)
    except Exception as e:
        # print(e)
        return redirect("LivePetitions_URL")
 
 
 
 
 
 
    
# Petitions Live Detail View Comment URL (Only Unauth)
def LivePetitionsSignatureView(request, petition_id):
    if request.method != "POST":
        return redirect(reverse("LivePetitionsDetails_URL", args=[petition_id]))
    try:
        petition = Petition.approved_objects.get(id=petition_id)
        form = PetitionSignerform(request.POST)
        if form.is_valid():
            obj = form.save(commit=False)
            obj.petition = petition
            obj.save()
            return redirect(reverse("LivePetitionsDetails_URL", args=[petition_id]))
        else:
            return redirect(reverse("LivePetitionsDetails_URL", args=[petition_id]))
    except:
        return redirect("LivePetitions_URL")


# **************************************** PETITION SECTION ****************************************





        








































# Create Commendation View
@login_required
def commendation_start(request):
    template_name="mysite/create_commendation.html"
    form=Commendationform()
    if request.method == 'POST':
        form=Commendationform(request.POST,request.FILES)
        # print(request.POST, request.FILES, sep="\n")
        if form.is_valid():
            new = form.save(commit=False)
            new.user=request.user
            new.save()
            form.save()
            return redirect('dashboard')
    try:
        profile = UserProfile.objects.get(user = User.objects.get(username=request.user.username))
    except:
        profile = None
    context={
        'form':form,
        'create_commendation_section': True,
        'profile':profile
    }
    return render(request, template_name,context)











# User All Commendations View
@login_required
def All_Commendations(request):
    template_name="mysite/commendations.html"
    commendations = Commendation.objects.all()
    try:
        profile = UserProfile.objects.get(user = User.objects.get(username=request.user.username))
    except:
        profile = None
    context={
        'commendations':commendations,
        'commendations_section': True,
        'profile':profile
    }
    return render(request,
                template_name,
                context)







    
# User Commendation Feedback Response View
@login_required
def CommendationResponseFeedbackView(request, commendation_id):
    if request.method == "GET":
        return redirect(reverse("all-commendations-url"))
    else:
        try:
            # print(request.POST)
            commendation = Commendation.objects.get(id = commendation_id)
            feedback_obj, created =  CommendationResponseFeedback.objects.get_or_create(
                user = request.user,
                commendation = commendation,
                Coverage_Admin = UserProfile.objects.get(user=request.user).Coverage_Admin,
            )
            if created:
                feedback_obj.Feedback = request.POST['Feedback']
                feedback_obj.response = request.POST['response']
                print(request.POST)
                feedback_obj.save()
                return redirect("all-commendations-url")
            feedback_obj.save()
            return redirect("all-commendations-url")
        except:
            return redirect("all-commendations-url")







        
# User (Itself) Commendation View
@login_required
def User_Commendation(request):
    template_name = "mysite/commendations.html"
    commendations = Commendation.objects.filter(user = request.user)
    try:
        profile = UserProfile.objects.get(user = User.objects.get(username=request.user.username))
    except:
        profile = None
    context = {
        'commendations': commendations,
        'my_commendation_view': True,
        'profile':profile
    }
    return render(request,
                template_name,
                context
            )






@login_required
def globalAdminResponsesCommendations(request):
    template_name = "mysite/commendations.html"
    try:
        profile = UserProfile.objects.get(user = User.objects.get(username=request.user.username))
        if profile.golbal_Admin == "True":
            commendations = CommendationResponseFeedback.objects.all()
        else:
            commendations = CommendationResponseFeedback.objects.filter(user=User.objects.get(username=request.user.username))
    except:
        profile = None
    context = {
        'commendations': commendations,
        'my_commendation_view_global': True,
        'profile':profile
    }
    return render(request,
                template_name,
                context
            )











        
# Approved Commendation By Global Admin
@login_required
def approved_commendation(request, commendation_id):
    if request.method != "POST":
        return redirect("globalAdminResponsesCommendations_URL")
    else:
        try:
            profile = UserProfile.objects.get(user = User.objects.get(username=request.user.username))
            if profile.golbal_Admin == "True":
                commendation = Commendation.objects.get(id=commendation_id)
                # print(request.POST)
                if request.POST.get("response", None) is None:
                    commendation.approve = False
                elif "on" in request.POST['response']:
                    commendation.approve = True
                commendation.save()
                return redirect(reverse("SpecificViewCommendation_URL", args=[commendation_id]))
            else:
                return redirect("globalAdminResponsesCommendations_URL")
        except:
            return redirect("dashboard")
        
        
        
        
        
        
    
    
# Specific Commendation Responses View
@login_required
def SpecificViewCommendation(request, commendation_id):
    template_name = "mysite/commendations.html"
    try:
        profile = UserProfile.objects.get(user = User.objects.get(username=request.user.username))
        if profile.golbal_Admin == "True":
            obj = Commendation.objects.get(id=commendation_id)
            # print("*********************************************************")
            # print(obj)
            # print("*********************************************************")
            if obj.Commendation_Coverage == profile.Coverage_Admin:
                commendations = obj.commendationresponsefeedback_set.all()
                # print("*********************************************************")
                # print(obj)
                # print("*********************************************************")
                context = {
                    'commendations': commendations,
                    'profile': profile,
                    'specific_commendation_view': True,
                    'title' : obj.Commendation_Title,
                    'obj' : obj
                }
                # print(context)
                return render(request,
                            template_name,
                            context
                )
            else:
                return redirect("globalAdminResponsesCommendations_URL")
        else:
            return redirect("globalAdminResponsesCommendations_URL")
    except:
        return redirect("globalAdminResponsesCommendations_URL")
    
    
        
# Commenadtion Details
@login_required
def Commendation_Details(request, commendation_id):
    template_name="mysite/commendation-details-single.html"
    try:
        profile=UserProfile.objects.get(user=User.objects.get(username=request.user.username))
        obj = Commendation.objects.get(id=commendation_id)
        context={
            'profile':profile,
            'obj' : obj,
            'specific_commendation_details':True
        }
        return render(request, template_name, context)
    
    except Exception as e:
        print(e)
        return redirect("all-commendations-url")
    
# Single Commendation Response Details
@login_required
def SpecificCommendationResponse(request, commendation_id):
    template_name="mysite/commendation-response-details-single.html"
    try:
        profile = UserProfile.objects.get(user=User.objects.get(username=request.user.username))
        commendation_response = CommendationResponseFeedback.objects.get(id=commendation_id, user=request.user)
        context={
            'profile':profile,
            'commendation_response': commendation_response,
            'view_specific_commendation_response_only': True
        }
        return render(request, template_name, context)
    except Exception as e:
        redirect("all-commendations-url")

    
# Live Commendations View (Both Auth and Unauth)
def LiveCommendationsView(request):
    commendations = Commendation.approved_objects.all()
    profile = None
    template_name="mysite/commendation-list-sidebar.html"
    if request.user.is_authenticated:
        # template_name="mysite/live_petitions.html"    
        try:
            profile = UserProfile.objects.get(user=User.objects.get(username=request.user.username))
        except Exception as e:
        # print(e)
            return redirect("dashboard")
        # context=  {
        # 'petitions': petitions,
        # 'profile' : profile,
        # 'livePetition_Section': True
        # }
        # return render(request,
        #                 template_name,
        #                 context)
    paginator = Paginator(commendations ,10, allow_empty_first_page=True)
    page = request.GET.get('page', 1)
    try:
        petitions = paginator.page(page)
    except PageNotAnInteger:
        commendations = paginator.page(1)
    except EmptyPage :
        commendations = paginator.page(paginator.num_pages)
    context = {
        'commendations':commendations,
        'liveCommendation_Section': True,
        'paginator': paginator,
    }
    return render(request,template_name,context)

# Commendation Live Detail View (Both Auth and Unauth)
def LiveCommendationsDetailView(request,commendation_id):
    profile = None
    if request.user.is_authenticated:
        # template_name="mysite/live_petitions.html"    
        try:
            profile = UserProfile.objects.get(user=User.objects.get(username=request.user.username))
        except Exception as e:
        # print(e)
            return redirect("dashboard")
    template_name="mysite/commendation-single.html"
    try:
        commendation = Commendation.approved_objects.get(id=commendation_id)
        template_name="mysite/commendation-single.html"
        context={
            'liveCommendation_Section_detail': True,
            'commendation': commendation,
            'profile' : profile   
        }
        return render(request, template_name, context)
    except Exception as e:
        # print(e)
        return redirect("LiveCommendations_URL")
    
    
    
    
  
# Commendation Live Detail View Comment URL (Only Unauth)
def LiveCommendationSignatureView(request, commendation_id):
    if request.method != "POST":
        return redirect(reverse("LiveCommendationsDetails_URL", args=[commendation_id]))
    try:
        commendation = Commendation.approved_objects.get(id=commendation_id)
        form = CommendationSignerform(request.POST)
        if form.is_valid():
            obj = form.save(commit=False)
            obj.commendation = commendation
            obj.save()
            return redirect(reverse("LiveCommendationsDetails_URL", args=[commendation_id]))
        else:
            print(form.errors)
            return redirect(reverse("LiveCommendationsDetails_URL", args=[commendation_id]))
    except:
        return redirect("LiveCommendations_URL")
    