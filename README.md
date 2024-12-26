# ase_charging_station_part_2

### TODO / Next Tasks:
#### 1. Implement Create Profile
- We also need a place to store new user data - we can do it either temporarily in a dictionary or create a "database" using a csv or json file
#### 2. Create Map on Mainpage
- Scale map so that Berlin is shown in the centre
#### 3. Create Charging Station "Database"
- add the 2 significant csv and excel files from the first project part to a "data" folder
- add a "tools" folder and create a createChargingStationDatabase.py file (or similar in naming)
- Use the new script to read the tables of the first project part
- create a new table for charging stations from it containing stationID | stationOperator | stationName | PLZ |Bundesland | Latitude | Longitude | KW | geometry | ratingID

- ratingID will remain empty for now, the other things should be "stripped" from the original tables of the
  first project part so that we have for each charging station an individual ID and name together with its
  location (latitude and longitude) and in which zip code it stands
- the new tables shall be stored in another new csv file (please name it something like "ChargingStationData.csv" or so)

### Future Tasks:
- Once we have a map and the new csv file, we can add markers on the map using the latitude and longitude of the charging stations
    - Once we have markers, we need a function that handles what happens if they are clicked (maybe some popup window showing info about the charging station, or we show the info below the map if you don't like popups - feel free to design whatever you like)
    - The Info page shall show the stored info about the clicked charging station (ID, Name, latitude, longitude, plz and a "rating average") as well as the possibility for users to rate the station
    - If someone wants to rate a station (by text or stars) it shall be checked if they are logged in on a profile and if not, they need to login or create one
    - If the login criteria is fulfilled, the user shall be able to give a rating of the station in stars (and if they want additionally text)
    - The rating must be stored somewhere (please do it just in the same way as we store our user data in task 1)
- Once we have a map and the new csv file, we are also able to fulfill usecase 1 "search for charging stations"
    - one would have to add a text-input field to allow the search for charging stations by postal codes
    - once a postal code is entered there, a list with charging stations shall be shown (as pop up or below the map)
    - if one clicks on the elements of the list (the charging stations by id and name etc.) the map shall zoom to the very charging station and show its individual info



### Hints how to use git:
#### Cloning a repository:
`git clone \<name of the repo\>`

#### Get the updates that happened on the repo
`git pull`

#### Adding stuff to git
`git add \<file-name\>`
`git add -u` add everything that was changed

#### Undo add
`git reset \<file-name\>` or
`git reset` reset everything you planned to add so far

#### Show adding / reset status
`git status`

#### Stage a version of your files
`git commit`
`git commit -m "text of the commit message"`
`git commit -m "text of the commit message" -m "more deeply description"`
`git commit --amend --no-edit` if you made a small mistake with you last commit and want to fix it
you can use `--amend` to change the last commit and add `--no-edit` if you want to keep the old commit
message

#### Pushing the commit online to github
`git push`
`git push --force` is needed if you overwrite something you already pushed

#### Creating your branch
`git branch \<branch_name\>`
Switch to the branch
`git checkout \<branch_name\>`

#### Getting updates of other group members
`git pull` to get updates of the branch you are currently working on
`git fetch --all --prune` to update everything

#### Putting your own branch on the newest version of another branch
`git rebase \<branch_name\>`
`git rebase main` you probably want to rebase on main...

#### In case of rebase/merge conflict
First: resolving the conflict in the editor and saving the file
`git add` of the file to stage the changes
`git rebase --continue`
`git merge --continue`
And then you have to type a new commit message.

#### Showing a list of all commits on your branch
`git log`