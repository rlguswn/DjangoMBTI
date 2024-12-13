from django.urls import path

from main.views import QuestionView, MbtiView

urlpatterns = [
    # 질문과 선택지 불러오기
    path('question/', QuestionView.as_view()),

    # 답변 제출후 결과 반환
    path('submit/', MbtiView.as_view()),
]
