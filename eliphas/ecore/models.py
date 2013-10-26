from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone

# Create your models here.

class Exam(models.Model):
	name = models.CharField(max_length=64)
	duration = models.IntegerField()
	allowed_users = models.ManyToManyField(User)

	def TakeExam(self, user):
		exam = user.exams.create(exam=self, starttime=timezone.now())
		# todo: choose some random questions
		for group in self.questiongroup_set.all():
			for question in group.questions.all():
				exam.questions.create(question=question, choice=None)
		return exam

	def __unicode__(self):
		return self.name


class QuestionGroup(models.Model):
	exams = models.ManyToManyField(Exam, through='ExamQuestionGroupLink')


class ExamQuestionGroupLink(models.Model):
	exam = models.ForeignKey(Exam)
	questiongroup = models.ForeignKey(QuestionGroup)
	number = models.IntegerField()


class Question(models.Model):
	group = models.ForeignKey(QuestionGroup, related_name='questions')
	text = models.CharField(max_length=512)

	def __unicode__(self):
		return self.text


class Choice(models.Model):
	question = models.ForeignKey(Question, related_name='choices')
	text = models.CharField(max_length=512)

	def __unicode__(self):
		return self.text


class ExamInstance(models.Model):
	starttime = models.DateTimeField()
	endtime = models.DateTimeField(null=True, default=None)
	exam = models.ForeignKey(Exam, related_name='instances')
	user = models.ForeignKey(User, related_name='exams')

	def __unicode__(self):
		return str(self.user) + ": " + str(self.exam)


class QuestionInstance(models.Model):
	examinstance = models.ForeignKey(ExamInstance, related_name='questions')
	question = models.ForeignKey(Question)
	choice = models.ForeignKey(Choice, null=True)

	def __unicode__(self):
		return str(self.examinstance) + " -- " + str(self.question) + ": " + str(self.choice)

