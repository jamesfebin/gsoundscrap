"""gscrap URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.8/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Add an import:  from blog import urls as blog_urls
    2. Add a URL to urlpatterns:  url(r'^blog/', include(blog_urls))
"""
from django.conf import settings
from django.conf.urls import include, url
from django.contrib import admin
from django.conf.urls.static import static


urlpatterns = [
	url(r'^$','gscrapweb.views.home',name='home'),
    url(r'^sync','gscrapweb.views.sync',name='sync'),
    url(r'^save_track_info','gscrapweb.views.save_track_info',name='save_track_info'),
    url(r'^follow_user','gscrapweb.views.follow_user',name='follow_user'),
    url(r'^like_track','gscrapweb.views.like_track',name='like_track'),
    url(r'^admin/', include(admin.site.urls)),
    url('', include('django.contrib.auth.urls', namespace='auth')),
    url('', include('social.apps.django_app.urls', namespace='social')),
]

if settings.DEBUG:
	urlpatterns += static(settings.STATIC_URL,document_root=settings.STATIC_ROOT)