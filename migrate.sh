#!/bin/bash
export DB_URI=postgresql://postgres:postgres@localhost/cnab

docker-compose -f docker-compose.yml up --build -d db;
python3 -m pip install virtualenv
virtualenv env
source env/bin/activate

cd api

pip install -r requirements/requirements.txt

python cnab/manage.py makemigrations
python cnab/manage.py migrate

cd ..

psql $DB_URI -f database_scripts.sql