from django.test import TestCase
from django.urls import reverse

from accounts.models import CustomUser
from rodbt.models import Question


USERNAME_REGISTRATION_ACCEPTED_TRUE = 'RegisteredUser'
USERNAME_REGISTRATION_ACCEPTED_FALSE = 'UnregisteredUser'
A_TEST_PASSWORD = 'a_test_password'

NUMBER_OF_QUESTIONS = 11

QUESTION_CREATE_URL = '/rodbt/question/create/'
QUESTION_CREATE_VIEW_NAME = 'rodbt:question-create'
QUESTION_CREATE_TEMPLATE = 'rodbt/question_form.html'

QUESTIONS_URL = '/rodbt/questions/'
QUESTIONS_VIEW_NAME = 'rodbt:questions'
QUESTIONS_TEMPLATE = 'rodbt/question_list.html'

QUESTION_DETAIL_URL = '/rodbt/questions/1/'
QUESTION_DETAIL_VIEW_NAME = 'rodbt:question-detail'
QUESTION_DETAIL_TEMPLATE = 'rodbt/question_detail.html'

A_TEST_QUESTION_BODY = (
"""
This is a Question Body, here. It's a long string of text, and it might
not be tested for length, but it's here since we have to provide a 'body'
when creating a `Question`.
"""
)

PAGE_TITLE_QUESTION_DETAIL = 'Question Detail'


class QuestionCreateViewTest(TestCase):
    """
    Test the `QuestionCreateView`.
    """
    @classmethod
    def setUpTestData(cls):
        """
        Create a `CustomUser` with `registration_accepted=True`.

        This specific function name `setUpTestData` is required by Django.
        """
        registered_user = CustomUser.objects.create(
            username=USERNAME_REGISTRATION_ACCEPTED_TRUE,
        )
        registered_user.set_password(A_TEST_PASSWORD)
        registered_user.registration_accepted = True
        registered_user.save()

    def test_view_url_redirects_to_login_if_not_logged_in(self):
        """
        View should redirect non-authenticated user to login view .
        """
        response = self.client.get(QUESTION_CREATE_URL)
        self.assertRedirects(
            response,
            f'/accounts/login/?next={QUESTION_CREATE_URL}',
        )

    def test_view_url_for_logged_in_registration_accepted_true_user(self):
        """
        View should return `status_code` of 200 for authenticated user
        who has `registration_accepted=True`.
        """
        self.client.login(
            username=USERNAME_REGISTRATION_ACCEPTED_TRUE,
            password=A_TEST_PASSWORD,
        )
        response = self.client.get(QUESTION_CREATE_URL)
        self.assertEqual(response.status_code, 200)

    def test_view_url_accessible_by_name(self):
        """
        View should be accessible through the `APP_NAME:VIEW_NAME`.

        This tests functionality of `app_name` and `name` in `urlpatterns`
        list of `urls.py`.
        """
        self.client.login(
            username=USERNAME_REGISTRATION_ACCEPTED_TRUE,
            password=A_TEST_PASSWORD,
        )
        response = self.client.get(reverse(QUESTION_CREATE_VIEW_NAME))
        self.assertEqual(response.status_code, 200)

    def test_view_uses_correct_template(self):
        """
        View should use proper `QUESTION_CREATE_TEMPLATE`.

        There is no need to test this case when `registration_accepted=False`,
        I think. Will write the test and see what it looks like.
        """
        self.client.login(
            username=USERNAME_REGISTRATION_ACCEPTED_TRUE,
            password=A_TEST_PASSWORD,
        )
        response = self.client.get(QUESTION_CREATE_URL)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, QUESTION_CREATE_TEMPLATE)

    def test_view_has_additional_context_objects(self):
        """
        View should have additional context objects:
        - `the_site_name`
        - `page_title`
        """
        self.client.login(
            username=USERNAME_REGISTRATION_ACCEPTED_TRUE,
            password=A_TEST_PASSWORD,
        )
        response = self.client.get(QUESTION_CREATE_URL)
        self.assertEqual(response.status_code, 200)
        self.assertTrue('the_site_name' in response.context)
        self.assertTrue('page_title' in response.context)

    def test_view_has_form(self):
        """
        View should have a `form` in the context.
        """
        self.client.login(
            username=USERNAME_REGISTRATION_ACCEPTED_TRUE,
            password=A_TEST_PASSWORD,
        )
        response = self.client.get(QUESTION_CREATE_URL)
        self.assertEqual(response.status_code, 200)
        self.assertTrue('form' in response.context)

    def test_view_form_has_correct_fields(self):
        """
        HTTP request to the view URL should have a form with the correct
        fields and they should be in proper order:
        - `body`
        - `journal`
        """
        self.client.login(
            username=USERNAME_REGISTRATION_ACCEPTED_TRUE,
            password=A_TEST_PASSWORD,
        )
        response = self.client.get(QUESTION_CREATE_URL)
        self.assertEqual(response.status_code, 200)
        # These two tests are checking if the fields are in the form.
        # Are these two tests necessary?
        self.assertTrue('body' in response.context['form'].fields)
        self.assertTrue('journal' in response.context['form'].fields)
        # This test is checking if the fields are present and are in the correct order,
        # specified in `rodbt/forms.py`.
        self.assertEqual(
            list(response.context['form'].fields),
            [
                'body',
                'journal',
            ]
        )

    def test_view_form_has_correct_labels(self):
        """
        Form inputs should have the correct labels:
        - `body` -> 'Question Body Text'
        - `journal` -> 'Journal'
        """
        self.client.login(
            username=USERNAME_REGISTRATION_ACCEPTED_TRUE,
            password=A_TEST_PASSWORD,
        )
        response = self.client.get(QUESTION_CREATE_URL)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(
            response.context['form'].fields['body'].label,
            'Question Body Text',
        )
        self.assertEqual(
            response.context['form'].fields['journal'].label,
            'Journal',
        )
