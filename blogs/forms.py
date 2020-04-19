from django import forms
from django.forms import ModelForm
from .models import *

class Comment(ModelForm):
    class Meta:
        model = BlogComment
        fields =  [
            'name',     
            'email',       
            'description',         
             
    
        ]

class Reply(ModelForm):
    class Meta:
        model = BlogReply
        fields =  [
            'name',     
            'email',       
            'description',         
]


class blogform(ModelForm):
    class Meta:
        model=Blog
        exclude = ['author','slug','publish']