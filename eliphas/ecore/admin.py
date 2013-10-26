from django.contrib import admin
from ecore.models import Exam, QuestionGroup, Question, Choice, ExamInstance, QuestionInstance, ExamQuestionGroupLink

class ChoiceInline(admin.StackedInline):
	model = Choice
	extra = 4


class QuestionAdmin(admin.ModelAdmin):
	inlines = (ChoiceInline,)


class ExamQuestionGroupLinkInline(admin.TabularInline):
	model = ExamQuestionGroupLink
	extra = 2


class ExamAdmin(admin.ModelAdmin):
	inlines = (ExamQuestionGroupLinkInline,)


class QuestionGroupAdmin(admin.ModelAdmin):
	inlines = (ExamQuestionGroupLinkInline,)


admin.site.register(Exam, ExamAdmin)
admin.site.register(QuestionGroup, QuestionGroupAdmin)
admin.site.register(Question, QuestionAdmin)
#admin.site.register(Choice)
admin.site.register(ExamInstance)
admin.site.register(QuestionInstance)

