# Flask-OlinAuth

Flask-OlinAuth implements OlinApps auth. It automatically provides a `/login` and `/logout` route
to the application, handling the process of actually authenticating a user with olinapps. 
Currently the plugin is inflexible and would not work if you override one of the routes. It also does not
use cryptographically secure cookies, which it 'should'.

At a high level, Flask-OlinAuth provides two useful pieces for your application,
both of which are demonstrated in `example.py`.

## `@auth_required`
A simple function decorator which ensures that a user is logged in before a
view is shown. The user is redirected to the login portal, with correct
arguments, if not.

## `current_user`
A nice local proxy for all of your views to get the current user, formatted as
a dictionary.

Flask-OlinAuth is very heavily inspired by Flask-Login, with structure, and
functionality adopted, and much knowledge gained.

## Installation

Install the extension with one of the following commands:

    $ easy_install flask-olinauth

or alternatively if you have pip installed (which you should):

    $ pip install flask-olinauth
