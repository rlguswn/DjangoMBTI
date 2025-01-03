from django.core.management import call_command
from django.test import TestCase
from rest_framework import status
from rest_framework.test import APITestCase

from main.models import Question, Option, Mbti


# Create your tests here.
class QuestionModelTest(TestCase):
    def test_create_question(self):
        question = Question.objects.create(
            text="나는 사람들과 함께 있는 것을 즐기며 에너지를 얻는다.",
            dimension="EI"
        )

        self.assertEqual(question.text, "나는 사람들과 함께 있는 것을 즐기며 에너지를 얻는다.")
        self.assertEqual(question.dimension, "EI")
        self.assertTrue(Question.objects.filter(id=question.id).exists())


class OptionModelTest(TestCase):
    def test_create_option(self):
        question = Question.objects.create(
            text="나는 사람들과 함께 있는 것을 즐기며 에너지를 얻는다.",
            dimension="EI"
        )

        option = Option.objects.create(
            question=question,
            text="그렇다.",
            score=1
        )

        self.assertEqual(option.question, question)
        self.assertEqual(option.text, "그렇다.")
        self.assertEqual(option.score, 1)


class MbtiModelTest(TestCase):
    def test_create_mbti(self):
        mbti = Mbti.objects.create(
            mbti="ESTJ",
            text="ESTJ에 대한 설명입니다."
        )

        self.assertEqual(mbti.mbti, "ESTJ")
        self.assertEqual(mbti.text, "ESTJ에 대한 설명입니다.")
        self.assertTrue(Mbti.objects.filter(id=mbti.id).exists())


class SeedDataTest(TestCase):
    def setUp(self):
        call_command('load_data')

    def test_question_data_loaded(self):
        question = Question.objects.first()

        self.assertIsNotNone(question)

    def test_option_data_loaded(self):
        question = Question.objects.first()
        options = Option.objects.filter(question=question)

        self.assertEqual(options.count(), 2)
        self.assertEqual(abs(options.first().score), 1)

    def test_mbti_data_loaded(self):
        mbti = Mbti.objects.first()

        self.assertIsNotNone(mbti)
        self.assertEqual(len(mbti.mbti), 4)


class QuestionViewTest(APITestCase):
    def setUp(self):
        call_command('load_data')

    def test_get_questions(self):
        response = self.client.get('/mbti/question/')

        self.assertEqual(response.status_code, status.HTTP_200_OK)

        self.assertIsNotNone(response.data)
        self.assertEqual(len(response.data[0]['options']), 2)

    def test_get_questions_empty(self):
        Question.objects.all().delete()

        response = self.client.get('/mbti/question/')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.data, {"error": "No questions found in DB"})


class MbtiViewTest(APITestCase):
    def setUp(self):
        question1 = Question.objects.create(text="EI에 대한 질문", dimension="EI")
        option1 = Option.objects.create(text="E", question=question1, score=1)
        Option.objects.create(text="I", question=question1, score=-1)

        question2 = Question.objects.create(text="SN에 대한 질문", dimension="SN")
        option2 = Option.objects.create(text="S", question=question2, score=1)
        Option.objects.create(text="N", question=question1, score=-1)

        question3 = Question.objects.create(text="TF에 대한 질문", dimension="TF")
        option3 = Option.objects.create(text="T", question=question3, score=1)
        Option.objects.create(text="F", question=question1, score=-1)

        question4 = Question.objects.create(text="JP에 대한 질문", dimension="JP")
        option4 = Option.objects.create(text="J", question=question4, score=1)
        Option.objects.create(text="P", question=question1, score=-1)

        mbti = Mbti.objects.create(mbti="ESTJ", text="엄격한 관리자, 경영자")

        self.valid_answers = {
            str(question1.id): option1.id,
            str(question2.id): option2.id,
            str(question3.id): option3.id,
            str(question4.id): option4.id,
        }

    def test_submit_valid_answers(self):
        response = self.client.post('/mbti/submit/', {'answer': self.valid_answers}, format='json')

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('mbti', response.data)
        self.assertEqual(response.data['mbti'], 'ESTJ')

    def test_submit_invalid_answers(self):
        response = self.client.post('/mbti/submit/', {'answer': 'invalid'}, format='json')

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.data, {"error": "Invalid format for 'answer'."})

    def test_submit_nonexistent_option_id(self):
        invalid_answers = self.valid_answers.copy()
        invalid_answers[list(invalid_answers.keys())[0]] = 9999

        response = self.client.post('/mbti/submit/', {'answer': invalid_answers}, format='json')

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.data, {"error": "Option_id '9999' does not exist."})

    def test_submit_nonexistent_mbti_result(self):
        invalid_answers = self.valid_answers.copy()
        invalid_answers[list(invalid_answers.keys())[0]] = Option.objects.filter(score=-1).first().id

        response = self.client.post('/mbti/submit/', {'answer': invalid_answers}, format='json')

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.data, {"error": "MBTI 'ISTJ' does not exist."})
