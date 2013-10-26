from django.conf.urls import patterns, url

from ecore import views

urlpatterns = patterns('',
    url(r'^$', views.home, name='home'),
    url(r'^login/$', 'ecore.views.login')
)

