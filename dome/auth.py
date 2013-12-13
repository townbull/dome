#!/usr/bin/python
#
# Copyright (C) 2012 Google Inc.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#      http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

__author__ = 'afshar@google.com (Ali Afshar)'


# Add the library location to the path
import sys
sys.path.insert(0, 'lib')

import os
import httplib2
import sessions
from google.appengine.ext import webapp
from google.appengine.ext.webapp.util import run_wsgi_app
from google.appengine.ext import db
from google.appengine.ext.webapp import template
from apiclient.discovery import build
from apiclient.http import MediaUpload
from oauth2client.client import flow_from_clientsecrets
from oauth2client.client import FlowExchangeError
from oauth2client.client import AccessTokenRefreshError
from oauth2client.appengine import CredentialsProperty
from oauth2client.appengine import StorageByKeyName
from oauth2client.appengine import simplejson as json


class DriveState(object):
  """Store state provided by Drive."""

  def __init__(self, state):
    """Create a new instance of drive state.

    Parse and load the JSON state parameter.

    Args:
      state: State query parameter as a string.
    """
    if state:
      state_data = json.loads(state)
      self.action = state_data['action']
      self.ids = map(str, state_data.get('ids', []))
    else:
      self.action = 'create'
      self.ids = []

  @classmethod
  def FromRequest(cls, request):
    """Create a Drive State instance from an HTTP request.

    Args:
      cls: Type this class method is called against.
      request: HTTP request.
    """
    return DriveState(request.get('state'))


class BaseDriveHandler(webapp.RequestHandler):
  """Base request handler for drive applications.

  Adds Authorization support for Drive.
  """

  def CreateOAuthFlow(self):
    """Create OAuth2.0 flow controller

    This controller can be used to perform all parts of the OAuth 2.0 dance
    including exchanging an Authorization code.

    Args:
      request: HTTP request to create OAuth2.0 flow for
    Returns:
      OAuth2.0 Flow instance suitable for performing OAuth2.0.
    """
    flow = flow_from_clientsecrets('client_secrets.json', scope='')
    # Dynamically set the redirect_uri based on the request URL. This is extremely
    # convenient for debugging to an alternative host without manually setting the
    # redirect URI.
    flow.redirect_uri = self.request.url.split('?', 1)[0].rsplit('/', 1)[0]
    return flow

  def GetCodeCredentials(self):
    """Create OAuth 2.0 credentials by extracting a code and performing OAuth2.0.

    The authorization code is extracted form the URI parameters. If it is absent,
    None is returned immediately. Otherwise, if it is present, it is used to
    perform step 2 of the OAuth 2.0 web server flow.

    Once a token is received, the user information is fetched from the userinfo
    service and stored in the session. The token is saved in the datastore against
    the user ID received from the userinfo service.

    Args:
      request: HTTP request used for extracting an authorization code and the
               session information.
    Returns:
      OAuth2.0 credentials suitable for authorizing clients or None if
      Authorization could not take place.
    """
    # Other frameworks use different API to get a query parameter.
    code = self.request.get('code')
    if not code:
      # returns None to indicate that no code was passed from Google Drive.
      return None

    # Auth flow is a controller that is loaded with the client information,
    # including client_id, client_secret, redirect_uri etc
    oauth_flow = self.CreateOAuthFlow()

    # Perform the exchange of the code. If there is a failure with exchanging
    # the code, return None.
    try:
      creds = oauth_flow.step2_exchange(code)
    except FlowExchangeError:
      return None

    # Create an API service that can use the userinfo API. Authorize it with our
    # credentials that we gained from the code exchange.
    users_service = CreateService('oauth2', 'v2', creds)

    # Make a call against the userinfo service to retrieve the user's information.
    # In this case we are interested in the user's "id" field.
    userid = users_service.userinfo().get().execute().get('id')

    # Store the user id in the user's cookie-based session.
    session = sessions.LilCookies(self, SESSION_SECRET)
    session.set_secure_cookie(name='userid', value=userid)

    # Store the credentials in the data store using the userid as the key.
    StorageByKeyName(Credentials, userid, 'credentials').put(creds)
    return creds

  def GetSessionCredentials(self):
    """Get OAuth 2.0 credentials for an HTTP session.

    If the user has a user id stored in their cookie session, extract that value
    and use it to load that user's credentials from the data store.

    Args:
      request: HTTP request to use session from.
    Returns:
      OAuth2.0 credentials suitable for authorizing clients.
    """
    # Try to load  the user id from the session
    session = sessions.LilCookies(self, SESSION_SECRET)
    userid = session.get_secure_cookie(name='userid')
    if not userid:
      # return None to indicate that no credentials could be loaded from the
      # session.
      return None

    # Load the credentials from the data store, using the userid as a key.
    creds = StorageByKeyName(Credentials, userid, 'credentials').get()

    # if the credentials are invalid, return None to indicate that the credentials
    # cannot be used.
    if creds and creds.invalid:
      return None

    return creds

  def RedirectAuth(self):
    """Redirect a handler to an authorization page.

    Used when a handler fails to fetch credentials suitable for making Drive API
    requests. The request is redirected to an OAuth 2.0 authorization approval
    page and on approval, are returned to application.

    Args:
      handler: webapp.RequestHandler to redirect.
    """
    flow = self.CreateOAuthFlow()

    # Manually add the required scopes. Since this redirect does not originate
    # from the Google Drive UI, which authomatically sets the scopes that are
    # listed in the API Console.
    flow.scope = ALL_SCOPES

    # Create the redirect URI by performing step 1 of the OAuth 2.0 web server
    # flow.
    uri = flow.step1_get_authorize_url(flow.redirect_uri)

    # Perform the redirect.
    self.redirect(uri)

  def RespondJSON(self, data):
    """Generate a JSON response and return it to the client.

    Args:
      data: The data that will be converted to JSON to return.
    """
    self.response.headers['Content-Type'] = 'application/json'
    self.response.out.write(json.dumps(data))

  def CreateAuthorizedService(self, service, version):
    """Create an authorize service instance.

    The service can only ever retrieve the credentials from the session.

    Args:
      service: Service name (e.g 'drive', 'oauth2').
      version: Service version (e.g 'v1').
    Returns:
      Authorized service or redirect to authorization flow if no credentials.
    """
    # For the service, the session holds the credentials
    creds = self.GetSessionCredentials()
    if creds:
      # If the session contains credentials, use them to create a Drive service
      # instance.
      return CreateService(service, version, creds)
    else:
      # If no credentials could be loaded from the session, redirect the user to
      # the authorization page.
      self.RedirectAuth()

  def CreateDrive(self):
    """Create a drive client instance."""
    return self.CreateAuthorizedService('drive', 'v2')

  def CreateUserInfo(self):
    """Create a user info client instance."""
    return self.CreateAuthorizedService('oauth2', 'v2')