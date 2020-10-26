from datetime import date
from rest_framework.decorators import action, permission_classes
from rest_framework import viewsets, permissions
from .models import Survey, Question, QuestionOption, Result, Answer
from surveys import serializers


class SurveyViewSet(viewsets.ModelViewSet):
    queryset = Survey.objects.all()
    serializer_class = serializers.SurveySerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]


    @action(detail=False)
    def active(self, request):
        "Возвращает список активных опросов (дата окончания больше или равна сегодняшней)"
        self.queryset = self.queryset.filter(end_date__gte=date.today())
        return self.list(self, request)
    #
    # @action(detail=True)
    # def survey(self):
    #     pass


class QuestionViewSet(viewsets.ModelViewSet):
    queryset = Question.objects.all()
    serializer_class = serializers.QuestionSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

    def get_queryset(self):
        """Метод переопределен для поддержки самостоятельной (domain.com/questions)
        и вложенной (domain.com/surveys/1/questions) сериализации"""
        if 'survey_pk' in self.kwargs:
            self.queryset = self.queryset.filter(survey=self.kwargs['survey_pk'])
            return super(QuestionViewSet, self).get_queryset()
        else:
            return super(QuestionViewSet, self).get_queryset()


class QuestionOptionViewSet(viewsets.ModelViewSet):
    queryset = QuestionOption.objects.all()
    serializer_class = serializers.QuestionOptionSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]


class ResultViewSet(viewsets.ModelViewSet):
    queryset = Result.objects.all()
    serializer_class = serializers.ResultSerializer
    permission_classes = [permissions.IsAuthenticated]


class AnswerViewSet(viewsets.ModelViewSet):
    queryset = Answer.objects.all()
    serializer_class = serializers.AnswerSerializer
    permission_classes = [permissions.IsAuthenticated]
