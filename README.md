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
          * `title`
          * `body`
          * `date`
          * `tags` - ManyToManyField to `Tag`
          * `edited_date`
        * `Question`:
          * `author` - ForeignKey to `CustomUser`
          * `body`
          * `date`
          * `tags` - ManyToManyField to `Tag`
          * `edited_date`
          * `journal` - ForeignKey to `Journal`
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
          * `start_date`
          * `target_date`
          * `tags` - ManyToManyField to `Tag`
          * `user` - ForeignKey to `CustomUser`
          * `activities` - ManyToManyField to `Activity`
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
