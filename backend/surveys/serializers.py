from rest_framework import serializers
from surveys.models import Survey, Question, QuestionOption, Result, Answer


class QuestionOptionSerializer(serializers.HyperlinkedModelSerializer):

    def to_internal_value(self, data):
        """
        Перехват переданных сериализатору данных для возможности передавать
        question_options в api как список строк ["Вариант 1", "Вариант 2"].
        """
        if isinstance(data, str):
            data = {'text': data}
        return super(QuestionOptionSerializer, self).to_internal_value(data)

    class Meta:
        model = QuestionOption
        fields = '__all__'


class QuestionSerializer(serializers.HyperlinkedModelSerializer):
    question_options = QuestionOptionSerializer(many=True, required=False)

    class Meta:
        model = Question
        fields = '__all__'


class SurveySerializer(serializers.HyperlinkedModelSerializer):
    questions = QuestionSerializer(many=True, required=False)

    class Meta:
        model = Survey
        fields = '__all__'

    def create(self, validated_data):
        question_list = validated_data.pop('questions')
        new_survey = Survey.objects.create(**validated_data)
        for question in question_list:
            question_option_list = question.pop('question_options')
            new_question = Question.objects.create(survey=new_survey, **question)
            for question_option in question_option_list:
                QuestionOption.objects.create(question=new_question, **question_option)
        return new_survey


class AnswerSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Answer
        fields = '__all__'


class ResultSerializer(serializers.HyperlinkedModelSerializer):
    answers = AnswerSerializer(many=True, required=False)

    class Meta:
        model = Result
        fields = '__all__'
