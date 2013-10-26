from django.conf.urls import patterns, url

from ecore import views

EXAM_LINK = r'^exam/(?P<exam_id>\d+)/'

urlpatterns = patterns('',
    url(r'^$', views.home, name='home'),

    url(r'^login/$', views.login_view, name='login'),
    url(r'^logout/$', views.logout_view, name='logout'),
    url(r'^register/$', views.register_view, name='register'),

	url(r'^exams/', views.exam_list, name='exam_list'),
	url(EXAM_LINK + r'questions/', views.exam_questions, name='exam_questions'),
	url(EXAM_LINK, views.exam_detail, name='exam_detail'),
)
