from django.shortcuts import render,redirect
from .models import *
from .forms import *
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.conf import settings
from django.core.mail import send_mail
from .tokens import account_activation_token
from django.contrib.sites.shortcuts import get_current_site
from django.utils.encoding import force_bytes, force_text
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.template.loader import render_to_string
from django.core.mail import EmailMessage
from django.http import HttpResponse
from django.db.models import Q
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.template.defaultfilters import slugify
from django.contrib.auth.decorators import login_required
from mysite.models import *







# Blog Post List View
def BlogList(request):
    blog = Blog.objects.filter(publish = True)
    paginator = Paginator(blog ,10, allow_empty_first_page=True)
    page = request.GET.get('page', 1)
    try:
        blogs = paginator.page(page)
    except PageNotAnInteger:
        blogs = paginator.page(1)
    except EmptyPage :
        blogs = paginator.page(paginator.num_pages)
    if request.user.is_authenticated:
        try:
            profile = UserProfile.objects.get(user = User.objects.get(username = request.user.username))
        except :
            profile = None
    else:
        profile = None
    context = {
        'blogs':blogs,
        'blog':blog,
        'blog_all_section': True,
        'paginator': paginator,
        'profile':profile
    }
    return render(request,'blog-list-sidebar.html',context)


# Blog Post Detail View
def BlogDetail(request,slug):
    lis   = Blog.objects.all()
    blogs = Blog.objects.get(slug=slug)
    comments= BlogComment.objects.filter(blog=blogs)
    # reply = BlogReply.objects.filter(comment = comments)    
    # print(reply)
    replies = BlogReply.objects.all()
    # print(comments)
    form = Comment()
    form_1 = Reply()
    if request.method =='POST':
         form=Comment(request.POST or None)
         if form.is_valid():
            new_comment = form.save(commit=False)
            new_comment.blog=blogs
            new_comment.save()
            form.save()
            return HttpResponseRedirect(reverse('detail', args=[slug]))
             
 
    context = {
        'blogs':blogs,
        'comments':comments,
        'list':lis,
        'form':form,
        # 'relpy' : reply,
        'replies' : replies,
        'form_1' : form_1,
        # 'blog_all_section':True
        "blog_detail_section":True
    }
    return render(request,'blog-single.html',context)

# Blog Search View
def search(request):
    query=request.GET.get('query',None)
    blogs=Blog.objects.all()
    if query is not None:
        blogs=blogs.filter(
        Q(title__icontains=query)|
        Q(description__icontains=query)|
        Q(author__username__icontains=query)
        )
    paginator = Paginator(blogs ,10) # Shows only 10 records per page

    page = request.GET.get('page', 1)
    try:
        blogs = paginator.page(page)
    except PageNotAnInteger:
    # If page is not an integer, deliver first page.
        blogs = paginator.page(1)
    except EmptyPage:
    # If page is out of range (e.g. 7777), deliver last page of results.
        blogs = paginator.page(paginator.num_pages)
    context={
        'blog_all_section': True,
        'search_section': True,
        'query' : query,
        'blogs':blogs
}

    return render(request,'blog-list-sidebar.html',context)

# Blog Post Reply View
@login_required
def ReplyPage(request,id, slug):
    comment=BlogComment.objects.get(id=id)
    form = Reply()
    if request.method == "GET":
        return redirect(reverse('detail', args = [slug]))
    if request.method=='POST':
        form = Reply(request.POST or None)
        if form.is_valid:
            new = form.save(commit=False)
            new.comment=comment
            new.save()
            form.save()
            return HttpResponseRedirect(reverse('detail', args = [slug]))
        else:
            return redirect(reverse('detail', args = [slug]))


# Blog  Post Form View
@login_required
def blogFormView(request):
    form = blogform()
    if request.method=='POST':
        form = blogform(request.POST ,  request.FILES)
        if form.is_valid():
            new = form.save(commit=False)
            new.author=request.user
            new.slug=slugify(new.title)
            new.save()
            form.save()
            return redirect('list')
    try:
        profile = UserProfile.objects.get(user = User.objects.get(username = request.user.username))
    except:
        profile = None
    context={
    'form':form,
    'blog_write':True,
    'profile' : profile
    }
    return render(request,'blogform.html',context)


# Self Blogs
@login_required
def self_Blogs(request):
    template_name="blog-list-sidebar.html"
    blog = Blog.objects.filter(author=User.objects.get(username=request.user.username))
    paginator = Paginator(blog ,10, allow_empty_first_page=True)
    page = request.GET.get('page', 1)
    try:
        blogs = paginator.page(page)
    except PageNotAnInteger:
        blogs = paginator.page(1)
    except EmptyPage :
        blogs = paginator.page(paginator.num_pages)
    if request.user.is_authenticated:
        try:
            profile = UserProfile.objects.get(user = User.objects.get(username = request.user.username))
        except :
            profile = None
    else:
        profile = None
    context = {
        'blogs':blogs,
        'blog':blog,
        'self_blogs':True,
        'paginator': paginator,
        'profile':profile
    }
    return render(request,
                template_name,
                context
            )

# Blog Post Form View
@login_required
def blogFormViewEditing(request, blog_id):
    template_name="blogform_edit.html"
    try:
        obj = Blog.objects.get(id=blog_id, author = User.objects.get(username=request.user.username))
        if request.method!='POST':
            form = blogform(instance = obj)
        else:
            form = blogform(request.POST, request.FILES, instance = obj)
            if form.is_valid():
                form.save()
                return redirect(reverse("detail", args=[obj.slug]))
        if request.user.is_authenticated:
            try:
                profile = UserProfile.objects.get(user = User.objects.get(username = request.user.username))
            except :
                profile = None
        else:
            profile = None
        context={
            'blog_write':True,
            'form' : form,
            'obj': obj,
            'profile' : profile
        }
        return render(request,
                    template_name,
                    context
                )
    except Exception as e:
        return redirect("list")

@login_required
def AssignBlog(request):
    try:
        profile = UserProfile.objects.get(user = User.objects.get(username = request.user.username))
        if profile.golbal_Admin == "True":
            template_name='assign-a-blog.html'
            form = AssignBlogForm()
            if request.user.is_authenticated:
                try:
                    profile = UserProfile.objects.get(user = User.objects.get(username = request.user.username))
                except :
                    profile = None
            else:
                profile = None
            if request.method=='POST':
                form = AssignBlogForm(request.POST ,  request.FILES)
                if form.is_valid():
                    new = form.save(commit=False)
                    new.slug=slugify(new.title)
                    new.save()
                    form.save()
                    current_site = get_current_site(request)
                    mail_subject = 'VoiceItOut Team.'
                    message = f"A blog has been assigned to {form.user.user} -- {form.author.email} from Global Admin {request.user.usernam}"
                    message += "\nYou can check and edit the details of the blog by following the below link:\n"
                    build_link = str(request.scheme) + "://" + str(get_current_site(request).domain) + str(reverse("blog_editing", args=[new.id]))
                    email = EmailMessage(mail_subject, message, to=[new.author.email, request.user.email])
                    email.send()
                    return redirect('list')
            context={
            'profile':profile,
            'form':form,
            'assign_blog':True

            }
            return render(request, template_name, context)
        else:
            return redirect("list")
    except:
        return redirect("list")