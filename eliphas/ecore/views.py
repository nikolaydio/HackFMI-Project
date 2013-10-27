# Create your views here.
from django.shortcuts import get_object_or_404, get_list_or_404, render_to_response, render
from ecore.models import Exam, QuestionInstance, Choice, ExamInstance
from django.contrib.auth.models import User
from django.http import HttpResponse, HttpResponseForbidden
from django import forms
from django.contrib.auth.decorators import login_required

from django.template import RequestContext
from django.utils import timezone

@login_required
def home(request):
	active_list = []
	upcomming_list = []
	taken_list = []
	exams = request.user.exams.all()
	for ex in exams:
		if (timezone.now() > ex.starttime):
			dur = ex.time_left()
			if ex.has_ended():
				#exam is already taken:
				taken_list.append([ex.exam.pk, ex.exam.name, ex.result(), ex.max_result()])
				ex.finish_exam(True)
				continue
			active_list.append([ex.exam.pk, ex.exam.name, dur])
		else:
			dur = (ex.starttime - timezone.now()).seconds
			upcomming_list.append( [ex.exam.pk, ex.exam.name, dur] )
	c = RequestContext(request, {"active_exams":active_list,
		"upcomming_exams":upcomming_list,
		"active_count": len(active_list),
		"taken_exams": taken_list})
	return render_to_response('ecore/home.html', c)

@login_required
def exam_list(request):
	now = timezone.now()
	exams = set(request.user.exams.all())
	exams = exams.union([e for e in request.user.accessexams.all() if ( not e.visibility_starttime or e.visibility_starttime<=now ) and ( not e.visibility_endtime or e.visibility_endtime>=now ) ])
	return render(request, 'ecore/exam_list.html', {'exams': exams })

@login_required
def exam_detail(request, exam_id):
	exam = get_object_or_404(Exam, pk=exam_id)
	users_taken = ExamInstance.objects.filter(exam_id=exam_id)
	users_taken = set([e.user for e in users_taken])
	exam.users_taken = users_taken
	if not exam.allowed_users.filter(pk=request.user.id).exists():
		return HttpResponseForbidden()
	return render(request, 'ecore/exam_detail.html', {'exam': exam })


class AuthenticationForm(forms.Form):
    choice = forms.CharField(max_length=100)

@login_required
def exam_questions(request, exam_id):
	exam = get_object_or_404(Exam, pk=exam_id)
	examinstance = request.user.exams.filter(exam_id=exam.id, endtime=None)
	if not examinstance:
		examinstance = exam.TakeExam(request.user)
	else:
		examinstance = examinstance[0]
	return render(request, 'ecore/exam_questions.html', {'examinst': examinstance })

def exam_select_choice(request, exam_id, choice_id):
	examinstance = get_object_or_404(ExamInstance, exam_id=exam_id, user_id=request.user.id, endtime=None)
	choice = get_object_or_404(Choice, pk=choice_id)
	questioninstance = examinstance.questions.get(question_id=choice.question.id)
	questioninstance.choice = choice
	questioninstance.save()
	
	return HttpResponse('')

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
			c = RequestContext(request, {'form':RegisterForm, 'error_msg':"Passwords are not the same."})
			return render_to_response( "ecore/register.html", c)

		if len(User.objects.filter(username=username)) > 0:
			c = RequestContext(request, {'form':RegisterForm, 'error_msg':"Username already taken."})
			return render_to_response( "ecore/register.html", c)

		user = User.objects.create_user(username, email, password)
		user.save()

		#render the login form
		c = RequestContext(request, {'form':AuthenticationForm, 'error_msg':"Your account has been crated. Please log in."})
		return render_to_response( "ecore/login.html", c)
	else:
		c = RequestContext(request, {'form':RegisterForm})
		return render_to_response( "ecore/register.html", c)
