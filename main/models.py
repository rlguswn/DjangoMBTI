from django.db import models


# Create your models here.
class Mbti(models.Model):
    MBTI_CHOICES = [
        ('ISTJ', 'ISTJ'), ('ISFJ', 'ISFJ'), ('INFJ', 'INFJ'), ('INTJ', 'INTJ'),
        ('ISTP', 'ISTP'), ('ISFP', 'ISFP'), ('INFP', 'INFP'), ('INTP', 'INTP'),
        ('ESTP', 'ESTP'), ('ESFP', 'ESFP'), ('ENFP', 'ENFP'), ('ENTP', 'ENTP'),
        ('ESTJ', 'ESTJ'), ('ESFJ', 'ESFJ'), ('ENFJ', 'ENFJ'), ('ENTJ', 'ENTJ')
    ]
    mbti = models.CharField(max_length=16, unique=True, choices=MBTI_CHOICES)
    text = models.TextField()

    def __str__(self):
        return self.mbti


class Question(models.Model):
    DIMENSION_CHOICES = [
        ('EI', 'Extraversion/Introversion'),
        ('SN', 'Sensing/Intuition'),
        ('TF', 'Thinking/Feeling'),
        ('JP', 'Judging/Perceiving')
    ]
    text = models.TextField()
    dimension = models.CharField(max_length=2, choices=DIMENSION_CHOICES)

    def __str__(self):
        return self.text


class Option(models.Model):
    text = models.TextField()
    question = models.ForeignKey(to='main.Question', on_delete=models.CASCADE)
    score = models.IntegerField()

    def __str__(self):
        return f'{self.text} ({self.score})'
