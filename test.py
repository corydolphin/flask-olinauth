import unittest
import example
import requests
import os


class FlaskOlinAuthTest(unittest.TestCase):
    def setUp(self):
        self.app = example.app.test_client()
        self.sessionid = get_sessionid()
        assert self.sessionid

    def tearDown(self):
        pass

    def test_public(self):
        rv = self.app.get('/')
        assert rv.data.find("lonely") > 0

    def test_private_unauth(self):
        rv = self.app.get('/secret')
        assert rv.status_code == 302
        assert rv.headers.get('Location').find("olinapps.com/external")

    def test_authenticate_sessionid(self):
        assert self.sessionid
        rv = self.app.get('/secret?sessionid=%s' % self.sessionid)
        assert rv.status_code == 200
        assert rv.data.find('42')

    def test_fail_sessionid(self):
        rv = self.app.get('/secret?sessionid=%s' % 1)  # invalid session
        assert rv.status_code == 302


def get_sessionid():
    payload = {"username": os.environ.get("OLIN-USERNAME", ""),
     "password": os.environ.get("OLIN-PASSWORD", "")}
    r = requests.post("https://olinapps.herokuapp.com/api/exchangelogin",
    data=payload)
    return r.json().get('sessionid', None)

if __name__ == '__main__':
    unittest.main()
