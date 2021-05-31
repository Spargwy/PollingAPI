from django.contrib import admin
from .models import Poll, Question, Answer


class AnswersAdmin(admin.StackedInline):
    model = Answer()
    extra = 1


class QuestionAdmin(admin.StackedInline):
    inlines = (AnswersAdmin,)
    model = Question
    extra = 1
    min_num = 1


@admin.register(Poll)
class PollAdmin(admin.ModelAdmin):
    inlines = (QuestionAdmin,)

    def get_readonly_fields(self, request, obj=None) -> list:
        readonly_fields = list(super().get_readonly_fields(request, obj))
        if obj is not None:
            readonly_fields.append('start_date')
        return readonly_fields
