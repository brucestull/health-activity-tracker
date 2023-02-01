from django.contrib import admin

from rodbt.models import Journal, Question


class QuestionInline(admin.TabularInline):
    """
    Defines format of `Question` inline insertion.
    """
    model = Question

@admin.register(Journal)
class JournalAdmin(admin.ModelAdmin):
    list_display = (
        'author',
        'title',
        'date',
    )
    fields = [
        'author',
        'title',
        'body',
    ]
    inlines = [
        QuestionInline,
    ]

admin.site.register(Question)
