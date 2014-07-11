import webapp2

import Social
import Core
import Gae 

import Apputil
import Oauth

import Subscriptions

import deferutil as DeferUtil
from google.appengine.ext import deferred

import iso8601

import logging

class Handler(webapp2.RequestHandler):
  """Request Handler for the home endpoint."""

  @Apputil.Oauth.auth_required
  def get(self):
    """Render the page."""

    logging.info("Start rendering main page")

    last_creation_time = self.request.get(Core.Html.LAST_CREATION_TIME_TAG)

    if last_creation_time is not None and last_creation_time != "":
        last_creation_time = iso8601.parse_date(last_creation_time)
    else:
        last_creation_time = None

    logging.error(last_creation_time)

    userinfo = Apputil.Userinfo.get_from_request_safe(self)
    root_url = Apputil.Url.get_root_url(self)

    has_all_subs = Social.Subscriptions.has_all_subscriptions(userinfo,root_url)

    if has_all_subs or Social.Subscriptions.has_some_subscription(userinfo,root_url):

        #if has_all_subs:
        #    logging.info("Setting cache")
        #    self.response.headers['Cache-Control'] = "private,s-maxage=300,max-age=300"

        html,items = _render_page(userinfo,root_url,last_creation_time)
        self.response.out.write(html)

        #logging.debug(self.response)

        deferred.defer(
            DeferUtil.defer_notifications,
            userinfo.key().name(),
            items,
            root_url,
            False,
            Gae.Userinfo.update_last_notify_time)

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
    self.redirect('/')

########## PRIVATES ##################
import Core
def _render_page(userinfo,root_url,start_time):
  items = Social.Subscriptions.get_timeline_items(userinfo,root_url,start_time)
  return (Core.Html.make_home(items,root_url,(start_time is not None)),items)
