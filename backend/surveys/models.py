from datetime import date
from django.db import models


class Survey(models.Model):
    id = models.AutoField(
        primary_key=True, db_column='survey_id'
    )

    name = models.CharField(
        verbose_name='Название опроса', max_length=127,
        help_text='Например: Опрос о качестве услуг',
        null=False, blank=True, default='Опрос',
        db_column='survey_name'
    )

    start_date = models.DateField(
        verbose_name="Дата начала",
        editable=False,
        null=False, blank=True, default=date.today,
        db_column='survey_start_date'
    )

    end_date = models.DateField(
        verbose_name="Дата окончания",
        null=True, blank=True, default=None,
        db_column='survey_end_date'
    )

    description = models.TextField(
        verbose_name='Описание', max_length=1024,
        help_text='Например: Сбор обратной связи от сотрудников Компании',
        null=True, blank=True, default=None,
        db_column='survey_description'
    )

    def __str__(self):
        return str(self.name)

    class Meta:
        ordering = ['start_date', 'name']
        db_table = 'survey'
        verbose_name = 'Опрос'
        verbose_name_plural = 'Опросы'


class Question(models.Model):
    id = models.AutoField(
        primary_key=True,
        db_column='question_id'
    )

    survey = models.ForeignKey(
        verbose_name='Опрос',
        to=Survey, on_delete=models.CASCADE,
        related_name='questions',
        null=False, blank=False, default=None,
        db_column='survey_id'
    )

    QUESTION_TYPE_CHOICES = [
        ('text', 'Ответ текстом'),
        ('radio', 'Ответ с выбором одного варианта'),
        ('checkbox', 'Ответ с выбором нескольких вариантов')
    ]

    type = models.CharField(
        verbose_name='Тип ответа на вопрос', max_length=8,
        help_text='Например: radio',
        choices=QUESTION_TYPE_CHOICES,
        null=False, blank=False, default='text',
        db_column='question_type'
    )

    text = models.TextField(
        verbose_name='Текст вопроса', max_length=127,
        help_text='Например: Есть ли у Вас замечания?',
        null=False, blank=False, default=None,
        db_column='question_text'
    )

    def __str__(self):
        return str(self.text)

    class Meta:
        ordering = ['survey', 'id']
        db_table = 'question'
        verbose_name = 'Вопрос'
        verbose_name_plural = 'Вопросы'


class QuestionOption(models.Model):
    id = models.AutoField(
        primary_key=True,
        db_column='question_option_id'
    )

    question = models.ForeignKey(
        verbose_name='Вопрос',
        to=Question, on_delete=models.CASCADE,
        related_name='question_options',
        null=False, blank=False, default=None,
        db_column='question_id'
    )

    text = models.TextField(
        verbose_name='Текст варианта ответа', max_length=127,
        help_text='Например: Скорее положительно',
        null=False, blank=False, default=None,
        db_column='question_option_text'
    )

    def __str__(self):
        return str(self.text)

    class Meta:
        ordering = ['question', 'id']
        db_table = 'question_option'
        verbose_name = 'Вариант ответа'
        verbose_name_plural = 'Варианты ответа'


class Response(models.Model):
    id = models.AutoField(
        primary_key=True,
        db_column='response_id'
    )

    survey = models.ForeignKey(
        verbose_name='Опрос',
        to=Survey, on_delete=models.CASCADE,
        related_name='responses',
        null=False, blank=False, default=None,
        db_column='survey_id'
    )

    user_id = models.IntegerField(
        verbose_name='Идентификатор анонимного пользователя',
        help_text='Например: 1234',
        null=False, blank=False, default=None,
        db_column='response_user_id'
    )

    def __str__(self):
        return f'{self.survey} (User: {self.user_id})'

    class Meta:
        ordering = ['survey', 'id']
        db_table = 'response'
        verbose_name = 'Результат'
        verbose_name_plural = 'Результаты'


class Answer(models.Model):
    id = models.AutoField(
        primary_key=True,
        db_column='answer_id'
    )

    response = models.ForeignKey(
        verbose_name='Результат',
        to=Response, on_delete=models.CASCADE,
        related_name='answers',
        null=False, blank=False, default=None,
        db_column='response_id'
    )

    question = models.ForeignKey(
        verbose_name='Вопрос',
        to=Question, on_delete=models.CASCADE,
        related_name='answer',
        null=False, blank=False, default=None,
        db_column='question_id'
    )

    question_option = models.ForeignKey(
        verbose_name='Вариант ответа',
        to=QuestionOption, on_delete=models.CASCADE,
        related_name='answer',
        null=True, blank=True, default=None,
        db_column='question_option_id'
    )

    text = models.TextField(
        verbose_name='Текст ответа', max_length=255,
        help_text='Например: Замечаний нет',
        null=True, blank=True, default=None,
        db_column='answer_text'
    )

    def __str__(self):
        return f'{self.question} -- {self.text or self.question_option}'

    class Meta:
        ordering = ['response', 'question']
        db_table = 'answer'
        verbose_name = 'Ответ'
        verbose_name_plural = 'Ответы'
