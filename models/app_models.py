from django.db import models

import datetime

def generate_id(entity):
    now = datetime.datetime.now()
    return entity+now.strftime("%Y%m%d%H%M%S%f")

class polls_list(models.Model):
    poll_id = models.CharField(name='poll_id', null=False, blank=False, max_length=25, default=generate_id('poll'), primary_key=True)
    poll_name = models.CharField(name='poll_name', null=False, blank=False, max_length=30)
    poll_description = models.CharField(name='poll_description', null=True, blank=True, max_length=50, default='-')
    creation_date = models.DateField(name='creation_date', null=False, blank=False, default=datetime.date.today)
    disabled = models.BooleanField(name='disabled', default=False)

class poll_questions(models.Model):
    poll_id = models.CharField(name='poll_id', null=False, blank=False, max_length=25)
    question_no = models.IntegerField(name='question_no', null=False, blank=False)
    question = models.CharField(name='question', null=False, blank=False, max_length=100)
    question_options = models.CharField(name='question_options', null=False, blank=False, max_length=1000)

    class Meta:
        constraints = [
            models.UniqueConstraint(fields = ['poll_id', 'question_no'], name = 'poll_questions_key')
        ]

class poll_responses(models.Model):
    poll_id = models.CharField(name='poll_id', null=False, blank=False, max_length=25)
    response_id = models.CharField(name='response_id', null=False, blank=False, max_length=25, default=generate_id('resp'))
    question_no = models.IntegerField(name='question_no', null=False, blank=False)
    answer = models.CharField(name='answer', null=False, blank=False, max_length=2)
