# IC Design
## Tech Stack
```
python 3
Django 3.2.5
HTML5
Javascript
```

## Install package
> pip install -r requirements.txt

## Run project on port:8000
> python manage.py makemigrations
> python manage.py migrate
> python manage.py runserver 8000

### using makefile for running application
> make install (for install all python package)
> make run_all (run projects with migrations stage)
> make run port=<no_port> (only run project, default of port=8000)

## Project Structure
path: `pages/templates/pages`
> folder for all html pages

path: `pages/templates/static`
> folder for all static file (css, jquery, image, etc.)

path: `pages/views.py`
> file for business logic

path: `pages/models.py`
> file for sql logic (query)