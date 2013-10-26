# Create your views here.
from django.shortcuts import get_object_or_404, render_to_response, render
from ecore.models import Exam

class menu_entry():
	id = 1
	name = "home"
	def __init__(self, id, name):
		self.id = id
		self.name = name

from django.template import RequestContext
def home(request):
	menu = [menu_entry(1, "home"), menu_entry(2, "login")]
	c = RequestContext(request, {"menu_list": menu})
	return render_to_response('ecore/home.html', c)

def exam_detail(request, exam_id):
	exam = get_object_or_404(Exam, pk=exam_id)
	return render(request, 'ecore/exam_detail.html', {'exam': exam })


from django.http import HttpResponseRedirect, HttpResponse
from django.core.urlresolvers import reverse
from django.contrib.auth import authenticate
import django.contrib.auth

import django.forms as forms
class AuthenticationForm(forms.Form):
    username = forms.CharField(max_length=100)
    password = forms.CharField(max_length=100)

def login(request):
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
