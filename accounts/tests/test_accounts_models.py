from django.test import TestCase

from accounts.models import CustomUser

A_TEST_USERNAME = 'ACustomUserModelTestUsername'


class CustomUserModelTest(TestCase):
    """
    Tests for the `CustomUser` model.
    """
    
    @classmethod
    def setUpTestData(cls):
        """
        Set up non-modified objects used by all test methods.

        This specific function name `setUpTestData` is required by Django.
        """
        CustomUser.objects.create(
            username=A_TEST_USERNAME,
        )

    def test_registration_accepted_label(self):
        """
        `registration_accepted` label should be 'Registration Accepted'.
        """
        custom_user = CustomUser.objects.get(id=1)
        field_label = custom_user._meta.get_field('registration_accepted').verbose_name
        self.assertEqual(field_label, 'Registration Accepted')

    def test_registration_accepted_default_value(self):
        """
        `registration_accepted` default value should be `False`.
        """
        custom_user = CustomUser.objects.get(id=1)
        self.assertEqual(custom_user.registration_accepted, False)

    def test_is_moderator_label(self):
        """
        `is_moderator` label should be 'Is Moderator'.
        """
        custom_user = CustomUser.objects.get(id=1)
        field_label = custom_user._meta.get_field('is_moderator').verbose_name
        self.assertEqual(field_label, 'Is Moderator')

    def test_is_moderator_default_value(self):
        """
        `is_moderator` default value should be `False`.
        """
        custom_user = CustomUser.objects.get(id=1)
        self.assertEqual(custom_user.is_moderator, False)

    def test_dunder_str(self):
        """
        `__str__` method should return the "<USER>.id : <USER>.username".
        """
        custom_user = CustomUser.objects.get(id=1)
        expected_string = str(custom_user.id) + ' : ' + custom_user.username
        self.assertEqual(str(custom_user), expected_string)
