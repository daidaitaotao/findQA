======
findQA
======

findQA is a Django command that enables users to search for testers based on
the country(s) and device(s) the user specifies.  The command output includes
the following fields formatted as CSV: the tester's first name, last name,
country code, and experience (which is how many bugs the tester has spotted
based on the searching criteria).

This is version 0.1.1 of this app.

Quick start
-----------

1. Check the requirements for this app in requirement.txt in 'findQA/requirements.txt'
   `pip freeze > requirements.txt`
   If you wish to install all required libraries, simply run
   `pip install -r requirements.txt`

2. In matchQA/matchQA/settings.py, make sure the app has been added to INSTALLED_APPS, such as
    INSTALLED_APPS = [
    'findQA.apps.FindQAConfig',
    ...]

3. Run `python manage.py migrate` to create the findQA tables in the database.

4. Run `python manage.py shell < load_data.py` to insert all data from matchQA/matchQA/csv_data
   into database.

5. Run `python manage.py find_testers -h` to view the command's help.
   Examples:
    * If you wish to search by all countries and device
    `python manage.py find_testers`

    * If you wish to search by country(s)
    `python manage.py find_testers -c US,JP`

    * If you wish to search by device(s), please make sure enclose each device's name in single quotes.
    `python manage.py find_testers -d 'iPhone 4','iPhone 4S'`

    * If you wish to search by countries and device(s).
    `python manage.py find_testers -c US,JP -d 'iPhone 4','iPhone 4S'`

5b. [OPTIONAL] Run `python manage.py test` to run unit tests to against the code.