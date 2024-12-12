from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from main.Serializers import QuestionSerializer, MbtiSerializer
from main.models import Question, Option


# Create your views here.
class QuestionView(APIView):
    def get(self, request):
        queryset = Question.objects.prefetch_related('option_set').all()
        serializer = QuestionSerializer(queryset, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

