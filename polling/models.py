from django.db import models
from django.contrib.auth.models import User
from django.contrib.auth import get_user_model


class Poll(models.Model):
    name = models.CharField(max_length=100)
    start_date = models.DateTimeField()
    finish_date = models.DateTimeField()
    description = models.TextField()

    def __str__(self):
        return self.name


class Question(models.Model):
    class Types(models.TextChoices):
        single = 'single'
        multiple = 'multiple'
        text = 'text'

    poll = models.ForeignKey(Poll, on_delete=models.CASCADE, related_name='questions')
    title = models.CharField(max_length=150)
    type = models.CharField(choices=Types.choices, max_length=8, default=Types.single)
    description = models.TextField(default="")

    def __str__(self):
        return self.title


class Choice(models.Model):
    question = models.ForeignKey(Question, on_delete=models.CASCADE, related_name='choices')
    title = models.CharField(max_length=200)

    def __str__(self):
        return self.title


class Answer(models.Model):
    user = models.ForeignKey(get_user_model(), on_delete=models.CASCADE, null=True, blank=True, related_name='answers')
    poll = models.ForeignKey(Poll, models.CASCADE, related_name='answers')
    question = models.ForeignKey(Question, models.CASCADE, related_name='answers')
    choices = models.ManyToManyField(Choice, related_name='answers', blank=True)
    choice_text = models.TextField(null=True, blank=True)

    def __str__(self):
        return self.user
