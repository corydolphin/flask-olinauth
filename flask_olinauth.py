from functools import wraps
from flask import current_app, request, session, redirect
from werkzeug.local import LocalProxy
import requests
import urllib

__version__ = "1.0"
OLINAPPS_STR = 'http://olinapps.com/external?%s'


class OlinAuth(object):
    def __init__(self, app=None, host_name=None):
        if app is not None and host_name is not None:
            self.init_app(app, host_name)
        else:
            self.app = None

    def init_app(self, app, host_name):
        app.olin_auth = self
        self.host_name = host_name  # used to generate callback url
        app.add_url_rule('/olinauthlogin', view_func=OlinAuth.__login, methods=['GET', 'POST'])
        app.add_url_rule('/olinauthlogout', view_func=OlinAuth.__logout, methods=['GET', 'POST'])

    @staticmethod
    def __login():
        """Handles the POST from Olin Auth's callback, and redirects to the original
        destination specified in the :destination: querystring.
        """
        if request.method == 'POST':
            # External login.
            if load_session():
                return redirect(request.args.get("destination") or "/")
            else:
                session.pop('sessionid', None)
        return "Please authenticate with Olin Apps to view."

    @staticmethod
    def __logout():
        """ Provides a logout view to the application, removing the user from the
        session and removing the session id. TODO: tell olinapps to deauth user?
        """
        session.pop('sessionid', None)
        session.pop('user', None)
        return redirect('/')


def load_session():
    """Returns an OlinAuth user dict and stores the sessionid and user in
    this application's session.

    TODO: support caching? When the sessionid is specified as a url argument,
    thie application will make a new web request each time, which is a waste.
    Perhaps we can check if there exists a cache on the app and use it.
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


def get_session_user():
    """ Returns the current session's user, or the user specified by the
    sessionid url parameter.
    """
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


def logout_user():
    '''Logs out the current_user, removing their information from the session. TODO: notify olinapps?'''
    session.pop('sessionid', None)
    session.pop('user', None)


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
            # callback to pass to olinapps, urlencode original url to allow
            # a user to be redirected to the original view they were accessing
            cbstring = "http://%s/olinauthlogin?destination=%s" % (
                current_app.olin_auth.host_name,
                request.url
                )
            return redirect(OLINAPPS_STR % urllib.urlencode({
                "callback": cbstring
                })
            )

    return decorated_view


current_user = LocalProxy(lambda: get_session_user())
