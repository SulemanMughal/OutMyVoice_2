from django.db import models
from django.conf import settings
from embed_video.fields import EmbedVideoField
from django.db.models.signals import pre_save
from django.dispatch import receiver
from django.conf import settings
from django.core.mail import send_mail
from django.db.models.signals import post_save
from django.contrib.auth.models import User
from ckeditor_uploader.fields import RichTextUploadingField
from django.urls import reverse

class Blog(models.Model):
    author      =       models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=False)
    title       =       models.CharField(max_length=1000 , blank=False)
    slug        =       models.CharField(max_length=1000, blank=False)
    image       =       models.ImageField(blank=True)
    video       =       EmbedVideoField(blank=True)
    description =       RichTextUploadingField( blank=True)
    created_at  =       models.DateTimeField(auto_now_add=True)
    updated     =       models.DateTimeField(auto_now=True)
    publish     =       models.BooleanField(blank=True,default=None, null=True)
    class Meta:
        ordering = ["-created_at"]

    def __str__(self):
        return self.title
    
    def get_absolute_url(self):
        return reverse("detail", args=[self.slug])
        
        
class BlogComment(models.Model):
    name        =       models.CharField(max_length=100)
    email       =       models.CharField(max_length=100)
    description =       models.TextField(max_length=1000)
    post_date   =       models.DateTimeField(auto_now_add=True)
    blog        =       models.ForeignKey(Blog, on_delete=models.CASCADE)

    class Meta:
        ordering = ["-post_date"]

    def __str__(self):
        return self.description
    
  



class BlogReply(models.Model):
    name        =       models.CharField(max_length=100)
    email       =       models.CharField(max_length=100)
    description =       models.TextField(max_length=1000)
    post_date   =       models.DateTimeField(auto_now_add=True)
    comment     =       models.ForeignKey(BlogComment, on_delete=models.CASCADE)

    class Meta:
        ordering = ["-post_date"]

    def __str__(self):
        return self.name

