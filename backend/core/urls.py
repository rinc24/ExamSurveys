from django.contrib import admin
from django.urls import path, include
from rest_framework import routers
from surveys import views

router = routers.DefaultRouter()
router.register(r'users', views.UserViewSet)
router.register(r'surveys', views.SurveyViewSet)
router.register(r'question_options', views.QuestionOptionViewSet)
router.register(r'responses', views.ResponseViewSet)
router.register(r'answers', views.AnswerViewSet)

urlpatterns = [
    path('', include(router.urls)),
    path('admin/', admin.site.urls),
    path('api-auth/', include('rest_framework.urls', namespace='rest_framework'))
]
