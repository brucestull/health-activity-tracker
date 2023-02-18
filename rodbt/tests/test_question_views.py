from django.test import TestCase
from django.urls import reverse

from accounts.models import CustomUser
from rodbt.models import Question, Journal


USERNAME_REGISTRATION_ACCEPTED_TRUE = 'RegisteredUser'
USERNAME_REGISTRATION_ACCEPTED_FALSE = 'UnregisteredUser'
PASSWORD_FOR_TESTING = 'a_test_password'

LOGIN_URL = '/accounts/login/'

NUMBER_OF_QUESTIONS = 11

QUESTION_CREATE_URL = '/rodbt/questions/create/'
QUESTION_CREATE_VIEW_NAME = 'rodbt:question-create'
QUESTION_CREATE_TEMPLATE = 'rodbt/question_form.html'

QUESTIONS_URL = '/rodbt/questions/'
QUESTIONS_VIEW_NAME = 'rodbt:questions'
QUESTIONS_TEMPLATE = 'rodbt/question_list.html'

QUESTION_DETAIL_URL = '/rodbt/questions/1/'
QUESTION_DETAIL_VIEW_NAME = 'rodbt:question-detail'
QUESTION_DETAIL_TEMPLATE = 'rodbt/question_detail.html'

QUESTION_BODY_TOO_LONG = (
"""
This is a Question Body, here. It's a long string of text, and it might
not be tested for length, but it's here since we have to provide a 'body'
when creating a `Question`.
"""
)

QUESTION_BODY = "This is a Question Body, here. It's short enough."
QUESTION_BODY_01 = "This is a Question Body, here. It's short enough. 01"
QUESTION_BODY_02 = "This is a Question Body, here. It's short enough. 02"

JOURNAL_TITLE = 'A Journal Title'
JOURNAL_BODY = (
"""
This is a Journal Body, here. It's a long string of text, and it might
not be tested for length, but it's here since we have to provide a 'body'
when creating a `Journal`.
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

    def test_view_url_redirects_to_login_if_user_not_authenticated(self):
        """
        View should redirect non-authenticated user to login view.
        """
        response = self.client.get(QUESTION_CREATE_URL)
        self.assertRedirects(
            response,
            f'{LOGIN_URL}?next={QUESTION_CREATE_URL}',
        )

    def test_view_url_for_authenticated_registration_accepted_false_user(self):
        """
        View should return `status_code` of 403 for authenticated user
        who has `registration_accepted=False`.
        """
        self.client.login(
            username=USERNAME_REGISTRATION_ACCEPTED_FALSE,
            password=PASSWORD_FOR_TESTING,
        )
        response = self.client.get(QUESTION_CREATE_URL)
        self.assertEqual(response.status_code, 403)

    def test_view_url_for_authenticated_registration_accepted_true_user(self):
        """
        View should return `status_code` of 200 for authenticated user
        who has `registration_accepted=True`.
        """
        self.client.login(
            username=USERNAME_REGISTRATION_ACCEPTED_TRUE,
            password=PASSWORD_FOR_TESTING,
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
            password=PASSWORD_FOR_TESTING,
        )
        response = self.client.get(reverse(QUESTION_CREATE_VIEW_NAME))

        # There is probably no need to test that `QUESTION_CREATE_VIEW_NAME`
        # routes to `QUESTION_CREATE_URL` since Django provides this
        # functionality in `reverse()`. Django has their own tests to ensure
        # `reverse()` works as expected.
        # self.assertEqual(reverse(QUESTION_CREATE_VIEW_NAME), QUESTION_CREATE_URL)

        self.assertEqual(response.status_code, 200)

    def test_view_uses_correct_template(self):
        """
        View should use proper `QUESTION_CREATE_TEMPLATE`.

        There is no need to test this case when `registration_accepted=False`,
        I think. That is tested in `test_view_url_for_authenticated_registration_accepted_false_user`.
        """
        self.client.login(
            username=USERNAME_REGISTRATION_ACCEPTED_TRUE,
            password=PASSWORD_FOR_TESTING,
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
            password=PASSWORD_FOR_TESTING,
        )
        response = self.client.get(QUESTION_CREATE_URL)
        # Probably not necessary to test `status_code` here since the
        # context wouldn't exist if the view didn't return `status_code`
        # of 200.
        self.assertEqual(response.status_code, 200)
        self.assertTrue('the_site_name' in response.context)
        self.assertTrue('page_title' in response.context)

    def test_view_has_form(self):
        """
        View should have a `form` in the context.
        """
        self.client.login(
            username=USERNAME_REGISTRATION_ACCEPTED_TRUE,
            password=PASSWORD_FOR_TESTING,
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
            password=PASSWORD_FOR_TESTING,
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
            password=PASSWORD_FOR_TESTING,
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

    def test_view_redirects_to_new_question_on_successful_post(self):
        """
        View should redirect to the newly created question on successful POST.
        """
        # Log in a user:6
        self.client.login(
            username=USERNAME_REGISTRATION_ACCEPTED_TRUE,
            password=PASSWORD_FOR_TESTING,
        )
        # Create a `Journal` object in the database since we need it to
        # create a `Question`:
        test_journal = Journal.objects.create(
            title=JOURNAL_TITLE,
            body=JOURNAL_BODY,
            author=CustomUser.objects.get(
                username=USERNAME_REGISTRATION_ACCEPTED_TRUE
            ),
        )
        # Make a POST request to the view to create a `Question`:
        response = self.client.post(
            QUESTION_CREATE_URL,
            {
                'body': QUESTION_BODY,
                'journal': test_journal.id,
            },
        )
        # Test that view redirects to the newly created `Question`
        # detail view:
        new_question = Question.objects.get(body=QUESTION_BODY)
        self.assertRedirects(
            response,
            reverse(
                QUESTION_DETAIL_VIEW_NAME,
                kwargs={'pk': new_question.id},
            ),
        )


class QuestionDetailViewTest(TestCase):
    """
    Tests the `QuestionDetailView`.
    """
    @classmethod
    def setUpTestData(cls):
        """
        Create two `CustomUser`s and a `Question` for testing.

        This specific function name `setUpTestData` is required by Django.
        """
        # Create users:
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

        # Create a `Journal` object in the database since we need it to
        # create a `Question`:
        test_journal = Journal.objects.create(
            title=JOURNAL_TITLE,
            body=JOURNAL_BODY,
            author=CustomUser.objects.get(
                username=USERNAME_REGISTRATION_ACCEPTED_TRUE
            ),
        )

        # Create a `Question` object in the database for
        # `USERNAME_REGISTRATION_ACCEPTED_TRUE`:
        test_question = Question.objects.create(
            body=QUESTION_BODY,
            author=CustomUser.objects.get(
                username=USERNAME_REGISTRATION_ACCEPTED_TRUE
            ),
        )
        test_journal.questions.add(test_question)

    def test_view_url_redirects_to_login_if_user_not_authenticated(self):
        """
        View should redirect non-authenticated user to login view.
        """
        response = self.client.get(QUESTION_DETAIL_URL)
        self.assertRedirects(
            response,
            f'{LOGIN_URL}?next={QUESTION_DETAIL_URL}'
        )

    def test_view_url_for_authenticated_registration_accepted_false_user(self):
        """
        View should return `status_code` of 403 for authenticated user
        who has `registration_accepted=False`.
        """
        self.client.login(
            username=USERNAME_REGISTRATION_ACCEPTED_FALSE,
            password=PASSWORD_FOR_TESTING,
        )
        response = self.client.get(QUESTION_DETAIL_URL)
        self.assertEqual(response.status_code, 403)

    def test_view_url_for_authenticated_registration_accepted_true_user(self):
        """
        View should return `status_code` of 200 for authenticated user
        who has `registration_accepted=True`.
        """
        self.client.login(
            username=USERNAME_REGISTRATION_ACCEPTED_TRUE,
            password=PASSWORD_FOR_TESTING,
        )
        response = self.client.get(QUESTION_DETAIL_URL)
        self.assertEqual(response.status_code, 200)

    def test_view_url_accessible_by_name(self):
        """
        View should be accessible by name.
        """
        self.client.login(
            username=USERNAME_REGISTRATION_ACCEPTED_TRUE,
            password=PASSWORD_FOR_TESTING,
        )
        the_existing_question = Question.objects.get(body=QUESTION_BODY)
        response = self.client.get(
            reverse(
                QUESTION_DETAIL_VIEW_NAME,
                args=[the_existing_question.id],
                # kwargs={'pk': the_existing_question.id},
                # Alternatively, can use the following:
            )
        )
        self.assertEqual(response.status_code, 200)

    def test_view_uses_correct_template(self):
        """
        View should use proper `JOURNAL_DETAIL_TEMPLATE`.
        """
        self.client.login(
            username=USERNAME_REGISTRATION_ACCEPTED_TRUE,
            password=PASSWORD_FOR_TESTING,
        )
        response = self.client.get(QUESTION_DETAIL_URL)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, QUESTION_DETAIL_TEMPLATE)

    def test_view_has_additional_context_objects(self):
        """
        View should have additional context objects:
            * `page_title`
            * `question`
        """
        self.client.login(
            username=USERNAME_REGISTRATION_ACCEPTED_TRUE,
            password=PASSWORD_FOR_TESTING,
        )
        response = self.client.get(QUESTION_DETAIL_URL)
        self.assertEqual(response.status_code, 200)
        self.assertIn('page_title', response.context)
        self.assertIn('question', response.context)

    def test_view_has_correct_page_title(self):
        """
        View should have the correct page title:
            * `PAGE_TITLE_QUESTION_DETAIL`
        """
        self.client.login(
            username=USERNAME_REGISTRATION_ACCEPTED_TRUE,
            password=PASSWORD_FOR_TESTING,
        )
        response = self.client.get(QUESTION_DETAIL_URL)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.context['page_title'], PAGE_TITLE_QUESTION_DETAIL)

    def test_view_has_correct_question(self):
        """
        View should have the correct `Question` object:
            * `QUESTION_BODY`
        
        This test may not be needed.
        """
        self.client.login(
            username=USERNAME_REGISTRATION_ACCEPTED_TRUE,
            password=PASSWORD_FOR_TESTING,
        )
        response = self.client.get(QUESTION_DETAIL_URL)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.context['question'].body, QUESTION_BODY)

    def test_view_has_question_in_context(self):
        """
        View should have an instance of a `Question` object in the context.
        """
        self.client.login(
            username=USERNAME_REGISTRATION_ACCEPTED_TRUE,
            password=PASSWORD_FOR_TESTING,
        )
        response = self.client.get(QUESTION_DETAIL_URL)
        self.assertEqual(response.status_code, 200)
        self.assertIsInstance(response.context['question'], Question)


class QuestionListViewTest(TestCase):
    """
    Tests for `QuestionListView`.
    """
    @classmethod
    def setUpTestData(cls):
        """
        Create two `CustomUser`s and a selection of 11 `Questions`s for testing.

        This specific function name `setUpTestData` is required by Django.
        """

        # Create users:
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

        # Create some `Question`s for `user_registration_accepted_true`:
        number_of_questions = NUMBER_OF_QUESTIONS
        for question_id in range(number_of_questions):
            Question.objects.create(
                body=QUESTION_BODY,
                author=user_registration_accepted_true,
            )

    def test_view_url_redirects_to_login_if_user_not_authenticated(self):
        """
        View should redirect non-authenticated user to login view.
        """
        response = self.client.get(QUESTIONS_URL)
        self.assertRedirects(
            response,
            f'{LOGIN_URL}?next={QUESTIONS_URL}',
        )

    def test_view_url_for_authenticated_registration_accepted_true_user(self):
        """
        View should return `status_code` of 200 for authenticated user
        who has `registration_accepted=True`.
        """
        self.client.login(
            username=USERNAME_REGISTRATION_ACCEPTED_TRUE,
            password=PASSWORD_FOR_TESTING,
        )
        response = self.client.get(QUESTIONS_URL)
        self.assertEqual(response.status_code, 200)

    def test_view_url_accessible_by_name(self):
        """
        View should be accessible through the `APP_NAME:VIEW_NAME`.

        This tests functionality of `app_name` and `name` in `urlpatterns`
        list of `urls.py`.
        """
        self.client.login(
            username=USERNAME_REGISTRATION_ACCEPTED_TRUE,
            password=PASSWORD_FOR_TESTING,
        )
        response = self.client.get(reverse(QUESTIONS_VIEW_NAME))
        self.assertEqual(response.status_code, 200)

    def test_view_uses_correct_template(self):
        """
        View should use proper `QUESTIONS_TEMPLATE`.
        """
        self.client.login(
            username=USERNAME_REGISTRATION_ACCEPTED_TRUE,
            password=PASSWORD_FOR_TESTING,
        )
        response = self.client.get(QUESTIONS_URL)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, QUESTIONS_TEMPLATE)

    def test_view_has_additional_context_objects(self):
        """
        View should have additional context objects:
        - `the_site_name`
        - `page_title`
        """
        self.client.login(
            username=USERNAME_REGISTRATION_ACCEPTED_TRUE,
            password=PASSWORD_FOR_TESTING,
        )
        response = self.client.get(QUESTIONS_URL)
        self.assertEqual(response.status_code, 200)
        self.assertTrue('the_site_name' in response.context)
        self.assertTrue('page_title' in response.context)

    # def test_view_has_questions_in_proper_order(self):
    #     """
    #     View should have a `question_list` object in the context that is
    #     ordered by `created_at` in descending order.
    #     """
    #     # Log in a user:
    #     self.client.login(
    #         username=USERNAME_REGISTRATION_ACCEPTED_TRUE,
    #         password=PASSWORD_FOR_TESTING,
    #     )
    #     # Create a `Journal` object in the database since we need it to
    #     # create a `Question`:
    #     test_journal = Journal.objects.create(
    #         title=JOURNAL_TITLE,
    #         body=JOURNAL_BODY,
    #         author=CustomUser.objects.get(
    #             username=USERNAME_REGISTRATION_ACCEPTED_TRUE
    #         ),
    #     )
    #     # Create a `Question` object in the database:
    #     test_question_1 = Question.objects.create(
    #         body=QUESTION_BODY_01,
    #         author=CustomUser.objects.get(
    #             username=USERNAME_REGISTRATION_ACCEPTED_TRUE
    #         ),
    #     )
    #     test_question_1.journal.add(test_journal)
    #     # Create a second `Question` object in the database:
    #     test_question_2 = Question.objects.create(
    #         body=QUESTION_BODY_02,
    #         author=CustomUser.objects.get(
    #             username=USERNAME_REGISTRATION_ACCEPTED_TRUE
    #         ),
    #     )
    #     test_question_2.journal.add(test_journal)
    #     # Make a GET request to the view:
    #     response = self.client.get(QUESTIONS_URL)
    #     # Test that the `question_list` object in the context is ordered by
    #     # `created_at` in descending order:
    #     the_question_list = response.context['question_list']
    #     self.assertQuerysetEqual(
    #         response.context['question_list'],
    #         reversed(Question.objects.all()),
    #     )


class QuestionUpdateViewTest(TestCase):
#     """
#     Tests for `QuestionUpdateView`.
#     """
#     @classmethod
#     def setUpTestData(cls):
#         """
#         Create two `CustomUser`s and a selection of 11 `Questions`s for testing.

#         This specific function name `setUpTestData` is required by Django.
#         """

#         # Create users:
#         user_registration_accepted_true = CustomUser.objects.create(
#             username=USERNAME_REGISTRATION_ACCEPTED_TRUE,
#         )
#         user_registration_accepted_true.set_password(PASSWORD_FOR_TESTING)
#         user_registration_accepted_true.registration_accepted = True
#         user_registration_accepted_true.save()

#         user_registration_accepted_false = CustomUser.objects.create(
#             username=USERNAME_REGISTRATION_ACCEPTED_FALSE,
#         )
#         user_registration_accepted_false.set_password(PASSWORD_FOR_TESTING)
#         user_registration_accepted_false.registration_accepted = False
#         user_registration_accepted_false.save()

#         # Create some `Question`s for `user_registration_accepted_true`:
#         number_of_questions = NUMBER_OF_QUESTIONS
#         for question_id in range(number_of_questions):
#             Question.objects.create(
#                 body=QUESTION_BODY,
#                 author=user_registration_accepted_true,
#             )

#     def test_view_url_redirects_to_login_if_user_not_authenticated(self):
#         """
#         View should redirect non-authenticated user to login view.
#         """
#         response = self.client.get(
#             reverse(
#                 QUESTION_UPDATE_VIEW_NAME,
#                 kwargs={'pk': 1},
#             ),
#         )
#         self.assertRedirects(
#             response,
#             f'{LOGIN_URL}?next={QUESTION_UPDATE_URL}',
#         )

#     def test_view_url_for_authenticated_registration_accepted_true_user(self):
#         """
#         View should return `status_code` of 200 for authenticated user
#         who has `registration_accepted=True`.
#         """
#         self.client.login(
#             username=USERNAME_REGISTRATION_ACCEPTED_TRUE,
#             password=PASSWORD_FOR_TESTING,
#         )
#         response = self.client.get(
#             reverse(
#                 QUESTION_UPDATE_VIEW_NAME,
#                 kwargs={'pk': 1},
#             ),
#         )
#         self.assertEqual(response.status_code, 200)

#     def test_view_url_accessible_by_name(self):
#         """
#         View should be accessible through the `APP_NAME:VIEW_NAME`.

#         This tests functionality of `app_name` and `name` in `urlpatterns`
#         list of `urls.py`.
#         """
#         self.client.login(
#             username=USERNAME_REGISTRATION_ACCEPTED_TRUE,
#             password=PASSWORD_FOR_TESTING,
#         )
#         response = self.client.get(QUESTION_UPDATE_URL)
#         self.assertEqual(response.status_code, 200)
    pass
