# Health Activity Tracker

## Heroku Links

* Production Deployment:
  * <https://flynnt-knapp-health-tracker.herokuapp.com/>

## Application Structure

* RO-DBT:
  * `rodbt`:
    * Self-Enquiry Journal:
      * Possible Models and Fields:
        * `Journal`:
          * `author` - ForeignKey to `CustomUser`
          * `tags` - ManyToManyField to `Tag`
          * `title`
          * `body`
          * `date`
          * `edited_date`
        * `Question`:
          * `author` - ForeignKey to `CustomUser`
          * `tags` - ManyToManyField to `Tag`
          * `journal` - ManyToManyField to `Journal`
          * `body`
          * `date`
          * `edited_date`
    * Daily Diary Card:
      * Possible Model and Fields:
        * ???
* Goals and Values Tracker:
  * `values`:
    * Goals (e.g. obtain teaching position, create non-profit to help disadvantaged, etc.)
      * `SMART` Goals
      * Possible Model and Fields:
        * `Goal`:
          * `name`
          * `description`
          * `units`
          * `frequency`
          * `tags` - ManyToManyField to `Tag`
          * `user` - ForeignKey to `CustomUser`
          * `activities` - ManyToManyField to `Activity`
          * `start_date`
          * `target_date`
    * Values
      * e.g. care for others, teach others, care for self, enrich my life, enrich others' lives, etc.
      * Possible Model and Fields:
        * `Value`:
          * `name`
          * `description`
          * `tags` - ManyToManyField to `Tag`
          * `user` - ForeignKey to `CustomUser`
          * `goals` - ManyToManyField to `Goal`
    * Activities
      * e.g. apply for position, have fun, play, pet the cat, exercise, sleep, meditation, etc.
      * Possible Model and Fields:
        * `Activity` (plural: `Activities`)):
          * `name`
          * `description`
          * `start_time`
          * `end_time`
          * `duration`
          * `units` - ManyToManyField to `Unit`, or maybe `Unit` is a `ChoiceField`?
          * `tags` - ManyToManyField to `Tag`
          * `user` - ForeignKey to `CustomUser`
          * `goals` - ManyToManyField to `Goal`

## Additional Features (required or otherwise)

### View (Role) to Set `is_moderator` `True` or `False`

* Sets Moderator Role (or, maybe, group?)

### View (Role) to Set `registration_accepted` `True` or `False`

* Performs Moderator Role
* This role has `CustomUser` attributes `is_moderator` set to `True`.
* This can be called Moderator Role (or, maybe, group?)
* Dashboard

## Interesting and/or New Concepts and Commands

* Create database from command line:
  * `heroku addons:create heroku-postgresql:mini`

* `linebreaks` filter:
  * <https://docs.djangoproject.com/en/4.1/ref/templates/builtins/#linebreaks>
  * [`rodbt/templates/rodbt/journal_list.html`](./rodbt/templates/rodbt/journal_list.html):
    * `{{ journal.body | linebreaks }}`
  * Django Admin Documentation:

    ![linebreaks](https://user-images.githubusercontent.com/47562501/216554120-956f3226-10d5-4c42-b79c-260f089dce98.png)
* `truncatewords` filter:
  * <https://docs.djangoproject.com/en/4.1/ref/templates/builtins/#truncatewords>
  * [`rodbt/templates/rodbt/journal_list.html`](./rodbt/templates/rodbt/journal_list.html):
    * `{{ journal.title | truncatewords:5 }}`
  * Django Admin Documentation:

    ![truncatewords](https://user-images.githubusercontent.com/47562501/216563307-7d7e38da-da5e-4363-95d0-2360874f04f5.png)

* `Client()`:
  * [The test client - docs.djangoproject.com](https://docs.djangoproject.com/en/4.1/topics/testing/tools/#the-test-client)
  * [`django.test.Client` - docs.djangoproject.com](https://docs.djangoproject.com/en/4.1/topics/testing/tools/#django.test.Client)

  ```python
          c = Client()
          logged_in = c.login(
              username=A_TEST_USERNAME,
              password=A_TEST_PASSWORD,
          )
          print('logged_in: ', logged_in)
  ```
