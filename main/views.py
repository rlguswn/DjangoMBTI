from django.db import DatabaseError
from django.core.exceptions import ObjectDoesNotExist
from rest_framework import status
from rest_framework.exceptions import ValidationError
from rest_framework.response import Response
from rest_framework.views import APIView

from main.Serializers import QuestionSerializer, MbtiSerializer
from main.models import Question, Option, Mbti


# Create your views here.
class QuestionView(APIView):
    def get(self, request):
        try:
            queryset = Question.objects.prefetch_related('option_set').all()
            if not queryset.exists():
                return Response({"erorr": "No questions found in DB"}, status=status.HTTP_400_BAD_REQUEST)

            serializer = QuestionSerializer(queryset, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except DatabaseError as e:
            return Response(
                {"error": "Database error occurred while fetching questions.", "details": str(e)},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )

        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class MbtiView(APIView):
    def post(self, request):
        try:
            answers = request.data.get('answer')
            if not answers or not isinstance(answers, dict):
                raise ValidationError("Invalid format for 'answer'.")
            scores = {'EI': 0, 'SN': 0, 'TF': 0, 'JP': 0}

            for question_id, option_id in answers.items():
                try:
                    option = Option.objects.get(id=option_id)
                    dimension = option.question.dimension
                    scores[dimension] += option.score
                except ObjectDoesNotExist:
                    return Response({"error": f"Option_id '{option_id}' does not exist."}, status=status.HTTP_400_BAD_REQUEST)

            mbti = ''
            for dimension, score in scores.items():
                if score > 0:
                    mbti += dimension[0]
                elif score < 0:
                    mbti += dimension[1]

            try:
                queryset = Mbti.objects.get(mbti=mbti)
                serializer = MbtiSerializer(queryset)
            except ObjectDoesNotExist:
                return Response({"error": f"MBTI '{mbti}' does not exist."}, status=status.HTTP_400_BAD_REQUEST)

            return Response(serializer.data, status=status.HTTP_200_OK)
        except ValidationError as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)

        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
