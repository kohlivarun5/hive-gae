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
    items_map = Social.Subscriptions.get_timeline_items(userinfo,root_url)

    html = _render_page(items_map)
    self.response.out.write(html)

########## PRIVATES ##################
import Core
def _render_page(items_map):
  return Core.Html.make_home(items_map,None)
