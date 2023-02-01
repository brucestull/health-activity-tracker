# Health Activity Tracker

## Heroku Links

* Production Deployment:
  * <https://flynnt-knapp-health-tracker.herokuapp.com/>

## Application Structure

* RO-DBT
  * Self-Enquiry Journal
  * Daily Diary Card
* Goals and Values Tracker
  * Goals (e.g. obtain teaching position, create non-profit to help disadvantaged, etc.)
  * Values (e.g. care for others, teach others, etc.)
* Activity Tracker
  * Activity (e.g. apply for position, have fun, play, pet the cat, exercise, sleep, meditation, etc.)

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
