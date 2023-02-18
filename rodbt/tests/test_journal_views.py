from django.test import TestCase
from django.urls import reverse

from accounts.models import CustomUser
from rodbt.models import Journal


USERNAME_REGISTRATION_ACCEPTED_TRUE = 'RegisteredUser'
USERNAME_REGISTRATION_ACCEPTED_FALSE = 'UnregisteredUser'
PASSWORD_FOR_TESTING = 'a_test_password'

LOGIN_URL = '/accounts/login/'

NUMBER_OF_JOURNALS = 11

JOURNAL_CREATE_URL = '/rodbt/journals/create/'
JOURNAL_CREATE_VIEW_NAME = 'rodbt:journal-create'
JOURNAL_CREATE_TEMPLATE = 'rodbt/journal_form.html'

JOURNALS_URL = '/rodbt/journals/'
JOURNALS_VIEW_NAME = 'rodbt:journals'
JOURNALS_TEMPLATE = 'rodbt/journal_list.html'

JOURNAL_DETAIL_URL = '/rodbt/journals/1/'
JOURNAL_DETAIL_VIEW_NAME = 'rodbt:journal-detail'
JOURNAL_DETAIL_TEMPLATE = 'rodbt/journal_detail.html'

JOURNAL_TITLE = 'A Test Journal Title'
JOURNAL_BODY = (
"""
This is a Journal Body, here. It's a long string of text, and it might
not be tested for length, but it's here since we have to provide a 'body'
when creating a `Journal`.
"""
)

PAGE_TITLE_JOURNAL_DETAIL = 'Journal Detail'


class JournalCreateViewTest(TestCase):
    """
    Test the `JournalCreateView`.
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
        View should redirect non-authenticated user to login view.
        """
        response = self.client.get(JOURNAL_CREATE_URL)
        self.assertRedirects(
            response,
            f'{LOGIN_URL}?next={JOURNAL_CREATE_URL}'
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
        response = self.client.get(JOURNAL_CREATE_URL)
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
        response = self.client.get(JOURNAL_CREATE_URL)
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
        response = self.client.get(reverse(JOURNAL_CREATE_VIEW_NAME))
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
        response = self.client.get(JOURNAL_CREATE_URL)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, JOURNAL_CREATE_TEMPLATE)

    def test_view_has_extra_context_objects(self):
        """
        View should have additional context objects:
        - `the_site_name`
        - `page_title`
        """
        self.client.login(
            username=USERNAME_REGISTRATION_ACCEPTED_TRUE,
            password=PASSWORD_FOR_TESTING,
        )
        response = self.client.get(JOURNAL_CREATE_URL)
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
        response = self.client.get(JOURNAL_CREATE_URL)
        self.assertEqual(response.status_code, 200)
        self.assertTrue('form' in response.context)

    def test_view_form_has_correct_fields(self):
        """
        HTTP request to the view URL should have a form with the correct
        fields:
            * `title`
            * `body`

        Test that the view has a form with the correct fields.
        """
        self.client.login(
            username=USERNAME_REGISTRATION_ACCEPTED_TRUE,
            password=PASSWORD_FOR_TESTING,
        )
        response = self.client.get(JOURNAL_CREATE_URL)
        self.assertEqual(response.status_code, 200)
        # This tests that the form has the correct fields and they are
        # in the correct order.
        self.assertEqual(
            list(response.context['form'].fields),
            [
                'title',
                'body',
            ]
        )

    def test_view_form_has_correct_labels(self):
        """
        Form inputs should have correct labels:
            * `title` -> `Title`
            * `body` -> `Journal Body Text`
        """
        self.client.login(
            username=USERNAME_REGISTRATION_ACCEPTED_TRUE,
            password=PASSWORD_FOR_TESTING,
        )
        response = self.client.get(JOURNAL_CREATE_URL)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(
            response.context['form'].fields['title'].label,
            'Title'
        )
        self.assertEqual(
            response.context['form'].fields['body'].label,
            'Journal Body Text'
        )

    def test_view_redirects_to_new_journal_on_successful_post(self):
        """
        View should redirect to the newly created `Journal` on successful
        POST.
        """
        self.client.login(
            username=USERNAME_REGISTRATION_ACCEPTED_TRUE,
            password=PASSWORD_FOR_TESTING,
        )
        response = self.client.post(
            JOURNAL_CREATE_URL,
            {
                'title': JOURNAL_TITLE,
                'body': JOURNAL_BODY,
            }
        )
        # Get the newly created `Journal` object:
        new_journal = Journal.objects.get(title=JOURNAL_TITLE)
        # Test that the view redirects to the newly created `Journal`:
        self.assertRedirects(
            response,
            reverse(
                JOURNAL_DETAIL_VIEW_NAME,
                kwargs={'pk': new_journal.pk}
            )
        )


class JournalDetailViewTest(TestCase):
    """
    Test the `JournalDetailView`.
    """
    @classmethod
    def setUpTestData(cls):
        """
        Create two `CustomUser`s and a `Journal` for testing.

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

        # Create a `Journal` for `user_registration_accepted_true`.
        Journal.objects.create(
            author=user_registration_accepted_true,
            # Alternate `author` syntax:
            # author=CustomUser.objects.get(
            #     username=USERNAME_REGISTRATION_ACCEPTED_TRUE
            # ),
            title=JOURNAL_TITLE,
            body=JOURNAL_BODY,
        )

    def test_view_url_redirects_to_login_if_user_not_authenticated(self):
        """
        View should redirect non-authenticated user to login view.
        """
        response = self.client.get(JOURNAL_DETAIL_URL)
        self.assertRedirects(
            response,
            f'{LOGIN_URL}?next={JOURNAL_DETAIL_URL}'
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
        response = self.client.get(JOURNAL_DETAIL_URL)
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
        response = self.client.get(JOURNAL_DETAIL_URL)
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
        the_existing_journal = Journal.objects.get(title=JOURNAL_TITLE)
        response = self.client.get(
            reverse(
                JOURNAL_DETAIL_VIEW_NAME,
                args=[the_existing_journal.id]
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
        response = self.client.get(JOURNAL_DETAIL_URL)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, JOURNAL_DETAIL_TEMPLATE)

    def test_view_has_additional_context_objects(self):
        """
        View should have additional context objects:
            * `page_title`
            * `journal`
        """
        self.client.login(
            username=USERNAME_REGISTRATION_ACCEPTED_TRUE,
            password=PASSWORD_FOR_TESTING,
        )
        response = self.client.get(JOURNAL_DETAIL_URL)
        self.assertEqual(response.status_code, 200)
        self.assertTrue('page_title' in response.context)
        self.assertTrue('journal' in response.context)

    def test_view_has_correct_page_title(self):
        """
        View should have the correct page title:
            * `PAGE_TITLE_JOURNAL_DETAIL`
        """
        self.client.login(
            username=USERNAME_REGISTRATION_ACCEPTED_TRUE,
            password=PASSWORD_FOR_TESTING,
        )
        response = self.client.get(JOURNAL_DETAIL_URL)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.context['page_title'], PAGE_TITLE_JOURNAL_DETAIL)

    def test_view_has_correct_journal(self):
        """
        View should have the correct `Journal`:
            * `JOURNAL_TITLE`
            * `JOURNAL_BODY`

        This test may not be needed.
        """
        self.client.login(
            username=USERNAME_REGISTRATION_ACCEPTED_TRUE,
            password=PASSWORD_FOR_TESTING,
        )
        response = self.client.get(JOURNAL_DETAIL_URL)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.context['journal'].title, JOURNAL_TITLE)
        self.assertEqual(response.context['journal'].body, JOURNAL_BODY)

    def test_view_has_journal_in_context(self):
        """
        View should have an instance of a `Journal` object in the context.
        """
        self.client.login(
            username=USERNAME_REGISTRATION_ACCEPTED_TRUE,
            password=PASSWORD_FOR_TESTING,
        )
        response = self.client.get(JOURNAL_DETAIL_URL) # TemplateResponse
        # response_journal = response.context['journal'] # Journal
        self.assertEqual(response.status_code, 200)
        self.assertIsInstance(response.context['journal'], Journal)


class JournalListViewTest(TestCase):
    """
    Tests the `JournalListView`.
    """
    @classmethod
    def setUpTestData(cls):
        """
        Create two `CustomUser`s and a selection of 11 `Journal`s for testing.

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

        # Create some `Journal`s for `registered_user`.
        number_of_journals = NUMBER_OF_JOURNALS
        for journal_id in range(number_of_journals):
            Journal.objects.create(
                author=user_registration_accepted_true,
                title=f'Journal {journal_id} Title',
                body=f'Journal {journal_id} body text',
            )

    def test_view_url_redirects_to_login_if_user_not_authenticated(self):
        """
        View should redirect non-authenticated user to login view.
        """
        response = self.client.get(JOURNALS_URL)
        self.assertRedirects(
            response,
            f'{LOGIN_URL}?next={JOURNALS_URL}'
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
        response = self.client.get(JOURNALS_URL)
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
        response = self.client.get(JOURNALS_URL)
        self.assertEqual(response.status_code, 200)

    # TODO: This test may need refinement.
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
        response = self.client.get(reverse(JOURNALS_VIEW_NAME))
        self.assertEqual(response.status_code, 200)

    def test_view_uses_correct_template(self):
        """
        View should use the proper `JOURNALS_TEMPLATE`.
        """
        self.client.login(
            username=USERNAME_REGISTRATION_ACCEPTED_TRUE,
            password=PASSWORD_FOR_TESTING,
        )
        response = self.client.get(JOURNALS_URL)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, JOURNALS_TEMPLATE)

    # TODO: Test, pagination, that the view returns the correct number
    # of `Journal`s.

    def test_view_default_context_object_names(self):
        """
        View should have the correct default context object names.

        This test is probably not neccessary since Django provides the
        code for these context objects.
        """
        self.client.login(
            username=USERNAME_REGISTRATION_ACCEPTED_TRUE,
            password=PASSWORD_FOR_TESTING,
        )
        response = self.client.get(JOURNALS_URL)
        self.assertEqual(response.status_code, 200)
        self.assertTrue('journal_list' in response.context)
        self.assertTrue('object_list' in response.context)

    def test_view_has_additional_context_objects(self):
        """
        View should have additional context objects:
            * `the_site_name`
            * `page_title`
        """
        self.client.login(
            username=USERNAME_REGISTRATION_ACCEPTED_TRUE,
            password=PASSWORD_FOR_TESTING,
        )
        response = self.client.get(JOURNALS_URL)
        self.assertEqual(response.status_code, 200)
        self.assertTrue('the_site_name' in response.context)
        self.assertTrue('page_title' in response.context)

    def test_queryset(self):
        """
        Length of context `journal_list` should be equal to `NUMBER_OF_JOURNALS`.
        """
        self.client.login(
            username=USERNAME_REGISTRATION_ACCEPTED_TRUE,
            password=PASSWORD_FOR_TESTING,
        )
        response = self.client.get(JOURNALS_URL)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(
            len(response.context['journal_list']),
            NUMBER_OF_JOURNALS
        )
