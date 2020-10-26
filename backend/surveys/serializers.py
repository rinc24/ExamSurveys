from rest_framework import serializers
from surveys.models import Survey, Question, QuestionOption, Result, Answer


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
    questions = QuestionSerializer(many=True, required=False) # поле отношений

    class Meta:
        model = Survey
        fields = '__all__'

    def __init__(self, *args, **kwargs):
        """Метод переопределен для динамической сериализации поля отношений questions"""
        super(SurveySerializer, self).__init__(*args, **kwargs)
        # Если запрос не детальный (например список), то
        if not self.context['view'].detail and 'questions' in self.fields:
            del self.fields['questions']

    def create(self, validated_data):
        """Метод переопределен для поддержки вложенной сериализации"""
        question_list = validated_data.pop('questions', [])
        new_survey = Survey.objects.create(**validated_data)
        # Создаем вопросы
        for question in question_list:
            question_option_list = question.pop('question_options', [])
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

    class Meta:
        model = Result
        fields = '__all__'
