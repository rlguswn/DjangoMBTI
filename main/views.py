from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from main.Serializers import QuestionSerializer, MbtiSerializer
from main.models import Question, Option, Mbti


# Create your views here.
class QuestionView(APIView):
    def get(self, request):
        queryset = Question.objects.prefetch_related('option_set').all()
        serializer = QuestionSerializer(queryset, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


class MbtiView(APIView):
    def post(self, request):
        answers = request.data.get('answer')
        scores = {'EI': 0, 'SN': 0, 'TF': 0, 'JP': 0}

        for question_id, option_id in answers.items():
            option = Option.objects.get(id=option_id)
            dimension = option.question.dimension
            scores[dimension] += option.score

        mbti = ''
        for dimension, score in scores.items():
            if score > 0:
                mbti += dimension[0]
            elif score < 0:
                mbti += dimension[1]

        queryset = Mbti.objects.get(mbti=mbti)
        serializer = MbtiSerializer(queryset)
        return Response(serializer.data, status=status.HTTP_200_OK)
