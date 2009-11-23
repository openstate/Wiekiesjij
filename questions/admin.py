from django.contrib import admin

from questions.models import Question, QuestionSet, Answer


class QuestionAdmin(admin.ModelAdmin):
    pass

admin.site.register(Question, QuestionAdmin)

class QuestionSetAdmin(admin.ModelAdmin):
    pass
    
admin.site.register(QuestionSet, QuestionSetAdmin)

class AnswerAdmin(admin.ModelAdmin):
    pass

admin.site.register(Answer, AnswerAdmin)