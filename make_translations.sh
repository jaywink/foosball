#!/bin/bash
./manage.py makemessages -l fi --ignore "bower_components/*" --ignore "node_modules/*" -e jinja,html,py
