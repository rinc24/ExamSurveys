from django.contrib import admin
from surveys.models import Survey, Question, QuestionOption, Response, Answer

for model in [Survey, Question, QuestionOption, Response, Answer]:
    admin.site.register(model)
