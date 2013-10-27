# Create your views here.
from django.shortcuts import get_object_or_404, get_list_or_404, render_to_response, render
from ecore.models import Exam, QuestionInstance, Choice
from django.contrib.auth.models import User
from django.http import HttpResponseForbidden
from django import forms
from django.contrib.auth.decorators import login_required


from django.template import RequestContext
from django.utils import timezone

@login_required
def home(request):
	active_list = []
	upcomming_list = []
	exams = request.user.exams.all()
	for ex in exams:
		if (timezone.now() > ex.starttime):
			dur = ex.exam.duration - (timezone.now() - ex.starttime).seconds
			if dur <= 0:
				continue
			active_list.append([ex.exam.pk, ex.exam.name, dur])
		else:
			dur = (ex.starttime - timezone.now()).seconds
			upcomming_list.append( [ex.exam.pk, ex.exam.name, dur] )
	c = RequestContext(request, {"active_exams":active_list, "upcomming_exams":upcomming_list, "active_count": len(active_list)})
	return render_to_response('ecore/home.html', c)

@login_required
def exam_list(request):
	exams = set(request.user.exams.all())
	exams = exams.union(request.user.accessexams.all())
	return render(request, 'ecore/exam_list.html', {'exams': exams })

@login_required
def exam_detail(request, exam_id):
	exam = get_object_or_404(Exam, pk=exam_id)
	if not exam.allowed_users.filter(pk=request.user.id).exists():
		return HttpResponseForbidden()
	return render(request, 'ecore/exam_detail.html', {'exam': exam })

@login_required
def exam_questions(request, exam_id):
	exam = get_object_or_404(Exam, pk=exam_id)
	examinstance = request.user.exams.filter(exam_id=exam.id, endtime=None)
	if not examinstance:
		examinstance = exam.TakeExam(request.user)
	else:
		examinstance = examinstance[0]
	return render(request, 'ecore/exam_questions.html', {'examinstance': examinstance })


import ecore.models
@login_required
#name = doexam
def my_exams_view(request):
	exam_instance = ecore.models.ExamInstance.objects.filter(user=request.user)
	if len(exam_instance) < 1:
		return HttpResponse("You are not doing any exams currently.")
	print(exam_instance[0].exam.name)
	questions = ecore.models.QuestionInstance.objects.filter(exam=exam_instance[0])
	c = RequestContext(request, {"time_left":100, "question_list": questions, "examinst":exam_instance[0]})
	return render_to_response('ecore/exam.html', c)




from django.http import HttpResponseRedirect, HttpResponse
from django.core.urlresolvers import reverse
from django.contrib.auth import authenticate
import django.contrib.auth

import django.forms as forms
class AuthenticationForm(forms.Form):
    username = forms.CharField(max_length=100)
    password = forms.CharField(max_length=100, widget=forms.PasswordInput())

def logout_view(request):
	django.contrib.auth.logout(request)
	return HttpResponseRedirect("/")

def login_view(request):
	if request.user.is_authenticated():
		return HttpResponseRedirect('/')
	if request.method == "POST":
		username = request.POST['username']
		password = request.POST['password']
		user = authenticate(username=username, password=password)
		if user is not None:
			if user.is_active:
				django.contrib.auth.login(request, user)
				return HttpResponseRedirect("/")
			else:
				return HttpResponse("not active")
		else:
			return HttpResponse("wrong username/pass")
	else:
		c = RequestContext(request, {'form':AuthenticationForm})
		return render_to_response( "ecore/login.html", c)

class RegisterForm(forms.Form):
	username = forms.CharField(max_length=32)
	password = forms.CharField(max_length=32, widget=forms.PasswordInput())
	password_again = forms.CharField(max_length=32, widget=forms.PasswordInput())
	email = forms.EmailField(max_length=48)

from django.contrib.auth.models import User
def register_view(request):
	if request.user.is_authenticated():
		return HttpResponseRedirect('/')
	if request.method == "POST":
		username = request.POST['username']
		password = request.POST['password']
		password_again = request.POST['password_again']
		email = request.POST['email']
		
		if password != password_again:
			return HttpResponse("Passwords are not the same.")

		if len(User.objects.filter(username=username)) > 0:
			return HttpResponse("Username already taken.")
		user = User.objects.create_user(username, email, password)
		user.save()
		return HttpResponseRedirect('/login')
	else:
		c = RequestContext(request, {'form':RegisterForm})
		return render_to_response( "ecore/register.html", c)
