from django.contrib import admin

from questions.models import Question, QuestionSet, Answer, QuestionSetQuestion


class QuestionAdmin(admin.ModelAdmin):
    list_display = ('title', 'frontend_title', 'theme',)

admin.site.register(Question, QuestionAdmin)
    
class QuestionSetQuestionAdmin(admin.ModelAdmin):
    list_display = ('question', 'questionset', 'position', )
    list_filter = ('questionset', )
admin.site.register(QuestionSetQuestion, QuestionSetQuestionAdmin)

class QuestionSetAdmin(admin.ModelAdmin):
    pass
    
admin.site.register(QuestionSet, QuestionSetAdmin)

class AnswerAdmin(admin.ModelAdmin):
    pass

admin.site.register(Answer, AnswerAdmin)