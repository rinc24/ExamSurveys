from django.contrib import admin
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from rest_framework_nested.routers import NestedSimpleRouter
from surveys import views

router = DefaultRouter()
router.register(r'surveys', views.SurveyViewSet)
router.register(r'questions', views.QuestionViewSet)
router.register(r'question_options', views.QuestionOptionViewSet)
router.register(r'results', views.ResultViewSet)
router.register(r'answers', views.AnswerViewSet)

surveys_router = NestedSimpleRouter(router, r'surveys', lookup='survey')
surveys_router.register(r'questions', views.QuestionViewSet)

urlpatterns = [
    path('', include(router.urls)),
    path('', include(surveys_router.urls)),
    path('admin/', admin.site.urls),
    path('api-auth/', include('rest_framework.urls', namespace='rest_framework')),
]
