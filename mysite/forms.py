
from django import forms
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _
from django.core import validators
from .models import (
    Petition,
    PetitionResponseFeedback,
    Commendation,
    CommendationResponseFeedback
)
from django.contrib.auth.forms import (
    UserCreationForm, 
    UserChangeForm
)
from django.contrib.auth import (
    authenticate, 
    get_user_model, 
    password_validation
)

#User Login Form ................
class loginForm(forms.Form):
    username = forms.CharField()
    password = forms.CharField(widget = forms.PasswordInput())




#User Registration Form...................
class registerForm(forms.ModelForm):
    password = forms.CharField(label = 'Password', 
                            widget = forms.PasswordInput(),
                            strip=False,
                            help_text=password_validation.password_validators_help_text_html(),
                        )
    password2 = forms.CharField(label = 'Repeat Password', 
                            widget = forms.PasswordInput(),
                            strip=False,
                            help_text="Both Passwords should be same.",
                        )
    email = forms.EmailField(label = 'Email Address', 
                            widget = forms.TextInput()
                        )
    username = forms.CharField(label="Username", 
                            widget=forms.TextInput()
                        )
    class Meta:
        model = User
        fields = [
            'first_name',
            'last_name',
        ]

    # Clean Methof for username
    def clean_username(self):
        username_data = self.cleaned_data.get("username")
        if username_data is None:
            raise ValidationError("Username is required")
        else:
            try:
                User.objects.get(username = username_data)
                raise ValidationError(username_data + "\tAlready Exists.")
            except User.DoesNotExist:
                return username_data
    
    # Clean Method for email
    def clean_email(self):
        email_data = self.cleaned_data.get('email')
        if email_data is None:
            raise ValidationError("Enter a valid E-mail Address")
        else:
            if User.objects.filter(email = email_data).count() != 0 :
                if not User.objects.get(email = email_data).is_active :
                    User.objects.get(email = email_data).delete()
                else:
                    raise ValidationError(email_data + "\tAlready Exists.")
            else:
                return email_data
    
    # Clean Method For Password
    def clean_password2(self):
        cd = self.cleaned_data
        if self.cleaned_data.get('password') != cd['password2']:
            raise forms.ValidationError("Passwords don't match.")
        return cd['password2']

    
# User Edit Profile Form
class EditProfileForm(UserChangeForm):
    password = forms.CharField(label='', widget = forms.TextInput(attrs = {'type' : 'hidden'}))
    class Meta:
        model = User
        fields = [
            'username',
            'first_name',
            'last_name',
            'password',
        ]
        
# Create Petition Form
class Petitionform(forms.ModelForm):
    class Meta:
        model=Petition
        exclude =  ['user','approve']


# Petition Response Feedback Form
class PetitionResponseForm(forms.ModelForm):
    class Meta:
        model = PetitionResponseFeedback
        fields = [
            'Feedback'
        ]

# Create Commendation Form
class Commendationform(forms.ModelForm):
    class Meta:
        model=Commendation
        exclude =  [
            'user',
            'approve'
        ]
        
# Commendation Response Feedback Response Form
class CommendationResponseFeedbackForm(forms.ModelForm):
    class Meta:
        model=CommendationResponseFeedback
        exclude =  [
            'user',
            'approve'
        ]