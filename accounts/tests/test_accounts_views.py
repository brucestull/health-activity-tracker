from django.test import TestCase
from django.urls import reverse

from accounts.models import CustomUser


USERNAME_REGISTRATION_ACCEPTED_FALSE = 'UnregisteredUser'
PASSWORD_FOR_TESTING = 'a_test_password'

LOGIN_URL = '/accounts/login/'
LOGIN_VIEW_NAME = 'login'
LOGIN_TEMPLATE = 'registration/login.html'

HOME_URL = '/'
HOME_VIEW_NAME = 'home'
HOME_TEMPLATE = 'home.html'


class CustomLoginViewTest(TestCase):
    """
    Tests for the `CustomLoginView` view.
    """

    def test_valid_url_exists_at_desired_location(self):
        """
        Test that the login view URL exists at the desired location.
        """
        response = self.client.get(LOGIN_URL)
        self.assertEqual(response.status_code, 200)

    def test_view_accessible_by_name(self):
        """
        Test that the login view URL is accessible by name.
        """
        response = self.client.get(reverse(LOGIN_VIEW_NAME))
        self.assertEqual(response.status_code, 200)
        # TODO: Redundant?
        self.assertEqual(response.resolver_match.view_name, LOGIN_VIEW_NAME)
        self.assertEqual(response._request.path, LOGIN_URL)

    def test_view_uses_correct_template(self):
        """
        Test that the login view uses the correct template.
        """
        response = self.client.get(LOGIN_URL)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, LOGIN_TEMPLATE)

    def test_view_has_additional_context_objects(self):
        """
        Test that the login view has the additional context objects
        that we want.
        """
        response = self.client.get(LOGIN_URL)
        self.assertEqual(response.status_code, 200)
        self.assertIn('the_site_name', response.context)

    def test_view_has_form(self):
        """
        Test that the login view has a form.
        """
        response = self.client.get(LOGIN_URL)
        self.assertEqual(response.status_code, 200)
        self.assertIn('form', response.context)
        # Alternatives:
        self.assertTrue(response.context['form'])
        self.assertTrue('form' in response.context)

    def test_view_has_form_with_correct_fields(self):
        """
        Test that the login view has a form with the correct fields.
        """
        response = self.client.get(LOGIN_URL)
        self.assertEqual(response.status_code, 200)
        form = response.context['form']
        self.assertIn('username', form.fields)
        self.assertIn('password', form.fields)

    def test_view_has_form_with_correct_labels(self):
        """
        Test that the login view has a form with the correct labels.
        """
        response = self.client.get(LOGIN_URL)
        self.assertEqual(response.status_code, 200)
        form = response.context['form']
        self.assertEqual(form.fields['username'].label, 'Username')
        self.assertEqual(form.fields['password'].label, 'Password')

    def test_view_redirects_to_home_view_on_success(self):
        """
        Test that the login view redirects to the home view on success.
        """
        # Create a user with `registration_accepted=False`:
        CustomUser.objects.create_user(
            username=USERNAME_REGISTRATION_ACCEPTED_FALSE,
            password=PASSWORD_FOR_TESTING,
            registration_accepted=False,
        )
        # Log in with that user:
        response = self.client.post(
            LOGIN_URL,
            {
                'username': USERNAME_REGISTRATION_ACCEPTED_FALSE,
                'password': PASSWORD_FOR_TESTING,
            },
            follow=True,
        )
        self.assertEqual(response.status_code, 200)
        self.assertRedirects(
            response,
            HOME_URL,
            status_code=302,
            target_status_code=200,
            fetch_redirect_response=True,
        )
        self.assertTemplateUsed(response, HOME_TEMPLATE)
        self.assertEqual(response.resolver_match.view_name, HOME_VIEW_NAME)
        self.assertEqual(response._request.path, HOME_URL)
