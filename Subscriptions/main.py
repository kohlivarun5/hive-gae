import Oauth
import Social
import Core

import Apputil

import webapp2

class Handler(webapp2.RequestHandler):
  """Request Handler for the home endpoint."""

  @Apputil.Oauth.auth_required
  def get(self):
    """Render the page."""
    
    userinfo = Apputil.Userinfo.get_from_request_safe(self)
    root_url = Apputil.Url.get_root_url(self)

    self.response.out.write(render_page(userinfo,root_url))


import Core
from Core import Coretypes

def render_page(userinfo,root_url,alert=None):
  subscriptions = Social.Subscriptions.get_subscriptions(userinfo,root_url)
  return Core.Html.make_subscriptions(subscriptions,alert)
