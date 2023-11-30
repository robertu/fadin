#!/bin/bash

set -a
. ./.env
cd fadin

echo -n "Waiting for PostgreSQL to start on $DB_HOST:$DB_PORT "

while ! nc -z $DB_HOST $DB_PORT; do
  sleep 0.2
  echo -n "."
done
echo " done."

poetry run ./manage.py flush --no-input
poetry run ./manage.py migrate
if [ "$@" == "pytest" ] ; then cd /app ; fi
poetry run $@
