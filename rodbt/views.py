from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpResponse
from django.views.generic import ListView

from rodbt.models import Journal
from rodbt.models import Question

def index(request):
    return HttpResponse("Hello, world. You're at the RO-DBT index!")


class JournalListView(LoginRequiredMixin, ListView):
    model = Journal
    context_object_name = 'journal_list'
    # template_name = 'rodbt/journal_list.html'
    login_url = 'login'

    def get_queryset(self):
        return Journal.objects.filter(author=self.request.user)


class QuestionListView(LoginRequiredMixin, ListView):
    model = Question
    context_object_name = 'question_list'
    # template_name = 'rodbt/question_list.html'
    login_url = 'login'

    def get_queryset(self):
        return Question.objects.filter(author=self.request.user)
