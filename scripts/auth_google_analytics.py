#!/usr/bin/python
"""
This script is for setting up OAuth credentials for Google Analytics.

To use:
Visit https://code.google.com/apis/console/ and select "API Access".
If a client ID for an "installed application" hasn't been created, add one.
Click "Download JSON" in the box containing information about that client ID.
Run this script:
  'python auth_google_analytics.py --secrets client_secrets.json'
(If you are running this on a host with no web browser, pass
--noauth_local_webserver as well.)
Paste the printed credentials into the Django settings file.
"""

import pprint
import sys

import gflags
from oauth2client.client import flow_from_clientsecrets, Storage, EXPIRY_FORMAT
from oauth2client.tools import run

gflags.DEFINE_string(
    'secrets', None, 'Client secret JSON filename', short_name='f')

gflags.FLAGS(sys.argv)

CLIENT_SECRETS = gflags.FLAGS.secrets

MISSING_CLIENT_SECRETS_MESSAGE = ("%s is missing or doesn't contain secrets "
                                  "for a web application" % CLIENT_SECRETS)

FLOW = flow_from_clientsecrets(
    CLIENT_SECRETS,
    scope='https://www.googleapis.com/auth/analytics.readonly',
    message=MISSING_CLIENT_SECRETS_MESSAGE)


s = Storage()
s.put = lambda *a, **kw: None
credentials = run(FLOW, s)

bits = dict([(str(name), str(getattr(credentials, name))) for name in
             ('access_token', 'client_id', 'client_secret',
              'refresh_token', 'token_uri',
              'user_agent')])
bits['token_expiry'] = credentials.token_expiry.strftime(EXPIRY_FORMAT)
print 'GOOGLE_ANALYTICS_CREDENTIALS = ',
pprint.pprint(bits)
