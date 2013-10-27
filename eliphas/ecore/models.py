from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone

# Create your models here.

class Exam(models.Model):
	name = models.CharField(max_length=64)
	visibility_starttime = models.DateTimeField(null=True, blank=True)
	visibility_endtime = models.DateTimeField(null=True, blank=True)
	fixed_start = models.DateTimeField(null=True, blank=True)
	duration = models.IntegerField()
	allowed_users = models.ManyToManyField(User, related_name='accessexams')
	tries = models.IntegerField(default=0)

	def CoolDuration(self):
		return self.duration
	
	def QuestionCount(self):
		count = 0
		for info in self.examquestiongrouplink_set.all():
			count += info.number
		return count

	def TakeExam(self, user):
		if self.fixed_start != None:
			exam_start_time = self.fixed_start
		else:
			exam_start_time = timezone.now()
		exam = user.exams.create(exam=self, starttime=exam_start_time)
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
	points = models.IntegerField(default=0)

	def __unicode__(self):
		return self.text


class ExamInstance(models.Model):
	starttime = models.DateTimeField()
	endtime = models.DateTimeField(null=True, blank=True, default=None)
	exam = models.ForeignKey(Exam, related_name='instances')
	user = models.ForeignKey(User, related_name='exams')

	def __unicode__(self):
		return str(self.user) + ": " + str(self.exam)
	def result(self):
		points = 0;
		for q in self.questions.all():
			if q.choice == None:
				continue
			points += q.choice.points
		return points
	def max_result(self):
		points = 0;
		for q in self.questions.all():
			a = [i.points for i in Choice.objects.filter(question=q.question)]
			if len(a) != 0:
				points += max(a)
		return points
	def finish_exam(self, force):
		flag = False
		if (self.exam.duration - (timezone.now() - self.starttime).seconds) <= 0:
			flag = True
		else:
			flag = False
		if force or flag:
			if self.endtime == None:
				self.endtime = timezone.now()
				self.save()
	#note: may return negative numbers
	def time_left(self):
		return self.exam.duration - (timezone.now() - self.starttime).seconds
	def has_ended(self):
		if self.time_left() <= 0 or self.endtime != None:
			return True
		return False


class QuestionInstance(models.Model):
	examinstance = models.ForeignKey(ExamInstance, related_name='questions')
	question = models.ForeignKey(Question)
	choice = models.ForeignKey(Choice, null=True, blank=True)

	def __unicode__(self):
		return str(self.examinstance) + " -- " + str(self.question) + ": " + str(self.choice)

