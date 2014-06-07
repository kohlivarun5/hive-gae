import Oauth
import Social
import Core

import Apputil

import webapp2

class Handler(webapp2.RequestHandler):
  """Request Handler for the home endpoint."""

  @Oauth.Util.auth_required
  def get(self):
    """Render the page."""
    
    userinfo = Apputil.Userinfo.get_from_request_safe(self)
    root_url = Apputil.Url.get_root_url(self)

    subscriptions = Social.Subscriptions.get_subscriptions(userinfo,root_url)
    html = _render_page(subscriptions)
    self.response.out.write(html)


########## PRIVATES ##################
import Core
from Core import Coretypes

def _render_page(subscriptions):
  return Core.Html.make_subscriptions(subscriptions)
