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
        """
        registered_user = CustomUser.objects.create(
            username=USERNAME_REGISTRATION_ACCEPTED_TRUE,
        )
        registered_user.set_password(A_TEST_PASSWORD)
        registered_user.registration_accepted = True
        registered_user.save()

    def test_view_url_redirects_to_login_if_not_logged_in(self):
        """
        Test that the view redirects to the login page if the user is not
        logged in.
        """
        response = self.client.get(QUESTION_CREATE_URL)
        self.assertRedirects(
            response,
            f'/accounts/login/?next={QUESTION_CREATE_URL}',
        )

    def test_view_url_for_logged_in_user(self):
        """
        Test that the view URL exists for a logged-in user.
        """
        self.client.login(
            username=USERNAME_REGISTRATION_ACCEPTED_TRUE,
            password=A_TEST_PASSWORD,
        )
        response = self.client.get(QUESTION_CREATE_URL)
        self.assertEqual(response.status_code, 200)

    def test_view_url_accessible_by_name(self):
        """
        Test that the view URL is accessible by name.
        """
        self.client.login(
            username=USERNAME_REGISTRATION_ACCEPTED_TRUE,
            password=A_TEST_PASSWORD,
        )
        response = self.client.get(reverse(QUESTION_CREATE_VIEW_NAME))
        self.assertEqual(response.status_code, 200)

    def test_view_uses_correct_template(self):
        """
        Test that the view uses the correct template.
        """
        self.client.login(
            username=USERNAME_REGISTRATION_ACCEPTED_TRUE,
            password=A_TEST_PASSWORD,
        )
        response = self.client.get(QUESTION_CREATE_URL)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, QUESTION_CREATE_TEMPLATE)

    def test_view_has_extra_context_objects(self):
        """
        Test that the view has the extra context objects `the_site_name`
        and `page_title`.
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
        Test that the view has a form.
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
        fields:
        - `body`
        - `journal`

        Test that the form has the correct fields and they are in proper order.
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
        # This test is checking if the fields are in the correct order,
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
        Test that the form has the correct labels.
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
