# -*- coding: utf-8 -*-
"""
Flask-OlinAuth example
===================
This is a small application that provides an implementation of Olin's
authentication protocol.

:copyright: (C) 2013 by Cory Dolphin.
:license:   MIT/X11, see LICENSE for more details.
"""
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
def index():  # this view is public, does not require authentication
    if current_user:  # if a user is logged in and authenticated
        responseString = "Awesome index, guess what? %s is logged in. Sweet,\
         right? <a href=%s> Logout</a>" % (current_user['id'], url_for('__logout'))
    else:
        responseString = "<html>It is kind of lonely here... No users are logged in. <a href=%s>Checkout my secret</a> </html>" % url_for('secret')
    return responseString


@app.route("/secret")
@auth_required
def secret():  # this view requires authentication, and will redirect if not.
    return "I wouldn't normally show you this, but since %s is logged in, here is the secret: 42" % current_user['id']


if __name__ == "__main__":
    app.run(debug=True)
