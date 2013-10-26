# Create your views here.
from django.shortcuts import render_to_response

class menu_entry():
	id = 1
	name = "home"
	def __init__(self, id, name):
		self.id = id
		self.name = name

def home(request):
	menu = [menu_entry(1, "home"), menu_entry(2, "login")]
	return render_to_response('ecore/home.html', {"menu_list": menu})

def question(request):
	pass

