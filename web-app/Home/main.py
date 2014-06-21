import webapp2

import Social
import Core

import Apputil
import Oauth

import Subscriptions

import logging

class Handler(webapp2.RequestHandler):
  """Request Handler for the home endpoint."""

  @Apputil.Oauth.auth_required
  def get(self):
    """Render the page."""

    userinfo = Apputil.Userinfo.get_from_request_safe(self)
    root_url = Apputil.Url.get_root_url(self)

    if Social.Subscriptions.has_some_subscription(userinfo,root_url):
        html = _render_page(userinfo,root_url)
        self.response.out.write(html)
    else:
        self.response.out.write(
            Subscriptions.Main.render_page(userinfo,root_url,
                "Login to a network to start using {Hive}!"))

  @Apputil.Oauth.auth_required
  def post(self):
    data = self.request

    svc_name  = data.get('service')
    item      = data.get('item')
    activity  = data.get('activity')

    try:
        activity_data = data.get('data') 
    except:
        pass

    userinfo = Apputil.Userinfo.get_from_request_safe(self)
    root_url = Apputil.Url.get_root_url(self)

    Social.Subscriptions.apply_activity(
      userinfo,root_url,svc_name,item,activity,activity_data)

    html = _render_page(userinfo,root_url)
    self.response.out.write(html)

########## PRIVATES ##################
import Core
def _render_page(userinfo,root_url):
  items = Social.Subscriptions.get_timeline_items(userinfo,root_url)
  return Core.Html.make_home(items)
