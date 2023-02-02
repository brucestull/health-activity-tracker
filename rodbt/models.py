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
    date = models.DateTimeField(
        'Created Date',
        auto_now_add=True,
    )
    edited_date = models.DateTimeField(
        'Edited Date',
        auto_now=True,
    )

    def __str__(self):
        return self.title[:30]


class Question(models.Model):
    author = models.ForeignKey(
        AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='questions',
    )
    body = models.CharField(
        max_length=200
    )
    date = models.DateTimeField(
        'Created Date',
        auto_now_add=True,
    )
    edited_date = models.DateTimeField(
        'Edited Date',
        auto_now=True,
    )
    journal = models.ManyToManyField(
        Journal,
        symmetrical=False,
        related_name='questions',
        blank=True,
    )

    def __str__(self):
        return self.body[:40]