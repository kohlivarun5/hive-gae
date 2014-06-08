import logging
import webapp2

from google.appengine.api import memcache

import Social
import Apputil
import Core
import Gae

class GapiCallbackHandler(webapp2.RequestHandler):
  """Request handler for OAuth 2.0 code exchange."""
  from oauth2client.client import FlowExchangeError

  def get(self):
    """Handle code exchange."""
    code = self.request.get('code')
    if not code:
      # TODO: Display error.
      return None
    root_url = Apputil.Url.get_root_url(self)
    oauth_flow = Social.Gapi.get_auth_flow(root_url)
    
    try:
      creds = oauth_flow.step2_exchange(code)
    except FlowExchangeError:
      # TODO: Display error.
      return None

    users_service = Apputil.Service.create('oauth2', 'v2', creds)
    # TODO: Check for errors.
    user = users_service.userinfo().get().execute()
    userid = user.get('id')

    Gae.Userinfo.put_credentials(userid,creds)
    Core.Session.store_userid(self, userid)
    self.redirect('/subscriptions')

class FbCallbackHandler(webapp2.RequestHandler):
  """Callback called by fb authentication"""

  def get(self):
    """Get the user's oauth info"""

    code = self.request.get("code")

    logging.debug(code)
    root_url = Apputil.Url.get_root_url(self)
    access_token = Social.Fb.get_access_token_from_code(code,root_url)

    logging.debug(access_token)

    userid = Core.Session.load_session_userid(self)
    userinfo = Gae.Userinfo.get(userid)
    assert userinfo is not None

    userinfo.fb_access_token = access_token
    Gae.Userinfo.put(userinfo)

    memcache.set(key=userid, value="Subscribed to Facebook!", time=5)
    self.redirect('/subscriptions')

class IgCallbackHandler(webapp2.RequestHandler):
  """Callback called by ig authentication"""

  def get(self):
    """Get the user's oauth info"""

    code = self.request.get("code")

    logging.debug(code)
    root_url = Apputil.Url.get_root_url(self)
    access_token = Social.Ig.get_access_token_from_code(code,root_url)

    logging.debug(access_token)

    userid = Core.Session.load_session_userid(self)
    userinfo = Gae.Userinfo.get(userid)
    assert userinfo is not None

    userinfo.ig_access_token = access_token
    Gae.Userinfo.put(userinfo)

    memcache.set(key=userid, value="Subscribed to Instagram!", time=5)
    self.redirect('/subscriptions')
