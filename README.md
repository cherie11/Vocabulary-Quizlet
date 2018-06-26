# Vocabulary-Quizlet
    Web app for vocabulary + quiz + customized word list

## Dependency
-----
  * Django==2.0
  * Python 3.6

## Run
------
```bash
    pip3 install -r requirements.txt
    python3 manage.py makemigrations --empty account
    python3 manage.py makemigrations --empty card
    python3 manage.py migrate account
    python3 manage.py migrate card
    python3 initdb.py
    python3 manage.py runserver
```
