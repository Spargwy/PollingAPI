from polling.models import Poll, Question, Answer
from rest_framework import serializers


class QuestionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Question
        fields = ('id', 'title', 'description', 'type')


class PollSerializer(serializers.ModelSerializer):
    questions = QuestionSerializer(many=True)

    class Meta:
        model = Poll
        fields = ['id', 'name', 'start_date', 'finish_date', 'questions']


class UserAnswerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Answer
        fields = ('question', '')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['question'].queryset = self.context['poll'].questions.all()
