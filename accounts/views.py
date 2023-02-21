from django.urls import reverse_lazy
from django.views.generic.edit import CreateView, UpdateView
from django.views.generic.detail import DetailView
from django.contrib.auth.views import LoginView
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin

from accounts.forms import CustomUserCreationForm, CustomUserChangeForm
from accounts.models import CustomUser
from config.settings.common import THE_SITE_NAME

DASHBOARD_PAGE_TITLE = 'Dashboard'


class CustomLoginView(LoginView):
    """
    Override the default login view. This will allow us to add the site
    name to the context and then display it on the page.
    """
    # TODO: Is this functionality a security risk?
    # This is probably not neccessary because we can control whether or
    # not a link is shown in the template for the login view.
    redirect_authenticated_user = True

    def get_context_data(self, **kwargs):
        """
        Get the parent `context` and add the site name to the it.
        """
        context = super().get_context_data(**kwargs)
        context['the_site_name'] = THE_SITE_NAME
        return context


class SignUpView(CreateView):
    """
    View for user to create a new account.
    """
    form_class = CustomUserCreationForm
    success_url = reverse_lazy('login')
    template_name = 'registration/signup.html'

    def get_context_data(self, **kwargs):
        """
        Add the site name to the context.
        """
        context = super().get_context_data(**kwargs)
        context['the_site_name'] = THE_SITE_NAME
        return context


class UserUpdateView(LoginRequiredMixin, UpdateView):
    """
    View for user to update an existing account.
    """
    model = CustomUser
    form_class = CustomUserChangeForm
    success_url = reverse_lazy('home')
    template_name ='registration/update.html'

    def get_context_data(self, **kwargs):
        """
        Add the site name to the context.
        """
        context = super().get_context_data(**kwargs)
        context['the_site_name'] = THE_SITE_NAME
        return context


class UserDashboardView(LoginRequiredMixin, UserPassesTestMixin, DetailView):
    """
    View for user to see their `Journal`s and `Question`s and other
    related models.
    """
    # No need to specify a `model` because we are overriding `get_object()`
    template_name = 'accounts/dashboard.html'

    def test_func(self):
        """
        Test if user has `registration_accepted=True`.
        """
        return self.request.user.registration_accepted

    def get_object(self):
        """
        Get the current user's `CustomUser` object.
        """
        return self.request.user

    def get_context_data(self, **kwargs):
        """
        Add `the_site_name` and `page_title` to the context.
        """
        context = super().get_context_data(**kwargs)
        # Default context objects:
        #   `object`: the `CustomUser` object
        #   `customuser`: the `CustomUser` object
        #   `view`: the `UserDashboardView` object
        context['the_site_name'] = THE_SITE_NAME
        context['page_title'] = DASHBOARD_PAGE_TITLE
        return context
