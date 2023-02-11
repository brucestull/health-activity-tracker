from django.test import TestCase

from rodbt.models import Question
from accounts.models import CustomUser


THIRTY_PLUS_ONE_CHARACTERS = '1234567890123456789012345678901'
FOURTY_PLUS_ONE_CHARACTERS = '12345678901234567890123456789012345678901'
A_TEST_USERNAME = 'ACustomUser'
A_TEST_JOURNAL_BODY = (
    """
    This is a Journal Body, here. It's a long string of text, and it
    might not be tested for length, but it's here since we have to
    provide a 'body' when creating a `Journal`.
    """
)
A_TEST_QUESTION_BODY = (
    """
    This is a Question Body, here. It's a long string of text, and it
    might not be tested for length, but it's here since we have to
    provide a 'body' when creating a `Question`.    
    """
)


class QuestionModelTest(TestCase):

    @classmethod
    def setUpTestData(cls):
        """
        Set up non-modified objects used by all test methods.
        """
        author = CustomUser.objects.create(
            username=A_TEST_USERNAME,
        )
        Question.objects.create(
            author=author,
            body=A_TEST_QUESTION_BODY,
        )

    def test_author_related_name(self):
        """
        `author` related_name should be `questions`.
        """
        question = Question.objects.get(id=1)
        related_name = question._meta.get_field('author').related_query_name()
        self.assertEqual(related_name, 'questions')

    def test_body_label(self):
        """
        `body` field label should be `Question Body Text`.
        """
        question = Question.objects.get(id=1)
        field_label = question._meta.get_field('body').verbose_name
        self.assertEqual(field_label, 'Question Body Text')

    def test_body_max_length_attribute(self):
        """
        `body` field max_length should be 200.
        """
        question = Question.objects.get(id=1)
        max_length = question._meta.get_field('body').max_length
        self.assertEqual(max_length, 200)

    def test_date_label(self):
        """
        `date` field label should be `Created Date`.
        """
        question = Question.objects.get(id=1)
        field_label = question._meta.get_field('date').verbose_name
        self.assertEqual(field_label, 'Created Date')

    def test_date_auto_now_add_attribute(self):
        """
        `date` field auto_now_add should be True.
        """
        question = Question.objects.get(id=1)
        auto_now_add = question._meta.get_field('date').auto_now_add
        self.assertEqual(auto_now_add, True)

    def test_edited_date_label(self):
        """
        `edited_date` field label should be `Edited Date`.
        """
        question = Question.objects.get(id=1)
        field_label = question._meta.get_field('edited_date').verbose_name
        self.assertEqual(field_label, 'Edited Date')

    def test_edited_date_auto_now_attribute(self):
        """
        `edited_date` field auto_now should be True.
        """
        question = Question.objects.get(id=1)
        auto_now = question._meta.get_field('edited_date').auto_now
        self.assertEqual(auto_now, True)

    def test_journal_attribute_related_name(self):
        """
        `journal` related_name should be `questions`.
        """
        question = Question.objects.get(id=1)
        related_name = question._meta.get_field('journal').related_query_name()
        self.assertEqual(related_name, 'questions')

    def test_journal_attribute_blank_attribute(self):
        """
        `journal` field `blank` attribute should be `True`.
        """
        question = Question.objects.get(id=1)
        blank = question._meta.get_field('journal').blank
        self.assertTrue(blank)

    def test_dunder_str(self):
        """
        `__str__` should return the question `body` field, truncated to 40 characters.
        """
        question = Question.objects.get(id=1)
        expected_dunder_string = question.body[:40]
        self.assertEqual(str(question), expected_dunder_string)

    def test_get_absolute_url(self):
        """
        `get_absolute_url` should return the url for the question detail page.
        """
        question = Question.objects.get(id=1)
        self.assertEqual(question.get_absolute_url(), '/rodbt/questions/1/')
