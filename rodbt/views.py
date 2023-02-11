from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpResponse
from django.views.generic import ListView
from django.views.generic.edit import CreateView
from django.views.generic.detail import DetailView

from rodbt.models import Journal
from rodbt.models import Question

# Import extra context value for the site name:
from config.settings.common import THE_SITE_NAME

# Add extra context values for the page titles:
PAGE_TITLE_JOURNAL_LIST = 'My Journals'
PAGE_TITLE_JOURNAL_CREATE = 'New Journal Entry'
PAGE_TITLE_QUESTION_LIST = 'My Questions'

def index(request):
    return HttpResponse("Hello, world. You're at the RO-DBT index!")


class JournalCreateView(LoginRequiredMixin, CreateView):
    """
    `CreateView` for a user to create a new `Journal`.
    """
    model = Journal
    fields = [
        'title',
        'body',
        # 'author',
    ]

    def form_valid(self, form):
        """
        Set the `author` field to the current user.
        """
        form.instance.author = self.request.user
        return super().form_valid(form)

    # Add extra context:
    def get_context_data(self, **kwargs):
        """
        Add extra contexts `the_site_name` and `page_title` to the view.
        """
        context = super().get_context_data(**kwargs)
        context['the_site_name'] = THE_SITE_NAME
        context['page_title'] = PAGE_TITLE_JOURNAL_CREATE
        return context

class JournalDetailView(LoginRequiredMixin, DetailView):
    """
    `DetailView` for a user to view a `Journal`.
    """
    model = Journal


class JournalListView(LoginRequiredMixin, ListView):
    """
    List view for a user to view their own journals.

    Default context object names are `journal_list` and `object_list`.

    Default template name is `rodbt/journal_list.html`.
    """
    model = Journal

    # login_url = 'login'

    # template_name = 'rodbt/journal_list.html'
    # TODO Remove this method: Use it temporarily to view the template
    # names in debug mode and `"justMyCode": true`.
    def get_template_names(self):
        template_names = super().get_template_names()
        return template_names

    def get_queryset(self):
        """
        Get the list of `Journal`s for the current user.
        """
        return Journal.objects.filter(author=self.request.user).order_by('-date')

    # context_object_name = 'journal_list'
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

    Default context object names are `question_list` and `object_list`.

    Default template name is `rodbt/question_list.html`.
    """
    model = Question

    # login_url = 'login'

    # template_name = 'rodbt/question_list.html'
    # TODO Remove this method: Use it temporarily to view the template
    # names in debug mode and `"justMyCode": true`.
    def get_template_names(self):
        template_names = super().get_template_names()
        return template_names

    def get_queryset(self):
        """
        Get the list of `Question`s for the current user.
        """
        return Question.objects.filter(author=self.request.user)

    # context_object_name = 'question_list'
    # Add extra context:
    def get_context_data(self, **kwargs):
        """
        Add extra contexts `the_site_name` and `page_title` to the view.
        """
        context = super().get_context_data(**kwargs)
        context['the_site_name'] = THE_SITE_NAME
        context['page_title'] = PAGE_TITLE_QUESTION_LIST
        return context
