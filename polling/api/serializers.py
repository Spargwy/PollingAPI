from polling.models import Poll, Question, Choice, Answer
from rest_framework import serializers


class ChoiceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Choice
        fields = ['id', 'question', 'title']
        read_only_fields = ('question',)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # editable id only for existing objects for updating
        self.fields['id'].read_only = not bool(getattr(self.instance, 'id', False))


class QuestionSerializer(serializers.ModelSerializer):
    choices = ChoiceSerializer(many=True, required=False)

    class Meta:
        model = Question
        fields = ['id', 'title', 'description', 'type', 'choices']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # editable id only for existing objects for updating
        self.fields['id'].read_only = not bool(getattr(self.instance, 'id', False))

    def validate(self, attrs):
        if attrs['type'] == Question.Types.text and len(attrs['choices']):
            raise serializers.ValidationError('Choices are not allowed for type text')
        elif attrs['type'] in [Question.Types.single, Question.Types.multiple] and not len(attrs['choices']):
            raise serializers.ValidationError('Choices are required for this type')
        return attrs


class UserAnswerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Answer
        fields = ('question', 'choices', 'choice_text')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['question'].queryset = self.context['poll'].questions.all()

    def validate(self, attrs):
        if attrs['question'].type in [Question.Types.single, Question.Types.multiple]:
            if not attrs['choices']:
                raise serializers.ValidationError('This question type must have minimum one choice')

            elif attrs['question'].type == Question.Types.single and len(attrs['choices']) > 1:
                raise serializers.ValidationError('You cant choose more than one variant')

        elif not attrs['text']:
            raise serializers.ValidationError('This question type must have text field')
        return attrs


class PollSerializer(serializers.ModelSerializer):
    questions = QuestionSerializer(many=True)

    class Meta:
        model = Poll
        fields = (
            'id',
            'name',
            'start_date',
            'finish_date',
            'description',
            'questions',
        )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if getattr(self.instance, 'id', None):
            self.fields['start_date'].read_only = True

    def validate(self, attrs):
        if (start_date := attrs.get('start_date')) and attrs['finish_date'] <= start_date:
            raise serializers.ValidationError({
                'finish_date': 'Finish date should be later than start date'
            })
        return attrs

    def create(self, validated_data):
        questions = validated_data.pop('questions')
        poll = super().create(validated_data)
        for question in questions:
            choices = question.pop('choices', [])
            question = Question.objects.create(poll=poll, **question)
            for choice in choices:
                Choice.objects.create(question=question, **choice)
        return poll


class PollShortSerializer(serializers.ModelSerializer):
    class Meta:
        model = Poll
        fields = ('id', 'name', 'start_date', 'finish_date', 'description')


class QuestionShortSerializer(serializers.ModelSerializer):
    class Meta:
        model = Question
        fields = ('title', 'description', 'choices')


class UserAnswerListSerializer(serializers.ModelSerializer):
    poll = PollShortSerializer()
    question = QuestionShortSerializer()
    choices = ChoiceSerializer(many=True)

    class Meta:
        model = Answer
        fields = ('poll', 'question', 'choices', 'choice_text')
