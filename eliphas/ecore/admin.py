from django.contrib import admin
from ecore.models import Exam, QuestionGroup, Question, Choice

print "hello"

admin.site.register(Exam)
admin.site.register(QuestionGroup)
admin.site.register(Question)
admin.site.register(Choice)

