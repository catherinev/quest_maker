## About this application
QuestMaker is a web application that integrates with FitBit and makes exercise more rewarding by enabling users to easily create and participate in quests with their friends. In its simplest form, a quest is a series of milestones that users reach as they cover more distance over time. For users with FitBits, daily progress is updated automatically; for those without, manual entry is easy.

The idea for this application comes from the [Walk to Rivendell Challenge](http://home.insightbb.com/~eowynchallenge/index.html), which provides a [series of waypoints](http://home.insightbb.com/~eowynchallenge/Tools/Bag_end/bag_end.html) for Frodo's walk across Middle Earth. Since its inception in 2003, many people have made the whimsical trek across Tolkien's Middle Earth by manually charting their mileage each day and sharing their progress with friends. QuestMaker personalizes and automates this process, allowing you to focus your energies on outwalking the rest of your ~~friends~~ ~~competitors~~ fellowship!


## Getting started
See [Getting Started](GettingStarted.md) for detailed info on how to set everything up on your machine.


## Running the test suite
TODO


## Git Workflow

### To work on the app:
See [Getting Started](GettingStarted.md) for initial setup. Once you are set up, follow the following procedure to contribute code.

#### A note on branch names:
* The production branch is ``master``.
* The development branch is ``develop``.
* Feature branches branch off from ``develop`` and are named ``feature-<description>``, e.g. feature-admin-editing.
* Hotfix branches are named ``hotfix-<description>``;  they may branch from develop or master and should be merged back into both.

Thus, if you are working on a **new feature**, follow this procedure:

First, pull down from develop (to make sure you're up-to-date) and create a new branch:
  ```
  git checkout develop
  git pull origin develop
  git checkout -b "your_branch_name"
  ```
Your branch name should be prefixed with feature-, e.g. feature-awesome-new-code.

NOTE: Any time you pull down from GitHub, there may be **new migrations** or **updated requirements**. New migrations need to be applied to your local database in order for it to function properly with the current Django models. New requirements must be installed. Thus, before continuing, it's a good idea to run:
  ```
    python manage.py migrate
    pip install -r requirements.txt
  ```

In other words, the app really has three components: the code, the database, and the dependencies. Pulling from GitHub changes the code but does not affect your database or your dependencies. Fortunately, the code contains (a) migration files that say how to update the database, and (b) requirements.txt which specifies current dependencies. These files are accessed by the two commands above. Certainly if you run into strange DB problems or dependency issues, make sure you have done this.

(**Conversely**, if you need to change the Django models, please bundle both the changes to models.py AND the corresponding migration files into the same commit, so that models and database structure always correspond within any commit. Similarly, if you need to update requirements, please make sure to update requirements.txt with ``pip freeze > requirements.txt`` and commit it along with the updated code.)


When you are done working:

1. Add and commit any local changes to your feature branch, e.g.:

  ```
  git add modifiedscript.py
  git commit -m "My awesome commit message in present tense!"
  ```

2. Merge develop into your feature branch:
  ```
  git checkout your_branch_name
  git pull origin develop
  ```
  (This will try to merge; fix conflicts if necessary)

3. Push up to GitHub:
  ```
  git push origin your_branch_name
  ```

4. On GitHub, submit a pull request.


## License information

This application is free to use under the terms of the [MIT License](LICENSE).
