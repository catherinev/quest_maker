## Getting started as a developer

Please report and problems or confusion you have in following these instructions. At the moment they are configured for an Ubuntu environment and have not been thoroughly tested.

1. Ensure you have python 2.7 and git installed on your system. Also install pip.

2. Clone QuestMaker to your machine:
    ```
    git clone https://github.com/catherinev/quest_maker.git
    ```

3. Install and configure virtualenvwrapper.  This will enable you to create a virtual environment that is the same as ours.

    a) First install virtualenvwrapper:
    ``pip install virtualenvwrapper``

    b) Make a folder for your virtual environments to live in, e.g.:
    ``mkdir ~/.virtualenvs``

    c) Add these lines to end of .bashrc (or your OS equivalent):
    ```
    export WORKON_HOME=~/.virtualenvs  # or the folder you just created
    export PROJECT_HOME=~/code/projects/  # or wherever you cloned the project
    source /usr/local/bin/virtualenvwrapper.sh  # or your path to virtualenvwrapper.sh
    ```
   d) Run .bashrc:
    ``source .bashrc``

4. Now create a virtualenv. You can call it questmaker:
    ``mkvirtualenv questmaker``

   You should always be inside your virtualenv when working on the project. You can enter/exit the virtualenv with:
   ```
       workon questmaker
       deactivate
   ```

5. Install dependencies into the virtualenv.
   For what follows, make sure you are inside the virtualenv.
   Navigate to the root project directory, which contains requirements.txt.
   Hopefully, this will install them in one fell swoop:
    ``pip install -r requirements.txt``

  If you run into hangups, install the offending packages another way (see their individual install instructions). We haven't had any problems pip installing the current packages on Ubuntu or Mac, but pip doesn't always work as smoothly on Windows.
  In any case, make sure to get the versions specified in requirements.txt.

6. Create the database. From the root project directory (which contains the script manage.py, run:
    ``python manage.py migrate``

This will initialize the database and run any migrations, bringing you up-to-date. (We are using SQLite3, hence the minimal setup).

**Congratulations! You are done with setup!**

## Next Steps
You should now be able to launch the app locally by navigating to the root project directory (which contains manage.py) and executing:
  ```
  python manage.py runserver --settings=quest_maker.settings.settings_dev
  ```

**Visit localhost:8000 and you should see the site!**

Furthermore, Django comes with a built-in admin panel which is very useful in both development and production. Check it out at localhost:8000/admin. To log in, you can create a superuser for yourself at any time by running:
  ```
  python manage.py createsuperuser
  ```
You may as well choose a username "admin" and password "password". It's just for your use locally during development.

**Ready to contribute?** See the [README](README.md) for more information!
