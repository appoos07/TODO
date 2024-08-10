# Todo Manager

A simple Django application to manage projects and their associated tasks (todos). This application allows users to create projects, add tasks, and export project details to a GitHub Gist.

1.Prerequisites

- Python 3.12
- Django
- GitHub account (for exporting gists)

2.Set up the database:

python manage.py makemigrations
python manage.py migrate

3.Create Superuser:

python manage.py createsuperuser

4.Run tests:

python manage.py test

5.Run the development server:

python manage.py runserver

6.Usage 

Access the application at http://127.0.0.1:8000/.
Log in with your superuser credentials.
Create and manage projects and tasks.
Export a project's tasks to a GitHub Gist.
