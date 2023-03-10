# Add Remote to Cloned Repository

## Application URL

* <https://flynnt-knapp-health-tracker.herokuapp.com/>

## Remote Heroku Repository URL

* <https://git.heroku.com/flynnt-knapp-health-tracker.git>

## Commands

1. Check remotes:

    ```bash
    (health-activity-tracker) PS C:\Users\FlynntKnapp\Programming\health-activity-tracker> git remote -v
    origin  https://github.com/brucestull/health-activity-tracker.git (fetch)
    origin  https://github.com/brucestull/health-activity-tracker.git (push)
    (health-activity-tracker) PS C:\Users\FlynntKnapp\Programming\health-activity-tracker>
    ```

1. Add `heroku` as a remote repository:

    ```bash
    git remote add heroku https://git.heroku.com/flynnt-knapp-health-tracker.git
    ```

1. Check remotes:

    ```bash
    (health-activity-tracker) PS C:\Users\FlynntKnapp\Programming\health-activity-tracker> git remote -v
    heroku  https://git.heroku.com/flynnt-knapp-health-tracker.git (fetch)
    heroku  https://git.heroku.com/flynnt-knapp-health-tracker.git (push)
    origin  https://github.com/brucestull/health-activity-tracker.git (fetch)
    origin  https://github.com/brucestull/health-activity-tracker.git (push)
    (health-activity-tracker) PS C:\Users\FlynntKnapp\Programming\health-activity-tracker>
    ```

1. Push changes to remote repository:

    ```bash
    git push heroku main
    ```
