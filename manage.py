#!/usr/bin/env python
import os
import sys

import environ

if __name__ == "__main__":
    envfile = str(environ.Path(__file__) - 1 + '.env')
    if os.path.isfile(envfile):
        environ.Env.read_env(envfile)

    os.environ.setdefault("DJANGO_SETTINGS_MODULE", "config.settings.local")

    from django.core.management import execute_from_command_line

    execute_from_command_line(sys.argv)
