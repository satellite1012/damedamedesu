
# Sogi


## Steps for development:

Install python and Django on your machine. Also have virtualenv and PostgreSQL set-up (see below if you need help).
Make sure there is a PostgreSQL user 'test' with password 'test' (no quotes).

If you made changes to the models:
`python manage.py makemigrations`
or `python manage.py makemigrations portal` if the above doesn't work.

Set up the database with:
`python manage.py migrate`

Run the following command in a terminal to start app on localhost:
`python manage.py runserver`

---

## Steps for setting up PostgreSQL on Windows:

- download and install PostgreSQL at http://www.postgresql.org/download/windows/
- add PostgreSQL to your path (usually something like C:\Program Files\PostgreSQL\bin)
- if you have permissions problems, give yourself access by opening pgAdmin
    - File -> Open pg_hba.conf -> C:\Program Files\PostgreSQL\9.4\data\ -> Open
    - double click the first two lines and change Method from 'md5' to 'trust'
    - save your changes
- to create a user named test:
    - run `psql -U postgres -c "CREATE ROLE test LOGIN NOSUPERUSER INHERIT CREATEDB CREATEROLE;"`
- to change a user's password:
    - run `psql -U postgres -c "ALTER USER test WITH PASSWORD 'test';`
- to create a new database named sogidb:
    - run `createdb -U postgres sogidb`
    
---

## Running on Heroku

- check that you've set DJANGO_SETTINGS_MODULE `heroku config:set DJANGO_SETTINGS_MODULE=sogi.settings`
- set up the dbs like you would locally
    - reset the database in heroku
    - `heroku run python manage.py migrate`
