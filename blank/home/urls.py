from django.conf.urls import include, url

from . import views

urlpatterns = [
    url('^$', views.home, name='home'),
]
