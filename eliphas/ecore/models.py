from django.db import models
from django.contrib.auth.models import User

# Create your models here.

class Exam(models.Model):
	name = models.CharField(max_length=64)

	def TakeExam(self, user):
		exam = user.exams.create(exam=self)
		# todo: choose some random questions
		for group in self.questiongroup_set.all():
			for question in group.question_set.all():
				exam.questioninstance_set.create(choice=None)
		return exam

class QuestionGroup(models.Model):
	exams = models.ManyToManyField(Exam)

class Question(models.Model):
	group = models.ForeignKey(QuestionGroup)
	text = models.CharField(max_length=512)

class Choice(models.Model):
	question = models.ForeignKey(Question)
	text = models.CharField(max_length=512)

class ExamInstance(models.Model):
	exam = models.ForeignKey(Exam)
	user = models.ForeignKey(User, related_name='exams')

class QuestionInstance(models.Model):
	exam = models.ForeignKey(ExamInstance)
	question = models.ForeignKey(Question)
	choice = models.ForeignKey(Choice, null=True)



