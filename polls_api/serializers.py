from rest_framework import serializers
from rest_flex_fields import FlexFieldsModelSerializer
from .models import Poll, Question, Choice, Answer, AnswerType


class PollsSerializer(FlexFieldsModelSerializer):
    def validate(self, data):
        try:
            if Poll.objects.get(pk=self.instance.pk).date_start:
                raise serializers.ValidationError("Polls with defined start date are immutable")
        except AttributeError:
            pass
        return data

    class Meta:
        model = Poll
        fields = '__all__'


class QuestionSerializer(FlexFieldsModelSerializer):
    poll = serializers.PrimaryKeyRelatedField(queryset=Poll.objects.all())

    class Meta:
        model = Question
        fields = '__all__'
        expandable_fields = {'poll': PollsSerializer}


class ChoiceSerializer(FlexFieldsModelSerializer):
    class Meta:
        model = Choice
        fields = '__all__'


class AnswerSerializer(FlexFieldsModelSerializer):
    question = serializers.PrimaryKeyRelatedField(queryset=Question.objects.all())
    choice = serializers.PrimaryKeyRelatedField(queryset=Choice.objects.all(), required=False, allow_null=True)

    def validate(self, data):
        question = data['question']
        user = data['user_id']
        user_answered_already = Answer.objects.filter(user_id=user, question=question)

        if user_answered_already:
            if question.type != AnswerType.MULTIPLE:
                raise serializers.ValidationError("This question does not support multiple answers")

        if question.type != AnswerType.TEXT and data['text']:
            raise serializers.ValidationError("This question accepts only predefined answers")

        if question.type == AnswerType.TEXT:
            if data['choice'] or not data['text']:
                raise serializers.ValidationError("This question accepts only text answers")

        return data

    class Meta:
        model = Answer
        fields = '__all__'
        expandable_fields = {'question': QuestionSerializer, 'choice': ChoiceSerializer}
