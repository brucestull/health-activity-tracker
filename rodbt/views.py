from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpResponse
from django.views.generic import ListView

from rodbt.models import Journal
from rodbt.models import Question

# Import extra context value for the site name:
from config.settings.common import THE_SITE_NAME

# Add extra context values for the page titles:
PAGE_TITLE_JOURNAL_LIST = 'My Journals'
PAGE_TITLE_QUESTION_LIST = 'My Questions'

def index(request):
    return HttpResponse("Hello, world. You're at the RO-DBT index!")


class JournalListView(LoginRequiredMixin, ListView):
    """
    List view for a user to view their own journals.
    """
    model = Journal
    context_object_name = 'journal_list'
    login_url = 'login'

    def get_queryset(self):
        return Journal.objects.filter(author=self.request.user)

    # Add extra context:
    def get_context_data(self, **kwargs):
        """
        Add extra contexts `the_site_name` and `page_title` to the view.
        """
        context = super().get_context_data(**kwargs)
        context['the_site_name'] = THE_SITE_NAME
        context['page_title'] = PAGE_TITLE_JOURNAL_LIST
        return context


class QuestionListView(LoginRequiredMixin, ListView):
    """
    List view for a user to view their own questions.
    """
    model = Question
    context_object_name = 'question_list'
    login_url = 'login'

    def get_queryset(self):
        return Question.objects.filter(author=self.request.user)

    # Add extra context:
    def get_context_data(self, **kwargs):
        """
        Add extra contexts `the_site_name` and `page_title` to the view.
        """
        context = super().get_context_data(**kwargs)
        context['the_site_name'] = THE_SITE_NAME
        context['page_title'] = PAGE_TITLE_QUESTION_LIST
        return context
