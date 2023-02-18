from django.db import models
from django.urls import reverse

from config.settings.common import AUTH_USER_MODEL


class Journal(models.Model):
    author = models.ForeignKey(
        AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='journals',
    )
    title = models.CharField(
        verbose_name='Title',
        max_length=200,
        blank=True,
        null=True,
    )
    body = models.TextField(
        verbose_name='Journal Body Text',
    )
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

    def get_absolute_url(self):
        return reverse('rodbt:journal-detail', args=[str(self.id)])


class Question(models.Model):
    author = models.ForeignKey(
        AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='questions',
    )
    body = models.CharField(
        verbose_name='Question Body Text',
        max_length=200,
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
        # null=True, # Has no effect on ManyToManyField. So not needed.
    )

    def __str__(self):
        return self.body[:40]

    def get_absolute_url(self):
        return reverse('rodbt:question-detail', args=[str(self.id)])