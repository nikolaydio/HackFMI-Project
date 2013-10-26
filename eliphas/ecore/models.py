from django.db import models

# Create your models here.

class Exam(models.Model):
	name = models.CharField(max_length=64)
	
class Question(models.Model):
	text = models.CharField(max_lenght=512)

class Choice(models.Model):
	question_id = models.ForeigKey(Question)
	text = models.CharField(max_length=512)


