from datetime import date
from django.contrib.auth.models import User
from rest_framework import viewsets, permissions
from .models import Survey, Question, QuestionOption, Response, Answer
from .serializers import \
    UserSerializer, SurveySerializer, QuestionSerializer, QuestionOptionSerializer, ResponseSerializer, AnswerSerializer


class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all().order_by('-date_joined')
    serializer_class = UserSerializer
    permission_classes = [permissions.IsAuthenticated]


class SurveyViewSet(viewsets.ModelViewSet):
    # queryset = Survey.objects.filter(end_date__gte=date.today())
    queryset = Survey.objects.all()
    serializer_class = SurveySerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

    def filter_queryset(self, queryset):
        for key, value in self.request.query_params.items():
            print(key, value)
            # queryset = queryset.filter(**{key: value})
        return queryset


class QuestionViewSet(viewsets.ModelViewSet):
    queryset = Question.objects.all()
    serializer_class = QuestionSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]


class QuestionOptionViewSet(viewsets.ModelViewSet):
    queryset = QuestionOption.objects.all()
    serializer_class = QuestionOptionSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]


class ResponseViewSet(viewsets.ModelViewSet):
    queryset = Response.objects.all()
    serializer_class = ResponseSerializer
    permission_classes = [permissions.IsAuthenticated]


class AnswerViewSet(viewsets.ModelViewSet):
    queryset = Answer.objects.all()
    serializer_class = AnswerSerializer
    permission_classes = [permissions.IsAuthenticated]
