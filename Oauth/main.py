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

    userinfo = Gae.Userinfo.get(userid)

    # Decide what to show based on subscriptions
    subscriptions = Social.Subscriptions.get_subscriptions(userinfo,root_url)
    is_new_user = True
    for sub in subscriptions:
        if type(sub.info) is Core.Coretypes.Subscribed:
            is_new_user=False
            break

    if is_new_user:
        self.redirect('/subscriptions')
    else:
        self.redirect('/')

import Subscriptions
def _render_after_subscription(self,userinfo,root_url,alert):

    if Social.Subscriptions.has_all_subscriptions(userinfo,root_url):
        self.redirect('/')
    else:
        self.response.out.write(
            Subscriptions.Main.render_page(
                userinfo,root_url,alert))


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

    _render_after_subscription(self,userinfo,root_url,
            "Subscribed to Facebook!")

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
    
    _render_after_subscription(self,userinfo,root_url,
            "Subscribed to Instagram!")

class TumblrCallbackHandler(webapp2.RequestHandler):
  """Callback called by ig authentication"""

  def get(self):
    """Get the user's oauth info"""

    oauth_token = self.request.get("oauth_token")
    oauth_verifier = self.request.get("oauth_verifier")

    userid = Core.Session.load_session_userid(self)
    userinfo = Gae.Userinfo.get(userid)
    assert userinfo is not None

    root_url = Apputil.Url.get_root_url(self)
    access_token = Social.Tumblr.get_access_token_from_code(oauth_token,
                                                            oauth_verifier,
                                                            userinfo,root_url)

    logging.info(access_token)
    userinfo.tumblr_oauth_token =  access_token['oauth_token']
    userinfo.tumblr_oauth_secret = access_token['oauth_token_secret']
    Gae.Userinfo.put(userinfo)
    
    _render_after_subscription(self,userinfo,root_url,
            "Subscribed to Tumblr!")
