# Massive Failure of Tests After Addition of UserPassesTestMixin

* Abundant 403 errors:
  * This was expected since we added code to require a user pass (`UserPassesTestMixin`) a test to access a view.
  * Need to make `<test_user>.registration_accepted = True`.

```console
Found 51 test(s).
Creating test database for alias 'default'...
System check identified no issues (0 silenced).
.................FFFFFF.FFFFFFF.FFFFFF.F...........
======================================================================
FAIL: test_view_form_has_correct_fields (rodbt.tests.test_journal_views.JournalCreateViewTest.test_view_form_has_correct_fields)
HTTP request to `/rodbt/journals/create/` should have a form with
----------------------------------------------------------------------
Traceback (most recent call last):
  File "C:\Users\FlynntKnapp\Programming\health-activity-tracker\rodbt\tests\test_journal_views.py", line 153, in test_view_form_has_correct_fields
    self.assertEqual(response.status_code, 200)
AssertionError: 403 != 200

======================================================================
FAIL: test_view_form_has_correct_labels (rodbt.tests.test_journal_views.JournalCreateViewTest.test_view_form_has_correct_labels)
HTTP request to `/rodbt/journals/create/` should have a form with
----------------------------------------------------------------------
Traceback (most recent call last):
  File "C:\Users\FlynntKnapp\Programming\health-activity-tracker\rodbt\tests\test_journal_views.py", line 176, in test_view_form_has_correct_labels
    self.assertEqual(response.status_code, 200)
AssertionError: 403 != 200

======================================================================
FAIL: test_view_has_extra_context_objects (rodbt.tests.test_journal_views.JournalCreateViewTest.test_view_has_extra_context_objects)
HTTP request to `/rodbt/journals/create/` should have the correct
----------------------------------------------------------------------
Traceback (most recent call last):
  File "C:\Users\FlynntKnapp\Programming\health-activity-tracker\rodbt\tests\test_journal_views.py", line 121, in test_view_has_extra_context_objects
    self.assertEqual(response.status_code, 200)
AssertionError: 403 != 200

======================================================================
FAIL: test_view_has_form (rodbt.tests.test_journal_views.JournalCreateViewTest.test_view_has_form)
HTTP request to `/rodbt/journals/create/` should have a form.
----------------------------------------------------------------------
Traceback (most recent call last):
  File "C:\Users\FlynntKnapp\Programming\health-activity-tracker\rodbt\tests\test_journal_views.py", line 136, in test_view_has_form
    self.assertEqual(response.status_code, 200)
AssertionError: 403 != 200

======================================================================
FAIL: test_view_url_accessible_by_name (rodbt.tests.test_journal_views.JournalCreateViewTest.test_view_url_accessible_by_name)
HTTP request to `/rodbt/journals/create/` should return a `200`
----------------------------------------------------------------------
Traceback (most recent call last):
  File "C:\Users\FlynntKnapp\Programming\health-activity-tracker\rodbt\tests\test_journal_views.py", line 92, in test_view_url_accessible_by_name
    self.assertEqual(response.status_code, 200)
AssertionError: 403 != 200

======================================================================
FAIL: test_view_url_for_logged_in_user (rodbt.tests.test_journal_views.JournalCreateViewTest.test_view_url_for_logged_in_user)
HTTP request to `/rodbt/journals/create/` should return a `200`
----------------------------------------------------------------------
Traceback (most recent call last):
  File "C:\Users\FlynntKnapp\Programming\health-activity-tracker\rodbt\tests\test_journal_views.py", line 78, in test_view_url_for_logged_in_user
    self.assertEqual(response.status_code, 200)
AssertionError: 403 != 200

======================================================================
FAIL: test_view_uses_correct_template (rodbt.tests.test_journal_views.JournalCreateViewTest.test_view_uses_correct_template)
HTTP request to `/rodbt/journals/create/` should use the correct
----------------------------------------------------------------------
Traceback (most recent call last):
  File "C:\Users\FlynntKnapp\Programming\health-activity-tracker\rodbt\tests\test_journal_views.py", line 106, in test_view_uses_correct_template
    self.assertEqual(response.status_code, 200)
AssertionError: 403 != 200

======================================================================
FAIL: test_view_has_correct_context (rodbt.tests.test_journal_views.JournalDetailViewTest.test_view_has_correct_context)
HTTP request to `/rodbt/journals/1/` should have the correct
----------------------------------------------------------------------
Traceback (most recent call last):
  File "C:\Users\FlynntKnapp\Programming\health-activity-tracker\rodbt\tests\test_journal_views.py", line 282, in test_view_has_correct_context
    self.assertEqual(response.status_code, 200)
AssertionError: 403 != 200

======================================================================
FAIL: test_view_has_correct_journal (rodbt.tests.test_journal_views.JournalDetailViewTest.test_view_has_correct_journal)
HTTP request to `/rodbt/journals/1/` should have the correct
----------------------------------------------------------------------
Traceback (most recent call last):
  File "C:\Users\FlynntKnapp\Programming\health-activity-tracker\rodbt\tests\test_journal_views.py", line 313, in test_view_has_correct_journal
    self.assertEqual(response.status_code, 200)
AssertionError: 403 != 200

======================================================================
FAIL: test_view_has_correct_page_title (rodbt.tests.test_journal_views.JournalDetailViewTest.test_view_has_correct_page_title)
HTTP request to `/rodbt/journals/1/` should have the correct page
----------------------------------------------------------------------
Traceback (most recent call last):
  File "C:\Users\FlynntKnapp\Programming\health-activity-tracker\rodbt\tests\test_journal_views.py", line 298, in test_view_has_correct_page_title
    self.assertEqual(response.status_code, 200)
AssertionError: 403 != 200

======================================================================
FAIL: test_view_returns_a_journal (rodbt.tests.test_journal_views.JournalDetailViewTest.test_view_returns_a_journal)
HTTP request to `/rodbt/journals/1/` should return a `Journal`.
----------------------------------------------------------------------
Traceback (most recent call last):
  File "C:\Users\FlynntKnapp\Programming\health-activity-tracker\rodbt\tests\test_journal_views.py", line 329, in test_view_returns_a_journal
    self.assertEqual(response.status_code, 200)
AssertionError: 403 != 200

======================================================================
FAIL: test_view_url_accessible_by_name (rodbt.tests.test_journal_views.JournalDetailViewTest.test_view_url_accessible_by_name)
HTTP request to `/rodbt/journals/1/` should return a `200` status
----------------------------------------------------------------------
Traceback (most recent call last):
  File "C:\Users\FlynntKnapp\Programming\health-activity-tracker\rodbt\tests\test_journal_views.py", line 251, in test_view_url_accessible_by_name
    self.assertEqual(response.status_code, 200)
AssertionError: 403 != 200

======================================================================
FAIL: test_view_url_for_logged_in_user (rodbt.tests.test_journal_views.JournalDetailViewTest.test_view_url_for_logged_in_user)
HTTP request to `/rodbt/journals/1/` should return a `200` status
----------------------------------------------------------------------
Traceback (most recent call last):
  File "C:\Users\FlynntKnapp\Programming\health-activity-tracker\rodbt\tests\test_journal_views.py", line 237, in test_view_url_for_logged_in_user
    self.assertEqual(response.status_code, 200)
AssertionError: 403 != 200

======================================================================
FAIL: test_view_uses_correct_template (rodbt.tests.test_journal_views.JournalDetailViewTest.test_view_uses_correct_template)
HTTP request to `/rodbt/journals/1/` should use the correct
----------------------------------------------------------------------
Traceback (most recent call last):
  File "C:\Users\FlynntKnapp\Programming\health-activity-tracker\rodbt\tests\test_journal_views.py", line 265, in test_view_uses_correct_template
    self.assertEqual(response.status_code, 200)
AssertionError: 403 != 200

======================================================================
FAIL: test_queryset (rodbt.tests.test_journal_views.JournalListViewTest.test_queryset)
HTTP request to `/rodbt/journals/` should return the correct
----------------------------------------------------------------------
Traceback (most recent call last):
  File "C:\Users\FlynntKnapp\Programming\health-activity-tracker\rodbt\tests\test_journal_views.py", line 463, in test_queryset
    self.assertEqual(response.status_code, 200)
AssertionError: 403 != 200

======================================================================
FAIL: test_view_context_has_extra_context_objects (rodbt.tests.test_journal_views.JournalListViewTest.test_view_context_has_extra_context_objects)
HTTP request to `/rodbt/journals/` should have the correct extra
----------------------------------------------------------------------
Traceback (most recent call last):
  File "C:\Users\FlynntKnapp\Programming\health-activity-tracker\rodbt\tests\test_journal_views.py", line 447, in test_view_context_has_extra_context_objects
    self.assertEqual(response.status_code, 200)
AssertionError: 403 != 200

======================================================================
FAIL: test_view_default_context_object_names (rodbt.tests.test_journal_views.JournalListViewTest.test_view_default_context_object_names)
HTTP request to `/rodbt/journals/` should use the correct context
----------------------------------------------------------------------
Traceback (most recent call last):
  File "C:\Users\FlynntKnapp\Programming\health-activity-tracker\rodbt\tests\test_journal_views.py", line 429, in test_view_default_context_object_names
    self.assertEqual(response.status_code, 200)
AssertionError: 403 != 200

======================================================================
FAIL: test_view_url_accessible_by_name (rodbt.tests.test_journal_views.JournalListViewTest.test_view_url_accessible_by_name)
HTTP request to `/rodbt/journals/` should return a `200` status code.
----------------------------------------------------------------------
Traceback (most recent call last):
  File "C:\Users\FlynntKnapp\Programming\health-activity-tracker\rodbt\tests\test_journal_views.py", line 398, in test_view_url_accessible_by_name
    self.assertEqual(response.status_code, 200)
AssertionError: 403 != 200

======================================================================
FAIL: test_view_url_for_logged_in_user (rodbt.tests.test_journal_views.JournalListViewTest.test_view_url_for_logged_in_user)
HTTP request to `/rodbt/journals/` should return a `200` status code.
----------------------------------------------------------------------
Traceback (most recent call last):
  File "C:\Users\FlynntKnapp\Programming\health-activity-tracker\rodbt\tests\test_journal_views.py", line 384, in test_view_url_for_logged_in_user
    self.assertEqual(response.status_code, 200)
AssertionError: 403 != 200

======================================================================
FAIL: test_view_uses_correct_template (rodbt.tests.test_journal_views.JournalListViewTest.test_view_uses_correct_template)
HTTP request to `/rodbt/journals/` should use the correct template.
----------------------------------------------------------------------
Traceback (most recent call last):
  File "C:\Users\FlynntKnapp\Programming\health-activity-tracker\rodbt\tests\test_journal_views.py", line 411, in test_view_uses_correct_template
    self.assertEqual(response.status_code, 200)
AssertionError: 403 != 200

----------------------------------------------------------------------
Ran 51 tests in 4.961s

FAILED (failures=20)
Destroying test database for alias 'default'...
(health-activity-tracker) PS C:\Users\FlynntKnapp\Programming\health-activity-tracker>
```
