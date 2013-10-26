from django.conf.urls import patterns, url

from ecore import views

urlpatterns = patterns('',
	url(r'^$', views.home, name='home'),
	url(r'^exam/(?P<exam_id>\d+)', views.exam_detail, name='exam_detail'),
	url(r'^login/$', 'ecore.views.login'),
)

