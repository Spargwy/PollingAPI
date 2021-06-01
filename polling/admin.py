from django.contrib import admin
from nested_admin.nested import NestedModelAdmin, NestedStackedInline

from .models import Poll, Question, Choice


class ChoiceAdmin(NestedStackedInline):
    model = Choice
    extra = 1


class QuestionAdmin(NestedStackedInline):
    inlines = (ChoiceAdmin,)
    model = Question
    extra = 1
    min_num = 1


@admin.register(Poll)
class PollAdmin(NestedModelAdmin):
    inlines = (QuestionAdmin,)

    def get_readonly_fields(self, request, obj=None) -> list:
        readonly_fields = list(super().get_readonly_fields(request, obj))
        if obj is not None:
            readonly_fields.append('start_date')
        return readonly_fields
