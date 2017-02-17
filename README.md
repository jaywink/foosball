# Foosball

[![Build Status](https://travis-ci.org/andersinno/foosball.svg?branch=master)](https://travis-ci.org/andersinno/foosball)
[![Stories in Ready](https://badge.waffle.io/andersinno/foosball.png?label=ready&title=Ready)](https://waffle.io/andersinno/foosball)

![logo](/foosball/static/images/logo.png?raw=true "Project logo")

Office foosball results!

Logo made with the awesome [Hipster logo generator](https://www.hipsterlogogenerator.com/).

LICENSE: MIT

## Settings

Moved to [settings](http://cookiecutter-django.readthedocs.org/en/latest/settings.html).

## Basic Commands

### Setting Up Your Development environment

First create a virtualenv using Python 3.5 or 3.6.
 
Install OS dependencies

    sudo ./install_os_dependencies.sh
    
Ensure pip is up to date

    pip install -U pip
    
Install local requirements

    pip install -r requirements/local.txt
    
Compile all required static resources

    npm run build

You can also use `pip-tools` for managing and installing requirements. `pip-sync requirements/local.txt`

### Setting Up Your Users

To create a **normal user account**, just go to Sign Up and fill out the form. Once you submit it, you'll see a "Verify Your E-mail Address" page. Go to your console to see a simulated email verification message. Copy the link into your browser. Now the user's email should be verified and ready to go.

To create an **superuser account**, use this command::

    python manage.py createsuperuser

For convenience, you can keep your normal user logged in on Chrome and your superuser logged in on Firefox (or similar), so that you can see how the site behaves for both kinds of users.

### Test coverage

To run the tests, check your test coverage, and generate an HTML coverage report::

    coverage run manage.py test
    coverage html
    open htmlcov/index.html

#### Running tests with py.test

    py.test

### Automatic Less CSS compilation

    npm run watch
    
### Updating requirements

    pip-compile -U requirements/local.in
    pip-compile -U requirements/production.in

## Deployment

Write instructions.
