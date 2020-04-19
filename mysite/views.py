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
        profile = UserProfile.objects.get(user = request.user)
        petitions = Petition.objects.filter(Petition_Coverage = profile.Coverage_Admin)
    except :
        profile = None
        petitions = None
    context={
        'dashboard_section':True,
        'all_petitions_section': True,
        'profile': profile,
        'petitions' : petitions
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
            form.save()
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
    context={
        'form': form,
        'change_password_section': True
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

    context={
        'create_petition_section': True,
        'form':form,
    }
    return render(request,template_name ,context)

# User (Itself) View Petitions View
@login_required
def User_Petitions(request):
    template_name = "mysite/dashboard.html"
    petitions = Petition.objects.filter(user = request.user)
    context = {
        'petitions': petitions,
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
    context={
        'form':form,
        'create_commendation_section': True,
    }
    return render(request, template_name,context)

# User All Commendations View
@login_required
def All_Commendations(request):
    template_name="mysite/commendations.html"
    commendations = Commendation.objects.all()
    context={
        'commendations':commendations,
        'commendations_section': True
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
            commendation = Commendation.objects.get(id = commendation_id)
            feedback_obj, created =  CommendationResponseFeedback.objects.get_or_create(
                user = request.user,
                commendation = commendation,
                Coverage_Admin = UserProfile.objects.get(user=request.user).Coverage_Admin,
            )
            if created:
                feedback_obj.Feedback = request.POST['Feedback']
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
    context = {
        'commendations': commendations,
        'my_commendation_view': True
    }
    return render(request,
                template_name,
                context
            )
