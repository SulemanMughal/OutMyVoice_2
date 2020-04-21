from django.conf.urls import url
from . import views


urlpatterns = [
    
    # Blog List View URL
    url(r'^$',
        views.BlogList,
        name='list'
    ),
    
    # Blog Post Detail View URL
    url(r'^detail/(?P<slug>[-\w]+)$',
        views.BlogDetail,
        name='detail'
    ),
    
    # Blog Search View URL
    url(r'^search/',
        views.search,
        name='search'
    ),
    
    # BLog Post Form View URL
    url(r'^create-a-blog/',
        views.blogFormView,
        name='blog'
    ),
    
    # Blog Comment Reply View URL
    url(r'^reply/(?P<id>\d+)/(?P<slug>[-\w]+)/$',
        views.ReplyPage,
        name='reply'
    ),

]