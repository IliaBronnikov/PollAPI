from django.contrib.auth.models import User
from rest_framework import serializers

from .models import Form, Question, Choice


class UserSerializer(serializers.ModelSerializer):
    forms = serializers.PrimaryKeyRelatedField(many=True, queryset=Form.objects.all())

    class Meta:
        model = User
        fields = ("id", "username", "forms")


class ChoiceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Choice
        fields = ("id", "choice_text")


class QuestionSerializer(serializers.ModelSerializer):
    choices = ChoiceSerializer(
        many=True,
    )

    class Meta:
        model = Question
        fields = "__all__"


class FormSerializer(serializers.ModelSerializer):
    class Meta:
        model = Form
        fields = ("pk", "title", "description", "start_at", "end_at")


class FormExtendedSerializer(serializers.ModelSerializer):
    questions = QuestionSerializer(
        many=True,
    )

    class Meta:
        model = Form
        fields = ("pk", "title", "description", "start_at", "end_at", "questions")


class TextAnswerSerializer(serializers.Serializer):
    user_id = serializers.IntegerField()
    answer_text = serializers.CharField()


class ChoiceAnswerSerializer(serializers.Serializer):
    user_id = serializers.IntegerField()
    answer_id = serializers.IntegerField()


class MultipleChoiceAnswerSerializer(serializers.Serializer):
    user_id = serializers.IntegerField()
    answers_id = serializers.IntegerField()


class AnswerSerializer(serializers.Serializer):
    user_id = serializers.IntegerField()
    choice_id = serializers.IntegerField(required=False)
    answer_text = serializers.CharField(required=False)
    choice_ids = serializers.ListField(
        child=serializers.IntegerField(min_value=0, max_value=100), required=False
    )
