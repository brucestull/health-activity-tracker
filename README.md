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

### Moderator View

* View for `user`s where `user.is_moderator` is `True`:
  * Moderator Dashboard.
  * Moderator can administrate users.
  * Moderator can delete any user.
  * Moderator can set `user.registration_accepted` for any user.

## Interesting and/or New Concepts and Commands

* Create database from command line:
  * `heroku addons:create heroku-postgresql:mini`
