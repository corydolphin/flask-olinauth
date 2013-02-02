# Flask-OlinAuth

Flask-OlinAuth implements OlinApps auth. It automatically provides a `/olinauthlogin` and `/olinauthlogout` route
to the application, handling the process of actually authenticating a user with olinapps.

At a high level, Flask-OlinAuth provides two useful pieces for your application,
both of which are demonstrated in `example.py`.

## `@auth_required`
A simple function decorator which ensures that a user is logged in before a
view is shown. The user is redirected to the login portal, with correct
arguments, if not.

## `current_user`
A nice local proxy for all of your views to get the current user, formatted as
a dictionary.

## `logout_user`
Will log out the currently authenticated user, allowing you to simply
create your own logout view.

Flask-OlinAuth is very heavily inspired by Flask-Login, with structure, and
functionality adopted, and much knowledge gained.

## Installation

Install the extension with one of the following commands:

    $ easy_install flask-olinauth

or alternatively if you have pip installed (which you should):

    $ pip install flask-olinauth

## Example Usage
```
from flask import Flask, url_for
from flask.ext.olinauth import OlinAuth, auth_required, current_user
app = Flask(__name__)

SECRET_KEY = "yeah, not actually a secret"
DEBUG = True

app.config.from_object(__name__)

oa = OlinAuth(app, 'localhost:5000')
#initial OlinAuth, with callback host of localhost:5000, for local server
oa.init_app(app, 'localhost:5000')


@app.route("/")
def index():
    if current_user:
        responseString = "Awesome index, guess what? %s is logged in. Sweet, right?" % current_user['id']
    else:
        responseString = "<html>It is kind of lonely here... No users are logged in. <a href=%s>Checkout my secret</a> </html>" % url_for('secret')
    return responseString


@app.route("/secret")
@auth_required
def secret():
    return "I wouldn't normally show you this, but since %s is logged in, here is the secret: 42" % current_user['id']


if __name__ == "__main__":
    app.run(debug=True)

```