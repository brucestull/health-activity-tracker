from django.test import TestCase
from django.urls import reverse

from accounts.models import CustomUser
from accounts.forms import CustomUserCreationForm


USERNAME_REGISTRATION_ACCEPTED_FALSE = 'UnregisteredUser'
PASSWORD_FOR_TESTING = 'a_test_password'

USERNAME_FOR_TESTING = 'a_test_username'
EMAIL_FOR_TESTING = 'a_test_username@email.app'

SIGNUP_URL = '/accounts/signup/'
SIGNUP_VIEW_NAME = 'signup'
SIGNUP_TEMPLATE = 'registration/signup.html'

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


class SignUpViewTest(TestCase):
    """
    Tests for the `SignUpView` view.
    """

    def test_valid_url_exists_at_desired_location(self):
        """
        Test that the sign up view URL exists at the desired location.
        """
        response = self.client.get('/accounts/signup/')
        self.assertEqual(response.status_code, 200)

    def test_view_accessible_by_name(self):
        """
        Test that the sign up view URL is accessible by name.
        """
        response = self.client.get(reverse('signup'))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response._request.path, SIGNUP_URL)

    def test_view_uses_correct_template(self):
        """
        Test that the sign up view uses the correct template.
        """
        response = self.client.get(SIGNUP_URL)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, SIGNUP_TEMPLATE)

    def test_view_has_additional_context_objects(self):
        """
        Test that the sign up view has the additional context objects
        that we want.
        """
        response = self.client.get(SIGNUP_URL)
        self.assertEqual(response.status_code, 200)
        self.assertIn('the_site_name', response.context)

    def test_view_has_form(self):
        """
        Test that the sign up view has a form.
        """
        response = self.client.get(SIGNUP_URL)
        self.assertEqual(response.status_code, 200)
        self.assertIn('form', response.context)
        # Alternatives:
        self.assertTrue(response.context['form'])
        self.assertTrue('form' in response.context)

    def test_view_uses_correct_form(self):
        """
        Test that the sign up view uses the correct form.
        """
        response = self.client.get(SIGNUP_URL)
        self.assertEqual(response.status_code, 200)
        self.assertIsInstance(response.context['form'], CustomUserCreationForm)

    def test_view_has_form_with_correct_fields(self):
        """
        Test that the sign up view has a form with the correct fields.

        This test is redundant, because the form is tested by Django.
        We didn't write the code for the form.
        """
        response = self.client.get(SIGNUP_URL)
        self.assertEqual(response.status_code, 200)
        form = response.context['form']
        self.assertIn('username', form.fields)
        self.assertIn('email', form.fields)
        self.assertIn('password1', form.fields)
        self.assertIn('password2', form.fields)

    def test_view_has_form_with_correct_labels(self):
        """
        Test that the sign up view has a form with the correct labels.

        This test is redundant, because the form is tested by Django.
        We didn't write the code for the form.
        """
        response = self.client.get(SIGNUP_URL)
        self.assertEqual(response.status_code, 200)
        form = response.context['form']
        self.assertEqual(form.fields['username'].label, 'Username')
        self.assertEqual(form.fields['email'].label, 'Email address')
        self.assertEqual(form.fields['password1'].label, 'Password')
        self.assertEqual(form.fields['password2'].label, 'Password confirmation')

    def test_view_redirects_to_login_view_on_success(self):
        """
        Test that the sign up view redirects to the login view on success.
        """
        response = self.client.post(
            SIGNUP_URL,
            {
                'username': USERNAME_FOR_TESTING,
                'email': EMAIL_FOR_TESTING,
                'password1': PASSWORD_FOR_TESTING,
                'password2': PASSWORD_FOR_TESTING,
            },
            follow=True,
        )
        self.assertEqual(response.status_code, 200)
        self.assertRedirects(
            response,
            LOGIN_URL,
            status_code=302,
            target_status_code=200,
            fetch_redirect_response=True,
        )
        self.assertTemplateUsed(response, LOGIN_TEMPLATE)
        self.assertEqual(response.resolver_match.view_name, LOGIN_VIEW_NAME)
        self.assertEqual(response._request.path, LOGIN_URL)
