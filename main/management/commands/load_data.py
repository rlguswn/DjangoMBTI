import json

from django.core.management.base import BaseCommand
from main.models import Question, Option, Mbti


class Command(BaseCommand):
    help = '시드 데이터 불러오기'

    def handle(self, *args, **options):
        with open('main/fixtures/seed_data.json', 'r', encoding='utf-8') as jsonfile:
            data = json.load(jsonfile)
            count = 0
            for q in data['question']:
                question, created = Question.objects.get_or_create(
                    text=q['text'],
                    dimension=q['dimension']
                )
                count += 1

                for o in q['options']:
                    Option.objects.create(
                        question=question,
                        text=o['text'],
                        score=o['score']
                    )
                    count += 1

            for m in data['mbti']:
                Mbti.objects.create(
                    mbti=m['mbti'],
                    text=m['text']
                )
                count += 1

        self.stdout.write(self.style.SUCCESS(f'{count}개의 데이터가 성공적으로 추가되었습니다.'))
