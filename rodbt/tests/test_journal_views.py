from django.test import TestCase, Client
from django.urls import reverse
from django.forms import TextInput, Textarea

from accounts.models import CustomUser
from rodbt.models import Journal


A_TEST_USERNAME = 'ACustomUser'
A_TEST_PASSWORD = 'a_test_password'

NUMBER_OF_JOURNALS = 11

JOURNAL_CREATE_URL = '/rodbt/journals/create/'
JOURNAL_CREATE_VIEW_NAME = 'rodbt:journal-create'

JOURNALS_URL = '/rodbt/journals/'
JOURNALS_VIEW_NAME = 'rodbt:journals'

JOURNAL_DETAIL_URL = '/rodbt/journals/1/'
JOURNAL_DETAIL_VIEW_NAME = 'rodbt:journal-detail'

A_TEST_JOURNAL_TITLE = 'A Test Journal Title'
A_TEST_JOURNAL_BODY = (
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
        Create a `CustomUser` for testing.
        """

        # Create a user.
        the_test_user = CustomUser.objects.create(
            username=A_TEST_USERNAME,
        )
        the_test_user.set_password(A_TEST_PASSWORD)
        the_test_user.save()

    def test_view_url_redirect_if_not_logged_in(self):
        """
        AnonymousUser HTTP request to `/rodbt/journals/create/` should
        redirect to `/accounts/login/`.

        Test that the view redirects to the login page if the user is not
        logged in.
        """
        response = self.client.get('/rodbt/journals/create/')
        self.assertRedirects(response, '/accounts/login/?next=/rodbt/journals/create/')

    def test_view_url_for_logged_in_user(self):
        """
        HTTP request to `/rodbt/journals/create/` should return a `200`
        status code.

        Test that the view is accessible if the user is logged in.
        """
        login = self.client.login(
            username=A_TEST_USERNAME,
            password=A_TEST_PASSWORD,
        )
        response = self.client.get(JOURNAL_CREATE_URL)
        self.assertEqual(response.status_code, 200)

    def test_view_url_accessible_by_name(self):
        """
        HTTP request to `/rodbt/journals/create/` should return a `200`
        status code.

        Test that the view is accessible by name.
        """
        login = self.client.login(
            username=A_TEST_USERNAME,
            password=A_TEST_PASSWORD,
        )
        response = self.client.get(reverse('rodbt:journal-create'))
        self.assertEqual(response.status_code, 200)

    def test_view_uses_correct_template(self):
        """
        HTTP request to `/rodbt/journals/create/` should use the correct
        template.

        Test that the view uses the correct template.
        """
        login = self.client.login(
            username=A_TEST_USERNAME,
            password=A_TEST_PASSWORD,
        )
        response = self.client.get(JOURNAL_CREATE_URL)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'rodbt/journal_form.html')

    def test_view_has_extra_context_objects(self):
        """
        HTTP request to `/rodbt/journals/create/` should have the correct
        extra context objects: `the_site_name` and `page_title`.

        Test that the view has the correct extra context objects.
        """
        login = self.client.login(
            username=A_TEST_USERNAME,
            password=A_TEST_PASSWORD,
        )
        response = self.client.get(JOURNAL_CREATE_URL)
        self.assertEqual(response.status_code, 200)
        self.assertTrue('the_site_name' in response.context)
        self.assertTrue('page_title' in response.context)

    def test_view_has_form(self):
        """
        HTTP request to `/rodbt/journals/create/` should have a form.

        Test that the view has a form.
        """
        login = self.client.login(
            username=A_TEST_USERNAME,
            password=A_TEST_PASSWORD,
        )
        response = self.client.get(JOURNAL_CREATE_URL)
        self.assertEqual(response.status_code, 200)
        self.assertTrue('form' in response.context)

    def test_view_form_has_correct_fields(self):
        """
        HTTP request to `/rodbt/journals/create/` should have a form with
        the correct fields:
            * `title`
            * `body`

        Test that the view has a form with the correct fields.
        """
        login = self.client.login(
            username=A_TEST_USERNAME,
            password=A_TEST_PASSWORD,
        )
        response = self.client.get(JOURNAL_CREATE_URL)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(
            list(response.context['form'].fields),
            [
                'title',
                'body',
            ]
        )

    def test_view_form_has_correct_labels(self):
        """
        HTTP request to `/rodbt/journals/create/` should have a form with
        the correct labels:
            * `Title`
            * `Journal Body Text`

        Test that the view has a form with the correct labels.
        """
        login = self.client.login(
            username=A_TEST_USERNAME,
            password=A_TEST_PASSWORD,
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


class JournalDetailViewTest(TestCase):
    """
    Test the `JournalDetailView`.
    """
    @classmethod
    def setUpTestData(cls):
        """
        Create a `CustomUser` and a `Journal` for testing.
        """

        # Create a user.
        the_test_user = CustomUser.objects.create(
            username=A_TEST_USERNAME,
        )
        the_test_user.set_password(A_TEST_PASSWORD)
        the_test_user.save()

        # Create a `Journal` for `the_test_user`.
        Journal.objects.create(
            author=the_test_user,
            title=A_TEST_JOURNAL_TITLE,
            body=A_TEST_JOURNAL_BODY,
        )

    def test_view_url_redirect_if_not_logged_in(self):
        """
        AnonymousUser HTTP request to `/rodbt/journals/1/` should redirect
        to `/accounts/login/`.

        Test that the view redirects to the login page if the user is not
        logged in.
        """
        response = self.client.get(JOURNAL_DETAIL_URL)
        self.assertRedirects(response, '/accounts/login/?next=/rodbt/journals/1/')

    def test_view_url_for_logged_in_user(self):
        """
        HTTP request to `/rodbt/journals/1/` should return a `200` status
        code.

        Test that the view is accessible if the user is logged in.
        """
        login = self.client.login(
            username=A_TEST_USERNAME,
            password=A_TEST_PASSWORD,
        )
        response = self.client.get(JOURNAL_DETAIL_URL)
        self.assertEqual(response.status_code, 200)

    def test_view_url_accessible_by_name(self):
        """
        HTTP request to `/rodbt/journals/1/` should return a `200` status
        code.

        Test that the view is accessible by name.
        """
        login = self.client.login(
            username=A_TEST_USERNAME,
            password=A_TEST_PASSWORD,
        )
        response = self.client.get(reverse('rodbt:journal-detail', args=[1]))
        self.assertEqual(response.status_code, 200)

    def test_view_uses_correct_template(self):
        """
        HTTP request to `/rodbt/journals/1/` should use the correct
        template.

        Test that the view uses the correct template.
        """
        login = self.client.login(
            username=A_TEST_USERNAME,
            password=A_TEST_PASSWORD,
        )
        response = self.client.get(JOURNAL_DETAIL_URL)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'rodbt/journal_detail.html')

    def test_view_has_correct_context(self):
        """
        HTTP request to `/rodbt/journals/1/` should have the correct
        context:
            * `page_title`
            * `journal`

        Test that the view has the correct context.
        """
        login = self.client.login(
            username=A_TEST_USERNAME,
            password=A_TEST_PASSWORD,
        )
        response = self.client.get(JOURNAL_DETAIL_URL)
        self.assertEqual(response.status_code, 200)
        self.assertTrue('page_title' in response.context)
        self.assertTrue('journal' in response.context)

    def test_view_has_correct_page_title(self):
        """
        HTTP request to `/rodbt/journals/1/` should have the correct page
        title.

        Test that the view has the correct page title.
        """
        login = self.client.login(
            username=A_TEST_USERNAME,
            password=A_TEST_PASSWORD,
        )
        response = self.client.get(JOURNAL_DETAIL_URL)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.context['page_title'], PAGE_TITLE_JOURNAL_DETAIL)

    def test_view_has_correct_journal(self):
        """
        HTTP request to `/rodbt/journals/1/` should have the correct
        `Journal`.

        Test that the view has the correct `Journal`.
        """
        login = self.client.login(
            username=A_TEST_USERNAME,
            password=A_TEST_PASSWORD,
        )
        response = self.client.get(JOURNAL_DETAIL_URL)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.context['journal'].title, A_TEST_JOURNAL_TITLE)
        self.assertEqual(response.context['journal'].body, A_TEST_JOURNAL_BODY)

    def test_view_returns_a_journal(self):
        """
        HTTP request to `/rodbt/journals/1/` should return a `Journal`.

        Test that the view returns a `Journal`.
        """
        login = self.client.login(
            username=A_TEST_USERNAME,
            password=A_TEST_PASSWORD,
        )
        response = self.client.get(JOURNAL_DETAIL_URL) # TemplateResponse
        # response_journal = response.context['journal'] # Journal
        self.assertEqual(response.status_code, 200)
        self.assertIsInstance(response.context['journal'], Journal)


class JournalListViewTest(TestCase):
    """
    Test the `JournalListView`.
    """
    @classmethod
    def setUpTestData(cls):
        """
        Create a `CustomUser` and a selection of 11 `Journal`s for testing.
        """

        # Create a user.
        the_test_user = CustomUser.objects.create(
            username=A_TEST_USERNAME,
        )
        the_test_user.set_password(A_TEST_PASSWORD)
        the_test_user.save()

        # Create some `Journal`s for `the_test_user`.
        number_of_journals = NUMBER_OF_JOURNALS
        for journal_id in range(number_of_journals):
            Journal.objects.create(
                author=the_test_user,
                title=f'Journal {journal_id} Title',
                body=f'Journal {journal_id} body text',
            )

    def test_view_url_redirect_if_not_logged_in(self):
        """
        AnonymousUser HTTP request to `/rodbt/journals/` should redirect to
        `/accounts/login/`.

        Test that the view redirects to the login page if the user is not
        logged in.
        """
        response = self.client.get(JOURNALS_URL)
        self.assertRedirects(response, '/accounts/login/?next=/rodbt/journals/')

    def test_view_url_for_logged_in_user(self):
        """
        HTTP request to `/rodbt/journals/` should return a `200` status code.

        Test that the view is accessible if the user is logged in.
        """
        login = self.client.login(
            username=A_TEST_USERNAME,
            password=A_TEST_PASSWORD,
        )
        response = self.client.get(JOURNALS_URL)
        self.assertEqual(response.status_code, 200)

    # TODO: This test may need refinement.
    def test_view_url_accessible_by_name(self):
        """
        HTTP request to `/rodbt/journals/` should return a `200` status code.

        Test that the view is accessible by name.
        """
        login = self.client.login(
            username=A_TEST_USERNAME,
            password=A_TEST_PASSWORD,
        )
        response = self.client.get(reverse('rodbt:journals'))
        self.assertEqual(response.status_code, 200)

    def test_view_uses_correct_template(self):
        """
        HTTP request to `/rodbt/journals/` should use the correct template.

        Test that the view uses the correct template.
        """
        login = self.client.login(
            username=A_TEST_USERNAME,
            password=A_TEST_PASSWORD,
        )
        response = self.client.get(JOURNALS_URL)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'rodbt/journal_list.html')

    # TODO: Test, pagination, that the view returns the correct number
    # of `Journal`s.

    def test_view_default_context_object_names(self):
        """
        HTTP request to `/rodbt/journals/` should use the correct context
        object name.

        Test that the view uses the correct context object name.
        """
        login = self.client.login(
            username=A_TEST_USERNAME,
            password=A_TEST_PASSWORD,
        )
        response = self.client.get(JOURNALS_URL)
        self.assertEqual(response.status_code, 200)
        self.assertTrue('journal_list' in response.context)
        self.assertTrue('object_list' in response.context)

    def test_view_context_has_extra_context_objects(self):
        """
        HTTP request to `/rodbt/journals/` should have the correct extra
        context objects:
            * `the_site_name`
            * `page_title`

        Test that the view has the correct extra context objects.
        """
        login = self.client.login(
            username=A_TEST_USERNAME,
            password=A_TEST_PASSWORD,
        )
        response = self.client.get(JOURNALS_URL)
        self.assertEqual(response.status_code, 200)
        self.assertTrue('the_site_name' in response.context)
        self.assertTrue('page_title' in response.context)

    def test_queryset(self):
        """
        HTTP request to `/rodbt/journals/` should return the correct
        number of `Journal`s.

        Test that the view returns the correct number of `Journal`s.
        """
        login = self.client.login(
            username=A_TEST_USERNAME,
            password=A_TEST_PASSWORD,
        )
        response = self.client.get(JOURNALS_URL)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.context['journal_list']), NUMBER_OF_JOURNALS)




