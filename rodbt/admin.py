from django.contrib import admin

from rodbt.models import Journal, Question


@admin.register(Journal)
class JournalAdmin(admin.ModelAdmin):
    list_display = [
        'author',
        '__str__',  # title
        # 'title',
        'date',
    ]
    fields = [
        'author',
        'title',
        'body',
    ]
    list_filter = [
        'date',
        'edited_date',
    ]

@admin.register(Question)
class QuestionAdmin(admin.ModelAdmin):
    list_display = [
        'author',
        '__str__',  # body
        'date',
    ]
    fields = [
        'author',
        'body',
        'journal',
    ]
    list_filter = [
        'date',
        'edited_date',
    ]

