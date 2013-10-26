# Create your views here.
from django.shortcuts import get_object_or_404, render_to_response, render
from ecore.models import Exam

class menu_entry():
	id = 1
	name = "home"
	def __init__(self, id, name):
		self.id = id
		self.name = name

def home(request):
	menu = [menu_entry(1, "home"), menu_entry(2, "login")]
	return render_to_response('ecore/home.html', {"menu_list": menu})

def exam_detail(request, exam_id):
	exam = get_object_or_404(Exam, pk=exam_id)
	return render(request, 'ecore/exam_detail.html', {'exam': exam })


