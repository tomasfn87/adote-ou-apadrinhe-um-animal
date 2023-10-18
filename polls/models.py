from django.db import models
from django.utils import timezone as tz
import datetime as dt

class Question(models.Model):
    def __str__(self):
        return self.question_text

    def was_published_recently(self):
        now = tz.now()
        return now - dt.timedelta(days=1) <= self.pub_date <= now

    question_text = models.CharField(max_length=200)
    pub_date = models.DateTimeField("date published")


class Choice(models.Model):
    def __str__(self):
        return self.choice_text

    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    choice_text = models.CharField(max_length=200)
    votes = models.IntegerField(default=0)
