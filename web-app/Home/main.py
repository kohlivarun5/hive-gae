import webapp2

import Oauth

class Handler(webapp2.RequestHandler):
  """Request Handler for the home endpoint."""

  @Oauth.Util.auth_required
  def get(self):
    """Render the page."""

    html = _render_page([])
    self.response.out.write(html)

########## PRIVATES ##################
import Core
def _render_page(items):
  return Core.Html.make_home(None)
