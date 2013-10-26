from django.db import models
from django.contrib.auth.models import User

# Create your models here.

class Exam(models.Model):
	name = models.CharField(max_length=64)

class QuestionGroup(models.Model):
	exams = models.ManyToManyField(Exam)

class Question(models.Model):
	group_id = models.ForeignKey(QuestionGroup)
	text = models.CharField(max_length=512)

class Choice(models.Model):
	question_id = models.ForeignKey(Question)
	text = models.CharField(max_length=512)

class ExamInstance(models.Model):
	user_id = models.ForeignKey(User)

class QuestionInstance(models.Model):
	exam_id = models.ForeignKey(ExamInstance)
	choice_id = models.ForeignKey(Choice)



