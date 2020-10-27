from rest_framework import serializers, validators
from surveys.models import Survey, Question, QuestionOption, Result, Answer
from datetime import date


class QuestionOptionSerializer(serializers.HyperlinkedModelSerializer):
    """Сериализатор варианта ответа"""
    def to_internal_value(self, data):
        """Перехват переданных сериализатору данных для возможности передавать
        question_options в api как список строк ["Вариант 1", "Вариант 2"]
        Переводит строки в объекты question_option"""
        if isinstance(data, str):
            data = {'text': data}

        return super(QuestionOptionSerializer, self).to_internal_value(data)

    class Meta:
        model = QuestionOption
        fields = '__all__'


class QuestionSerializer(serializers.HyperlinkedModelSerializer):
    """Сериализатор вопроса"""
    question_options = QuestionOptionSerializer(many=True, required=False)

    class Meta:
        model = Question
        fields = '__all__'


class SurveySerializer(serializers.HyperlinkedModelSerializer):
    """Сериализатор опроса"""
    questions = QuestionSerializer(many=True, required=False)  # поле отношений

    def validate(self, attrs):
        """Валидация опросов"""
        # Валидация дат начала и окончания при создании и обновлении
        if self.instance:  # если есть состояние (при обновлении)
            start_date = self.instance.start_date  # Не берется из attrs, т.к. дата начала не изменяется при обновлении
            end_date = attrs.get('end_date', self.instance.end_date)
        else:  # если состояния нет (при создании)
            print(attrs.get('start_date', 123))
            start_date = attrs.get('start_date', date.today())
            end_date = attrs.get('end_date', None)

        if end_date:
            if start_date > end_date:
                raise serializers.ValidationError(
                    f'Дата окончания опроса {end_date} не может быть раньше даты начала {start_date}.'
                )

        return attrs

    class Meta:
        model = Survey
        fields = '__all__'
        validators = []

    def __init__(self, *args, **kwargs):
        """Метод переопределен для динамической сериализации поля отношений questions"""
        super(SurveySerializer, self).__init__(*args, **kwargs)
        # Если запрос не детальный (например список), то
        if not self.context['view'].detail and 'questions' in self.fields:
            del self.fields['questions']

    def create(self, validated_data):
        """Метод переопределен для поддержки вложенной сериализации"""
        question_list = validated_data.pop('questions', [])  # изымаем вопросы (otm related field)
        new_survey = Survey.objects.create(**validated_data)
        # Создаем вопросы
        for question in question_list:
            question_option_list = question.pop('question_options', [])  # изымаем варианты ответов (otm related field)
            new_question = Question.objects.create(survey=new_survey, **question)
            # Создаем варианты ответов
            for question_option in question_option_list:
                QuestionOption.objects.create(question=new_question, **question_option)

        return new_survey
    
    def update(self, instance, validated_data):
        """Поле start_date недоступно для редактирования, только для создания"""
        if 'start_date' in validated_data.keys():
            del validated_data['start_date']

        return super(SurveySerializer, self).update(instance, validated_data)


class AnswerSerializer(serializers.HyperlinkedModelSerializer):
    """Сериализатор ответа"""
    class Meta:
        model = Answer
        fields = '__all__'


class ResultSerializer(serializers.HyperlinkedModelSerializer):
    """Сериализатор результата"""
    answers = AnswerSerializer(many=True, required=False)

    def create(self, validated_data):
        """Метод переопределен для поддержки вложенной сериализации"""
        answer_list = validated_data.pop('answers', [])  # изымаем ответы (otm related field)
        new_result = Result.objects.create(**validated_data)
        # Создаем ответы
        for answer in answer_list:
            question_options = answer.pop('question_options', [])  # изымаем вариенты ответов (mtm related field)
            new_answer = Answer.objects.create(result=new_result, **answer)
            # Добавлеяем выбранные вариенты ответа к ответу
            for question_option in question_options:
                new_answer.question_options.add(question_option)

        return new_result

    class Meta:
        model = Result
        fields = '__all__'
