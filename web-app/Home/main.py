import webapp2

import Social
import Core

import Apputil
import Oauth

class Handler(webapp2.RequestHandler):
  """Request Handler for the home endpoint."""

  @Oauth.Util.auth_required
  def get(self):
    """Render the page."""

    userinfo = Apputil.Userinfo.get_from_request_safe(self)
    root_url = Apputil.Url.get_root_url(self)
    items = Social.Subscriptions.get_timeline_items(userinfo,root_url)

    html = _render_page(items)
    self.response.out.write(html)

########## PRIVATES ##################
import Core
def _render_page(items):
  return Core.Html.make_home(items)
