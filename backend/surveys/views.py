from datetime import date
from rest_framework import viewsets, permissions
from .models import Survey, Question, QuestionOption, Result, Answer
from surveys import serializers


class SurveyViewSet(viewsets.ModelViewSet):
    queryset = Survey.objects.all()
    serializer_class = serializers.SurveySerializer

    def filter_queryset(self, queryset):
        for key, value in self.request.query_params.items():
            if key == 'actual':
                queryset = queryset.filter(end_date__gte=date.today())
        return queryset


class QuestionViewSet(viewsets.ModelViewSet):
    queryset = Question.objects.all()
    serializer_class = serializers.QuestionSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]


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
