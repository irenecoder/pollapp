from django.db import models
from django.utils import timezone
import datetime
from django.contrib import admin

# Create your models here.
class Question(models.Model):
    quiz_text = models.CharField(max_length=200)
    date_created = models.DateTimeField()

    def __str__(self):
        return self.quiz_text
    @admin.display(
        boolean=True,
        ordering= 'date_created',
        description = 'Published recently?',
    )
    def was_published_recently(self):
        now = timezone.now()
        return now - datetime.timedelta(days=1)<= self.date_created <= now

class Choice(models.Model):
    question = models.ForeignKey(Question,on_delete=models.CASCADE,default=1)
    choice_text = models.CharField(max_length=200)
    votes = models.IntegerField(default=0)
    

    def __str__(self):
        return self.choice_text


