from rest_framework import serializers

from main.models import Question, Option, Mbti


class OptionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Option
        fields = ['id', 'text']


class QuestionSerializer(serializers.ModelSerializer):
    options = OptionSerializer(many=True, read_only=True, source='option_set')

    class Meta:
        model = Question
        fields = ['id', 'text', 'options']


class MbtiSerializer(serializers.ModelSerializer):
    class Meta:
        model = Mbti
        fields = ['mbti', 'text']
