from django.db import DatabaseError
from django.core.exceptions import ObjectDoesNotExist
from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema
from rest_framework import status
from rest_framework.exceptions import ValidationError
from rest_framework.response import Response
from rest_framework.views import APIView

from main.Serializers import QuestionSerializer, MbtiSerializer
from main.models import Question, Option, Mbti
from main import swaggers as sw


# Create your views here.
class QuestionView(APIView):
    @swagger_auto_schema(
        operation_id='QustionView',
        operation_description='질문과 질문에 대한 선택지 불러오기',
        responses={
            status.HTTP_200_OK: openapi.Response(
                'Success', schema=sw.question_view_schema
            ),
            status.HTTP_400_BAD_REQUEST: openapi.Response(
                'Bad Request', schema=sw.status_400_schema
            ),
            status.HTTP_500_INTERNAL_SERVER_ERROR: openapi.Response(
                'Internal Server Error', schema=sw.status_500_schema
            )
        }
    )
    def get(self, request):
        try:
            queryset = Question.objects.prefetch_related('option_set').all()
            if not queryset.exists():
                return Response({"error": "No questions found in DB"}, status=status.HTTP_400_BAD_REQUEST)

            serializer = QuestionSerializer(queryset, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except DatabaseError:
            return Response(
                {"error": "Database error occurred while fetching questions."},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )

        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class MbtiView(APIView):
    @swagger_auto_schema(
        operation_id='MbtiView',
        operation_description='MBTI 테스트',
        request_body=sw.mbti_view_request_schema,
        responses={
            status.HTTP_200_OK: openapi.Response(
                'Success', schema=sw.mbti_view_schema
            ),
            status.HTTP_400_BAD_REQUEST: openapi.Response(
                'Bad Request', schema=sw.status_400_schema
            ),
            status.HTTP_500_INTERNAL_SERVER_ERROR: openapi.Response(
                'Internal Server Error', schema=sw.status_500_schema
            )
        }
    )
    def post(self, request):
        try:
            answers = request.data.get('answer')
            if not answers or not isinstance(answers, dict):
                return Response({"error": "Invalid format for 'answer'."},
                                status=status.HTTP_400_BAD_REQUEST)
            scores = {'EI': 0, 'SN': 0, 'TF': 0, 'JP': 0}

            for question_id, option_id in answers.items():
                try:
                    option = Option.objects.get(id=option_id)
                    dimension = option.question.dimension
                    scores[dimension] += option.score
                except ObjectDoesNotExist:
                    return Response(
                        {"error": f"Option_id '{option_id}' does not exist."},
                        status=status.HTTP_400_BAD_REQUEST
                    )

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
