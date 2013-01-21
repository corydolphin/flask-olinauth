# -*- coding: utf-8 -*-
"""
Flask-Login example
===================
This is a small application that provides a trivial demonstration of
Flask-Login, including remember me functionality.

:copyright: (C) 2011 by Matthew Frazier.
:license:   MIT/X11, see LICENSE for more details.
"""
from flask import Flask
from flask.exti.olinauth import OlinAuth, auth_required, current_user
app = Flask(__name__)

SECRET_KEY = "yeah, not actually a secret"
DEBUG = True

app.config.from_object(__name__)

oa = OlinAuth(app)
#initial OlinAuth, with callback host of localhost:5000
oa.init_app(app, 'localhost:5000')


@app.route("/")
def index():
    if current_user:
        responseString = "Awesome index, guess what? %s is logged in. Sweet, right?" % current_user['id']
    else:
        responseString = "It is kind of lonely here... No users are logged in"
    return responseString


@app.route("/secret")
@auth_required
def secret():
    return "I wouldn't normally show you this, but since %s is logged in, here is the secret: 42" % current_user['id']


if __name__ == "__main__":
    app.run(debug=True)
