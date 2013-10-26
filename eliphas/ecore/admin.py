from django.contrib import admin
from ecore.models import Exam, QuestionGroup, Question, Choice, ExamInstance, QuestionInstance

admin.site.register(Exam)
admin.site.register(QuestionGroup)
admin.site.register(Question)
admin.site.register(Choice)
admin.site.register(ExamInstance)
admin.site.register(QuestionInstance)

