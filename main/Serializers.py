from rest_framework import serializers

from main.models import Question, Option, Mbti


class OptionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Option
        fields = '__all__'


class QuestionSerializer(serializers.ModelSerializer):
    options = OptionSerializer(many=True, read_only=True, source='option_set')

    class Meta:
        model = Question
        fields = '__all__'


class MbtiSerializer(serializers.ModelSerializer):
    class Meta:
        model = Mbti
        fields = '__all__'
