from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.http import HttpResponse
from django.views.generic import ListView
from django.views.generic.edit import CreateView
from django.views.generic.detail import DetailView

from rodbt.models import Journal
from rodbt.models import Question

from rodbt.forms import QuestionForm

# Import extra context value for the site name:
from config.settings.common import THE_SITE_NAME

# Add extra context values for the page titles:
PAGE_TITLE_JOURNAL_LIST = 'My Journals'
PAGE_TITLE_JOURNAL_DETAIL = 'Journal Detail'
PAGE_TITLE_JOURNAL_CREATE = 'New Journal Entry'

PAGE_TITLE_QUESTION_LIST = 'My Questions'
PAGE_TITLE_QUESTION_DETAIL = 'Question Detail'
PAGE_TITLE_QUESTION_CREATE = 'New Question'


def index(request):
    return HttpResponse("Hello, world. You're at the RO-DBT index!")

class JournalCreateView(LoginRequiredMixin, UserPassesTestMixin, CreateView):
    """
    `CreateView` for a user to create a new `Journal`.
    """
    model = Journal
    fields = [
        'title',
        'body',
        # 'author', # `author` is set in `form_valid()
    ]

    def test_func(self):
        """
        Test if user has `registration_accepted=True`.
        """
        return self.request.user.registration_accepted

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

class JournalDetailView(LoginRequiredMixin, UserPassesTestMixin, DetailView):
    """
    `DetailView` for a user to view a `Journal`.
    """
    model = Journal

    def test_func(self):
        """
        Test if user has `registration_accepted=True`.
        """
        return self.request.user.registration_accepted

    # Add extra context:
    def get_context_data(self, **kwargs):
        """
        Add extra context `page_title` to the view.
        """
        context = super().get_context_data(**kwargs)
        context['page_title'] = PAGE_TITLE_JOURNAL_DETAIL
        return context

class JournalListView(LoginRequiredMixin, UserPassesTestMixin, ListView):
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

    def test_func(self):
        """
        Test if user has `registration_accepted=True`.
        """
        return self.request.user.registration_accepted

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

class QuestionCreateView(LoginRequiredMixin, UserPassesTestMixin, CreateView):
    """
    `CreateView` for a user to create a new `Question`.
    """
    # model = Question
    form_class = QuestionForm
    template_name = 'rodbt/question_form.html'
    # fields = [
    #     'body',
    #     'journal',
    #     # 'author', # `author` is set in `form_valid()
    # ]

    def test_func(self):
        """
        Test if user has `registration_accepted=True`.
        """
        return self.request.user.registration_accepted

    def get_form_kwargs(self):
        """
        Pass the `user`, via kwarg `user`, to `QuestionForm`.
        """
        kwargs = super().get_form_kwargs()
        kwargs['user'] = self.request.user
        return kwargs

    def form_valid(self, form):
        """
        Set the `author` field to the current user and then, if the form
        is valid, save the associated model.
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
        context['page_title'] = PAGE_TITLE_QUESTION_CREATE
        return context

class QuestionListView(LoginRequiredMixin, UserPassesTestMixin, ListView):
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

    def test_func(self):
        """
        Test if user has `registration_accepted=True`.
        """
        return self.request.user.registration_accepted

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

class QuestionDetailView(LoginRequiredMixin, UserPassesTestMixin, DetailView):
    """
    `DetailView` for a user to view a `Question`.
    """
    model = Question

    def test_func(self):
        """
        Test if user has `registration_accepted=True`.

        Purpose:
        * Ensure that the user is not able to view `Question`s for other users.
        * Ensure that the user is registered.
        """
        user_owns_question = self.request.user == self.get_object().author
        user_registration_accepted = self.request.user.registration_accepted

        return user_owns_question and user_registration_accepted


    # Add extra context:
    def get_context_data(self, **kwargs):
        """
        Add extra context `page_title` to the view.
        """
        context = super().get_context_data(**kwargs)
        context['page_title'] = PAGE_TITLE_QUESTION_DETAIL
        return context
