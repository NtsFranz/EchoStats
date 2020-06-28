## How to use the IgniteBot for stats when casting

![IgniteBot main window](img/main_window_blank.png)

1. Download and install the desktop program with the installer.
   - Updates can be downloaded when they are available from within the app
![App update](img/update.png)
2. Enter the access code
   ![Access Code entry](img/access_code.png)
   - Either use the code for the season (provided separately), or use a test code
   - To change the code later, click the code in the bottom left of the program
3. The OBS browser source for the end-of-round stats should be https://ignitevr-echostats.web.app/most_recent_match?client_name=[OCULUS_USERNAME] at 1920x1080
   - Append `&series_name=[SERIES_NAME]` to the url (https://ignitevr-echostats.web.app/most_recent_match?client_name=[OCULUS_USERNAME]&series_name=vrml_season_2)
      - valid codes are `vrml_test` and `vrml_season_2`. If no series name is specified, it defaults to `vrml_season_2`
4. The most_recent_match page will aggregate the stats from all rounds with the same `Stats ID`. This id can be changed either by restarting the IgniteBot or by clicking the `Split Stats` button. This should be done between games (not rounds) when the stats should be reset.
5. To preview or modify the stats shown on the overlay, go to https://ignitevr-echostats.web.app/group_recent_matches?client_name=[OCULUS_USERNAME]
   - The series name can also be specified here appending `&series_name=[SERIES_NAME]` to the url

### Using the round grouping website
 - The preview at the top shows what the current overlay would look like.
 - The green highlighted matches are the most recent group - stats are shown from these
 - To add another split, drag a black bar from the top.
 - To remove a split, drag it to the top or next to another black bar
 - While stats update as a round progresses, some updates still require a refresh, so refresh to be sure of what it will look like.