Rsscraper
=========

Test for Sendcloud

.. image:: https://img.shields.io/badge/built%20with-Cookiecutter%20Django-ff69b4.svg
     :target: https://github.com/pydanny/cookiecutter-django/
     :alt: Built with Cookiecutter Django
.. image:: https://img.shields.io/badge/code%20style-black-000000.svg
     :target: https://github.com/ambv/black
     :alt: Black code style


:License: MIT


Settings
--------

Moved to settings_.

.. _settings: http://cookiecutter-django.readthedocs.io/en/latest/settings.html

Basic Commands
--------------

Setting Up Your Users
^^^^^^^^^^^^^^^^^^^^^

* To create a **normal user account**, just go to Sign Up and fill out the form. Once you submit it, you'll see a "Verify Your E-mail Address" page. Go to your console to see a simulated email verification message. Copy the link into your browser. Now the user's email should be verified and ready to go.

* To create an **superuser account**, use this command::

    $ python manage.py createsuperuser

For convenience, you can keep your normal user logged in on Chrome and your superuser logged in on Firefox (or similar), so that you can see how the site behaves for both kinds of users.

Running dev server locally
^^^^^^^^^^^^^^^^^^^^^^^^^^

.. code-block:: bash
    pipenv shell "./manage.py runserver_plus 127.0.0.1:9000 --traceback"

 (change 127.0.0.1:9000 for your preferred listening host and address)

Type checks
^^^^^^^^^^^

Running type checks with mypy:

::

  $ mypy rsscraper

Test coverage
^^^^^^^^^^^^^

To run the tests, check your test coverage, and generate an HTML coverage report::

    $ coverage run -m pytest
    $ coverage html
    $ open htmlcov/index.html

Running tests with py.test
~~~~~~~~~~~~~~~~~~~~~~~~~~

::

  $ pytest


Celery
^^^^^^

This app comes with Celery.

To run a celery worker:

.. code-block:: bash

    cd rsscraper
    pipenv run celery worker -A config.celery_app -l INFO

Please note: For Celery's import magic to work, it is important *where* the celery commands are run. If you are in the same folder with *manage.py*, you should be right.


To run periodic tasks you should run celerybeat

.. code-block:: bash

    pipenv run celery beat -A config.celery_app -l INFO


Also, to configure periodic tasks you must go to `periodic task` section in admin ie. `http://localhost:9000/admin/django_celery_beat/` (change localhost:9000 for your host and port)





Deployment
----------

The following details how to deploy this application.



Docker
^^^^^^

In order to deploy using Docker compose you must build the image

(<env> can be either `local` or `production`)

.. code-block:: bash

    docker-compose -f <env>.yml build

Then run the image

.. code-block:: bash

    docker-compose -f <env>.yml up

Note: Local environment doesn't need any further configuration for deployment

For more information about running app with docker: https://cookiecutter-django.readthedocs.io/en/latest/deployment-with-docker.html
