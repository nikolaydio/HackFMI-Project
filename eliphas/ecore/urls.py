from django.conf.urls import patterns, url

from ecore import views

EXAM_LINK = r'^exam/(?P<exam_id>\d+)/'
QUESTION_LINK = EXAM_LINK + r'questions/'

urlpatterns = patterns('',
    url(r'^login/$', views.login_view, name='login'),
    url(r'^logout/$', views.logout_view, name='logout'),
    url(r'^register/$', views.register_view, name='register'),


	url(r'^exams/', views.exam_list, name='exam_list'),
	url(QUESTION_LINK + r'select/(?P<choice_id>\d+)', views.exam_select_choice, name='exam_select_choice'),	
	url(QUESTION_LINK, views.exam_questions, name='exam_questions'),
	url(EXAM_LINK, views.exam_detail, name='exam_detail'),

	url(r'^', views.home, name='home'),

)
