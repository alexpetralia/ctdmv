#!bin/bash

psql -U postgres -p 5433 -c "drop database tmp2;"
psql -U postgres -p 5433 -c "create database tmp2;"
pg_restore --verbose --clean --no-acl --no-owner -h localhost -p 5433 -U postgres -d tmp ~/Desktop/latest.dump; # Heroku backup
# cd web;
# npm run build;
# cd ..;
# python manage.py collectstatic --noinput
