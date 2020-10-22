from django.contrib import admin
from surveys.models import Survey, Question, QuestionOption, Result, Answer

for model in [Survey, Question, QuestionOption, Result, Answer]:
    admin.site.register(model)
