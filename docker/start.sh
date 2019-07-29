#!/bin/bash

set -e

./manage.py makemigrations --merge  --no-input --traceback
./manage.py migrate  --no-input --traceback

./manage.py runserver 0.0.0.0:8000
