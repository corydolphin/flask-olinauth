from functools import wraps
from flask import current_app, request, session, redirect
from werkzeug.local import LocalProxy
import requests

OLINAPPS_STR = 'http://olinapps.com/external?callback=http://%s/login'


class OlinAuth(object):
    def __init__(self, app=None, host_name=None):
        if app is not None:
            self.init_app(app, host_name)
        else:
            self.app = None

    def init_app(self, app, host_name):
        app.olin_auth = self
        self.host_name = host_name  # used to generate callback url

        @app.route('/login', methods=['GET', 'POST'])
        def _login():
            return login()

        @app.route('/logout', methods=['GET', 'POST'])
        def _logout():
            return logout()


def load_session():
    """Returns an OlinAuth user dict and stores the sessionid and user in
    this application's session
    """
    sessionid = request.form.get('sessionid') or request.args.get('sessionid')
    if not sessionid:
        return None
    r = requests.get('http://olinapps.com/api/me',
        params={"sessionid": sessionid})
    if r.status_code == 200 and r.json() and 'user' in r.json():
        session['sessionid'] = sessionid
        session['user'] = r.json()['user']
        return r.json()
    return None


def login():
    if request.method == 'POST':
        # External login.
        if load_session():
            return redirect('/')
        else:
            session.pop('sessionid', None)
    return "Please authenticate with Olin Apps to view."


def logout():
    session.pop('sessionid', None)
    session.pop('user', None)
    return redirect('/')


def get_session_user():
    session_user = session.get('user', None)
    if session_user:
        return session_user
    else:
        if load_session():
            return session.get('user', None)
    return None


def get_session_email():
    userinfo = get_session_user()
    if not userinfo:
        return None
    return str(userinfo['id']) + '@' + str(userinfo['domain'])


def auth_required(fn):
    """
    If you decorate a view with this, it will ensure that the current user is
    logged in and authenticated before calling the actual view.

        @app.route("/trees", methods=['GET'])
        @auth_required
        def get_trees():
            return "no trees"



    :param fn: The view function to decorate.
    """
    @wraps(fn)
    def decorated_view(*args, **kwargs):
        if current_user:
            return fn(*args, **kwargs)
        else:   # TODO: support SSL?
            return redirect(OLINAPPS_STR % current_app.olin_auth.host_name)

    return decorated_view


current_user = LocalProxy(lambda: get_session_user())
