from django.conf.urls import include, url

from . import views

urlpatterns = [
    url('^$', views.categories, name='categories'),
    url('^category/(?P<category_id>\d+)/$', views.category, name='category'),
    url('^blank/(?P<category_id>\d+)/(?P<blank_id>\d+)/$', views.blank, name='blank'),
    url('^download/$', views.download, name='download'),
    url('^bookmark/$', views.bookmark, name='bookmark'),
    url('^bookmark_add/$', views.bookmark_add, name='bookmark_add'),
    url('^profile/$', views.profile, name='profile'),
    
]
