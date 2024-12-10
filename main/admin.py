from django.contrib import admin

from main.models import Question, Option, Mbti


# Register your models here.
@admin.register(Mbti)
class MbtiAdmin(admin.ModelAdmin):
    list_display = ('mbti', 'text')
    search_fields = ('mbti', 'text')
    ordering = ('mbti',)


@admin.register(Question)
class QuestionAdmin(admin.ModelAdmin):
    list_display = ('dimension', 'text')
    search_fields = ('dimension', 'text')
    ordering = ('dimension',)


@admin.register(Option)
class OptionAdmin(admin.ModelAdmin):
    list_display = ('question', 'text', 'score')
    search_fields = ('question', 'text', 'score')
    ordering = ('question', 'score')
