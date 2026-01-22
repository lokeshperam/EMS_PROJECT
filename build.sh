#!/bin/bash
set -o errexit

pip install -r requirements.txt

cd ems_project
python manage.py collectstatic --no-input
python manage.py migrate
python manage.py create_default_user
