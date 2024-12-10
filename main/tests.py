from django.core.management import call_command
from django.test import TestCase
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
