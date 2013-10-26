# Create your views here.
from django.shortcuts import get_object_or_404, render_to_response, render
from ecore.models import Exam

from django.template import RequestContext
def home(request):
	c = RequestContext(request, {})
	return render_to_response('ecore/home.html', c)

def exam_list(request):
	exams = Exam.objects.all( )
	return render(request, 'ecore/exam_list.html', {'exams': exams })

def exam_detail(request, exam_id):
	exam = get_object_or_404(Exam, pk=exam_id)
	return render(request, 'ecore/exam_detail.html', {'exam': exam })

def exam_questions(request, exam_id):
	exam = get_object_or_404(Exam, pk=exam_id)
	return render(request, 'ecore/exam_questions.html', {'exam': exam })


from django.http import HttpResponseRedirect, HttpResponse
from django.core.urlresolvers import reverse
from django.contrib.auth import authenticate
import django.contrib.auth

import django.forms as forms
class AuthenticationForm(forms.Form):
    username = forms.CharField(max_length=100)
    password = forms.CharField(max_length=100)

def logout_view(request):
	django.contrib.auth.logout(request)
	return HttpResponseRedirect("/")

def login_view(request):
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
	password = forms.CharField(max_length=32)
	password_again = forms.CharField(max_length=32)
	email = forms.CharField(max_length=48)

from django.contrib.auth.models import User
def register_view(request):
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
