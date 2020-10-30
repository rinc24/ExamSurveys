from django.contrib import admin
from surveys.models import Survey, Question, QuestionOption, Result, Answer


class QuestionInline(admin.TabularInline):
    model = Question
    extra = 0


class QuestionOptionInline(admin.TabularInline):
    model = QuestionOption
    extra = 0


class AnswerInline(admin.TabularInline):
    model = Answer
    extra = 0


@admin.register(Survey)
class SurveyAdmin(admin.ModelAdmin):
    list_display = ['name', 'description', 'start_date', 'end_date']
    list_filter = ['start_date', 'end_date']
    fieldsets = (
        (None, {
            'fields': ('name', 'description')
        }),
        ('Период', {
            'fields': ('start_date', 'end_date')
        })
    )
    inlines = [QuestionInline]


@admin.register(Question)
class QuestionAdmin(admin.ModelAdmin):
    list_display = ['text', 'type', 'survey']
    list_filter = ['type', 'survey']
    inlines = [QuestionOptionInline]


@admin.register(QuestionOption)
class QuestionOptionAdmin(admin.ModelAdmin):
    list_display = ['text', 'question']
    list_filter = ['question']


@admin.register(Result)
class ResultAdmin(admin.ModelAdmin):
    list_display = ['user_id', 'survey']
    list_filter = ['user_id', 'survey']
    inlines = [AnswerInline]


@admin.register(Answer)
class AnswerAdmin(admin.ModelAdmin):
    list_display = ['question', 'text', 'display_question_options', 'result']
    list_filter = ['question', 'text', 'result']
