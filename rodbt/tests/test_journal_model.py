from django.test import TestCase

from rodbt.models import Journal
from accounts.models import CustomUser


THIRTY_PLUS_ONE_CHARACTERS = '1234567890123456789012345678901'
A_TEST_USERNAME = 'ACustomUser'
A_TEST_JOURNAL_BODY = (
"""
This is a Journal Body, here. It's a long string of text, and it might
not be tested for length, but it's here since we have to provide a 'body'
when creating a `Journal`.
"""
)


class JournalModelTest(TestCase):

    @classmethod
    def setUpTestData(cls):
        """
        Set up non-modified objects used by all test methods.

        This specific function name `setUpTestData` is required by Django.
        """
        author = CustomUser.objects.create(
            username=A_TEST_USERNAME,
        )
        Journal.objects.create(
            author=author,
            title=THIRTY_PLUS_ONE_CHARACTERS,
            body=A_TEST_JOURNAL_BODY,
        )

    def test_author_related_name(self):
        """
        `author` related_name should be `journals`.
        """
        journal = Journal.objects.get(id=1)
        related_name = journal._meta.get_field('author').related_query_name()
        self.assertEqual(related_name, 'journals')

    def test_title_label(self):
        """
        `title` field label should be `Title`.
        """
        journal = Journal.objects.get(id=1)
        field_label = journal._meta.get_field('title').verbose_name
        self.assertEqual(field_label, 'Title')

    def test_title_max_length_attribute(self):
        """
        `title` field max_length should be 200.
        """
        journal = Journal.objects.get(id=1)
        max_length = journal._meta.get_field('title').max_length
        self.assertEqual(max_length, 200)

    def test_title_blank_attribute(self):
        """
        `title` field `blank` attribute should be `True`.
        """
        journal = Journal.objects.get(id=1)
        blank = journal._meta.get_field('title').blank
        self.assertTrue(blank)

    def test_title_null_attribute(self):
        """
        `title` field `null` attribute should be `True`.
        """
        journal = Journal.objects.get(id=1)
        null = journal._meta.get_field('title').null
        self.assertTrue(null)

    def test_body_label(self):
        """
        `body` field label should be `Journal Body Text`.
        """
        journal = Journal.objects.get(id=1)
        field_label = journal._meta.get_field('body').verbose_name
        self.assertEqual(field_label, 'Journal Body Text')

    def test_date_label(self):
        """
        `date` field label should be `Created Date`.
        """
        journal = Journal.objects.get(id=1)
        field_label = journal._meta.get_field('date').verbose_name
        self.assertEqual(field_label, 'Created Date')

    def test_date_auto_now_add_attribute(self):
        """
        `date` field `auto_now_add` attribute should be `True`.
        """
        journal = Journal.objects.get(id=1)
        auto_now_add = journal._meta.get_field('date').auto_now_add
        self.assertTrue(auto_now_add)

    def test_edited_date_label(self):
        """
        `edited_date` field label should be `Edited Date`.
        """
        journal = Journal.objects.get(id=1)
        field_label = journal._meta.get_field('edited_date').verbose_name
        self.assertEqual(field_label, 'Edited Date')

    def test_edited_date_auto_now_attribute(self):
        """
        `edited_date` field `auto_now` attribute should be `True`.
        """
        journal = Journal.objects.get(id=1)
        auto_now = journal._meta.get_field('edited_date').auto_now
        self.assertTrue(auto_now)

    def test_dunder_str(self):
        """
        `__str__` method should return `title` field value, truncated to
        30 characters.
        """
        journal = Journal.objects.get(id=1)
        expected_dunder_string = journal.title[:30]
        self.assertEqual(str(journal), expected_dunder_string)

    def test_get_absolute_url(self):
        """
        `get_absolute_url` should return the url to a journal's detail page.
        """
        author = Journal.objects.get(id=1)
        self.assertEqual(author.get_absolute_url(), '/rodbt/journals/1/')
