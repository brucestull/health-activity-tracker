from django.test import TestCase
from django.urls import reverse

from accounts.models import CustomUser
from accounts.forms import CustomUserCreationForm, CustomUserChangeForm


USERNAME_REGISTRATION_ACCEPTED_TRUE = 'RegisteredUser'
USERNAME_REGISTRATION_ACCEPTED_FALSE = 'UnregisteredUser'
PASSWORD_FOR_TESTING = 'a_test_password'

USERNAME_FOR_TESTING_01 = 'TestUser'
EMAIL_FOR_TESTING_01 = 'TestUser@email.app'
FIRST_NAME_FOR_TESTING_01 = 'Test'
LAST_NAME_FOR_TESTING_01 = 'User'

USERNAME_FOR_TESTING_02 = 'TestUser'
EMAIL_FOR_TESTING_02 = 'TestUser@email.app'
FIRST_NAME_FOR_TESTING_02 = 'Test'
LAST_NAME_FOR_TESTING_02 = 'User'

SIGNUP_URL = '/accounts/signup/'
SIGNUP_VIEW_NAME = 'signup'
SIGNUP_TEMPLATE = 'registration/signup.html'

LOGIN_URL = '/accounts/login/'
LOGIN_VIEW_NAME = 'login'
LOGIN_TEMPLATE = 'registration/login.html'

USER_DASHBOARD_URL = '/accounts/dashboard/'
USER_DASHBOARD_VIEW_NAME = 'dashboard'
USER_DASHBOARD_TEMPLATE = 'accounts/dashboard.html'

USER_UPDATE_URL = '/accounts/1/edit/'
USER_UPDATE_VIEW_NAME = 'edit_profile'
USER_UPDATE_TEMPLATE = 'registration/update.html'

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
                'username': USERNAME_FOR_TESTING_01,
                'email': EMAIL_FOR_TESTING_01,
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


class UserUpdateViewTest(TestCase):
    """
    Tests for the `UserUpdateView` view.
    """

    @classmethod
    def setUpTestData(cls):
        """
        Create a user for testing and log them in.
        """
        user_registration_accepted_false = CustomUser.objects.create(
            username=USERNAME_REGISTRATION_ACCEPTED_FALSE,
        )
        user_registration_accepted_false.set_password(PASSWORD_FOR_TESTING)
        user_registration_accepted_false.registration_accepted = False
        user_registration_accepted_false.save()

    def test_valid_url_exists_at_desired_location(self):
        """
        Test that the user update view URL exists at the desired location.
        """
        self.client.login(
            username=USERNAME_REGISTRATION_ACCEPTED_FALSE,
            password=PASSWORD_FOR_TESTING,
        )
        response = self.client.get(USER_UPDATE_URL)
        self.assertEqual(response.status_code, 200)

    def test_view_accessible_by_name(self):
        """
        Test that the user update view URL is accessible by name.
        """
        self.client.login(
            username=USERNAME_REGISTRATION_ACCEPTED_FALSE,
            password=PASSWORD_FOR_TESTING,
        )
        response = self.client.get(reverse(USER_UPDATE_VIEW_NAME, args=[1]))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response._request.path, USER_UPDATE_URL)

    def test_view_uses_correct_template(self):
        """
        Test that the user update view uses the correct template.
        """
        self.client.login(
            username=USERNAME_REGISTRATION_ACCEPTED_FALSE,
            password=PASSWORD_FOR_TESTING,
        )
        response = self.client.get(USER_UPDATE_URL)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, USER_UPDATE_TEMPLATE)

    def test_view_has_additional_context_objects(self):
        """
        Test that the user update view has the additional context objects
        that we want.
        """
        self.client.login(
            username=USERNAME_REGISTRATION_ACCEPTED_FALSE,
            password=PASSWORD_FOR_TESTING,
        )
        response = self.client.get(USER_UPDATE_URL)
        self.assertEqual(response.status_code, 200)
        self.assertIn('the_site_name', response.context)

    def test_view_has_form(self):
        """
        Test that the user update view has a form.
        """
        self.client.login(
            username=USERNAME_REGISTRATION_ACCEPTED_FALSE,
            password=PASSWORD_FOR_TESTING,
        )
        response = self.client.get(USER_UPDATE_URL)
        self.assertEqual(response.status_code, 200)
        self.assertIn('form', response.context)
        # Alternatives:
        self.assertTrue(response.context['form'])
        self.assertTrue('form' in response.context)

    def test_view_uses_correct_form(self):
        """
        Test that the user update view uses the correct form.
        """
        self.client.login(
            username=USERNAME_REGISTRATION_ACCEPTED_FALSE,
            password=PASSWORD_FOR_TESTING,
        )
        response = self.client.get(USER_UPDATE_URL)
        self.assertEqual(response.status_code, 200)
        self.assertIsInstance(response.context['form'], CustomUserChangeForm)

    def test_view_has_form_with_correct_fields(self):
        """
        Test that the user update view has a form with the correct fields.
        """
        self.client.login(
            username=USERNAME_REGISTRATION_ACCEPTED_FALSE,
            password=PASSWORD_FOR_TESTING,
        )
        response = self.client.get(USER_UPDATE_URL)
        self.assertEqual(response.status_code, 200)
        form = response.context['form']
        self.assertIn('username', form.fields)
        self.assertIn('email', form.fields)

    def test_view_has_form_with_correct_labels(self):
        """
        Test that the user update view has a form with the correct labels.
        """
        self.client.login(
            username=USERNAME_REGISTRATION_ACCEPTED_FALSE,
            password=PASSWORD_FOR_TESTING,
        )
        response = self.client.get(USER_UPDATE_URL)
        self.assertEqual(response.status_code, 200)
        form = response.context['form']
        self.assertEqual(form.fields['username'].label, 'Username')
        self.assertEqual(form.fields['email'].label, 'Email address')
        self.assertEqual(form.fields['first_name'].label, 'First name')
        self.assertEqual(form.fields['last_name'].label, 'Last name')

    def test_view_redirects_to_home_view_on_success(self):
        """
        Test that the user update view redirects to the home view on success.
        """
        self.client.login(
            username=USERNAME_REGISTRATION_ACCEPTED_FALSE,
            password=PASSWORD_FOR_TESTING,
        )
        response = self.client.post(
            USER_UPDATE_URL,
            {
                'username': USERNAME_FOR_TESTING_01,
                'email': EMAIL_FOR_TESTING_01,
                # 'first_name': FIRST_NAME_FOR_TESTING_01,
                # 'last_name': LAST_NAME_FOR_TESTING_01,
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

    def test_view_updates_user_on_success(self):
        """
        Test that the user update view updates the user on success.
        """
        self.client.login(
            username=USERNAME_REGISTRATION_ACCEPTED_FALSE,
            password=PASSWORD_FOR_TESTING,
        )
        response = self.client.post(
            USER_UPDATE_URL,
            {
                'username': USERNAME_FOR_TESTING_02,
                'email': EMAIL_FOR_TESTING_02,
                'first_name': FIRST_NAME_FOR_TESTING_02,
                'last_name': LAST_NAME_FOR_TESTING_02,
            },
            follow=True,
        )
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.resolver_match.view_name, HOME_VIEW_NAME)
        self.assertEqual(response._request.path, HOME_URL)
        user = CustomUser.objects.get(id=1)
        self.assertEqual(user.username, USERNAME_FOR_TESTING_02)
        self.assertEqual(user.email, EMAIL_FOR_TESTING_02)
        self.assertEqual(user.first_name, FIRST_NAME_FOR_TESTING_02)
        self.assertEqual(user.last_name, LAST_NAME_FOR_TESTING_02)


class UserDashboardViewTest(TestCase):
    """
    Test the user dashboard view.
    """
    @classmethod
    def setUpTestData(cls):
        """
        Create two `CustomUser`s:
        - One with `registration_accepted=True`.
        - One with `registration_accepted=False`.

        This specific function name `setUpTestData` is required by Django.
        """
        user_registration_accepted_true = CustomUser.objects.create(
            username=USERNAME_REGISTRATION_ACCEPTED_TRUE,
        )
        user_registration_accepted_true.set_password(PASSWORD_FOR_TESTING)
        user_registration_accepted_true.registration_accepted = True
        user_registration_accepted_true.save()

        user_registration_accepted_false = CustomUser.objects.create(
            username=USERNAME_REGISTRATION_ACCEPTED_FALSE,
        )
        user_registration_accepted_false.set_password(PASSWORD_FOR_TESTING)
        user_registration_accepted_false.registration_accepted = False
        user_registration_accepted_false.save()

    def test_view_url_redirect_to_login_if_user_not_authenticated(self):
        """
        Test that the user dashboard view URL redirects to the login view if
        the user is not authenticated.
        """
        response = self.client.get(USER_DASHBOARD_URL)
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(
            response,
            f'{LOGIN_URL}?next={USER_DASHBOARD_URL}',
            status_code=302,
            target_status_code=200,
            fetch_redirect_response=True,
        )

    def test_view_url_for_authenticated_registration_accepted_true_user(self):
        """
        Test that the user dashboard view URL is accessible for an authenticated
        user with `registration_accepted=True`.
        """
        self.client.login(
            username=USERNAME_REGISTRATION_ACCEPTED_TRUE,
            password=PASSWORD_FOR_TESTING,
        )
        response = self.client.get(USER_DASHBOARD_URL)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, USER_DASHBOARD_TEMPLATE)
        self.assertEqual(response.resolver_match.view_name, USER_DASHBOARD_VIEW_NAME)
        self.assertEqual(response._request.path, USER_DASHBOARD_URL)


    def test_view_url_for_authenticated_registration_accepted_false_user(self):
        """
        Test that the user dashboard view URL is inaccessible for an authenticated
        user with `registration_accepted=False`.
        """
        self.client.login(
            username=USERNAME_REGISTRATION_ACCEPTED_FALSE,
            password=PASSWORD_FOR_TESTING,
        )
        response = self.client.get(USER_DASHBOARD_URL)
        self.assertEqual(response.status_code, 403)


    def test_view_url_accessible_by_name(self):
        """
        Test that the user dashboard view URL is accessible by name.
        """
        self.client.login(
            username=USERNAME_REGISTRATION_ACCEPTED_TRUE,
            password=PASSWORD_FOR_TESTING,
        )
        response = self.client.get(reverse(USER_DASHBOARD_VIEW_NAME))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response._request.path, USER_DASHBOARD_URL)

    def test_view_has_additional_context_objects(self):
        """
        Test that the user dashboard view has the additional context objects
        that we want.
        """
        self.client.login(
            username=USERNAME_REGISTRATION_ACCEPTED_TRUE,
            password=PASSWORD_FOR_TESTING,
        )
        response = self.client.get(USER_DASHBOARD_URL)
        self.assertEqual(response.status_code, 200)
        self.assertIn('the_site_name', response.context)
        self.assertIn('page_title', response.context)

    def test_view_has_correct_customuser_object(self):
        """
        Test that the user dashboard view has the correct `CustomUser` object.
        """
        self.client.login(
            username=USERNAME_REGISTRATION_ACCEPTED_TRUE,
            password=PASSWORD_FOR_TESTING,
        )
        current_custom_user = CustomUser.objects.get(
            username=USERNAME_REGISTRATION_ACCEPTED_TRUE
        )
        response = self.client.get(USER_DASHBOARD_URL)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.context['customuser'], current_custom_user)
