from django.db import models
from django.contrib.auth.models import User


class Poll(models.Model):
    name = models.CharField(max_length=100)
    start_date = models.TimeField()
    finish_date = models.TimeField()
    description = models.TextField()

    def __str__(self):
        return self.name


class Question(models.Model):
    class Types(models.TextChoices):
        single = 'single'
        multiple = 'multiple'
        text = 'text'

    title = models.CharField(max_length=150)
    type = models.CharField(choices=Types.choices, max_length=8, default=Types.single)
    description = models.TextField(default="")
    poll = models.ForeignKey(Poll, on_delete=models.CASCADE, related_name='questions')

    def __str__(self):
        return self.title


class Choice(models.Model):
    question = models.ForeignKey(Question, on_delete=models.DO_NOTHING)
    title = models.CharField(max_length=200)
    lock_other = models.BooleanField(default=False)

    def __str__(self):
        return self.title


class Answer(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    poll = models.ForeignKey(Poll, models.CASCADE)
    question = models.ForeignKey(Question, models.CASCADE)
    choice = models.ForeignKey(Choice, on_delete=models.DO_NOTHING)
    question_text = models.TextField(null=True, blank=True)

    def __str__(self):
        return self.question_text
