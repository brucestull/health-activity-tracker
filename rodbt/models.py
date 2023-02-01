from django.db import models

from config.settings.common import AUTH_USER_MODEL


class Journal(models.Model):
    author = models.ForeignKey(
        AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='journals',
    )
    title = models.CharField(
        max_length=200,
        blank=True,
        null=True,
    )
    body = models.TextField()
    date = models.DateTimeField(auto_now_add=True)
    edited_date = models.DateTimeField(auto_now=True)


class Question(models.Model):
    author = models.ForeignKey(
        AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='questions',
    )
    body = models.CharField(max_length=200)
    date = models.DateTimeField(auto_now_add=True)
    edited_date = models.DateTimeField(auto_now=True)
    journal = models.ForeignKey(
        Journal,
        on_delete=models.CASCADE,
        related_name='questions',
    )