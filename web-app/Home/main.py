import webapp2

import Social
import Core

import Apputil
import Oauth

import Subscriptions

class Handler(webapp2.RequestHandler):
  """Request Handler for the home endpoint."""

  @Apputil.Oauth.auth_required
  def get(self):
    """Render the page."""

    userinfo = Apputil.Userinfo.get_from_request_safe(self)
    root_url = Apputil.Url.get_root_url(self)

    if Social.Subscriptions.has_some_subscription(userinfo,root_url):
        items = Social.Subscriptions.get_timeline_items(userinfo,root_url)

        html = _render_page(items)
        self.response.out.write(html)
    else:
        self.response.out.write(
            Subscriptions.Main.render_page(userinfo,root_url,
                "Login to a network to start using {Hive}!"))

########## PRIVATES ##################
import Core
def _render_page(items):
  return Core.Html.make_home(items)
