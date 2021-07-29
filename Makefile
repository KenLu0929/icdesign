port = 8000 # defaults

install:
	pip install -r requirements.txt
run:
	python manage.py runserver $(port)
migration:
	python manage.py makemigrations
migrate:
	python manage.py migrate
superuser:
	python manage.py createsuperuser
test:
	python manage.py test
run_all:
	python manage.py makemigrations
	python manage.py migrate
	python manage.py runserver $(port)