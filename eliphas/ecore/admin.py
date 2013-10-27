from django.contrib import admin
from ecore.models import Exam, QuestionGroup, Question, Choice, ExamInstance, QuestionInstance, ExamQuestionGroupLink
from django import forms

class ChoiceInline(admin.StackedInline):
	model = Choice
	extra = 4


class QuestionAdmin(admin.ModelAdmin):
	inlines = (ChoiceInline,)


class ExamQuestionGroupLinkInline(admin.TabularInline):
	model = ExamQuestionGroupLink
	extra = 2


class ExamAdmin(admin.ModelAdmin):
	date_hierarchy = 'visibility_starttime'
	inlines = (ExamQuestionGroupLinkInline,)

class QuestionGroupCreateForm(forms.ModelForm):
	pass

class QuestionGroupAdmin(admin.ModelAdmin):
	inlines = (ExamQuestionGroupLinkInline,)

admin.site.register(Exam, ExamAdmin)
admin.site.register(QuestionGroup, QuestionGroupAdmin)
admin.site.register(Question, QuestionAdmin)
#admin.site.register(Choice)
admin.site.register(ExamInstance)
admin.site.register(QuestionInstance)

