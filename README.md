# Foosball

![logo](/foosball/static/images/logo.png?raw=true "Project logo")


Office foosball results! Made with Python 3.5.

LICENSE: MIT

## Settings

Moved to [settings](http://cookiecutter-django.readthedocs.org/en/latest/settings.html).

## Basic Commands

### Setting Up Your Development environment

* Create a virtualenv using Python 3.5.x. 
* Compile all required static resources
  `npm run build`


### Setting Up Your Users

To create a **normal user account**, just go to Sign Up and fill out the form. Once you submit it, you'll see a "Verify Your E-mail Address" page. Go to your console to see a simulated email verification message. Copy the link into your browser. Now the user's email should be verified and ready to go.

To create an **superuser account**, use this command::

    $ python manage.py createsuperuser

For convenience, you can keep your normal user logged in on Chrome and your superuser logged in on Firefox (or similar), so that you can see how the site behaves for both kinds of users.

### Test coverage

To run the tests, check your test coverage, and generate an HTML coverage report::

    $ coverage run manage.py test
    $ coverage html
    $ open htmlcov/index.html

#### Running tests with py.test

    $ py.test


### Live reloading and Sass CSS compilation

Moved to [Live reloading and SASS compilation](http://cookiecutter-django.readthedocs.org/en/latest/live-reloading-and-sass-compilation.html).


It's time to write the code!!!

## Deployment

Write instructions.
