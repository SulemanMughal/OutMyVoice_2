from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.core.mail import EmailMessage
from django.contrib.sites.shortcuts import get_current_site
from django.template.loader import render_to_string
from django.contrib.auth.models import User
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
    Commendationform
)

# Import APP Tokens
from .tokens import account_activation_token

# Import APP Models
from .models import (
    UserProfile,
    Petition,
    PetitionResponseFeedback,
    Commendation,
    CommendationResponseFeedback
)

# Create your views here.

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

# User Login View    
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

# Logout User View
def logout_User(request):
    logout(request)
    return redirect('home_page')

# User Dashboard View
@login_required()
def dashboard(request):
    template_name = "mysite/dashboard.html"
    try:
        profile = UserProfile.objects.get(user = User.objects.get(username= request.user.username))
        petitions = Petition.objects.filter(Petition_Coverage = profile.Coverage_Admin, user = User.objects.get(username= request.user.username))
        responses = []
        # print("***********************************************")
        for i in petitions:
            j = i.petitionresponsefeedback_set.filter(petition__id = i.id, user=User.objects.get(username=request.user.username))
            if len(j) != 0:
                responses.append(j)
        # print(responses)
        # print("***********************************************")
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
    
# User Registration View
def register_user(request):
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
            user.username = form.cleaned_data['username']
            user.save()
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
    try:
        profile = UserProfile.objects.get(user=request.user)
    except:
        profile = None
    if request.method!='POST':
        form = EditProfileForm(instance = request.user)
    else:
        form = EditProfileForm(request.POST, instance = request.user)
        if form.is_valid():
            # print("*********************************")
            # print(request.POST)
            # print("*********************************")
            form.save()
            # if profile is not None:
            #     # print(profile)
            #     profile.golbal_Admin = request.POST['golbal_Admin']
            #     # print(profile.golbal_Admin)
            #     profile.save()
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

# Create Petition View
@login_required
def petition_start(request):
    template_name= 'mysite/create_petition.html'
    form=Petitionform()
    if request.method == 'POST':
        form=Petitionform(request.POST,request.FILES)
        if form.is_valid():
            new = form.save(commit=False)
            new.user=request.user
            new.save()
            # print(new)
            form.save()
            return redirect(reverse("dashboard"))
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
                return redirect(reverse("SpecificViewPetition_URL", args=[petition_id]))
            else:
                return redirect("globalAdminResponses_URL")
        except:
            return redirect("dashboard")
        
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
        
# Specific Peition View Responses
@login_required
def SpecificViewPetition(request, petition_id):
    template_name = "mysite/dashboard.html"
    try:
        profile = UserProfile.objects.get(user = User.objects.get(username=request.user.username))
        if profile.golbal_Admin == "True":
            obj = Petition.objects.get(id=petition_id)
            # print("*********************************************************")
            # print(obj)
            # print("*********************************************************")
            if obj.Petition_Coverage == profile.Coverage_Admin:
                petitions = obj.petitionresponsefeedback_set.all()
                # print("*********************************************************")
                # print(obj)
                # print("*********************************************************")
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
            else:
                return redirect("globalAdminResponses_URL")
        else:
            return redirect("globalAdminResponses_URL")
    except:
        return redirect("globalAdminResponses_URL")
    
    
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
    
# Specific Petition Details
@login_required
def Petition_Details(request, petition_id):
    template_name="mysite/petition_details.html"
    try:
        profile = UserProfile.objects.get(user=User.objects.get(username=request.user.username))
        obj = Petition.objects.get(id=petition_id)
        # petitions = PetitionResponseFeedback.objects.filter(user = User.objects.get(username=request.user.username))
        context={
            'profile' : profile,
            'obj' : obj,
            'petition_detail_section' : True,
            # 'petitions': petitions
        }
        # print("**********************************")
        # print(context)
        # print("**********************************")
        return render(request,
                      template_name,
                      context)
    except Exception as e:
        # print(e)
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
