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
import json

import logging

class Handler(webapp2.RequestHandler):
  """Request Handler for the home endpoint."""

  @Apputil.Oauth.auth_required
  def get(self):
    """Render the page."""

    logging.info("Start rendering main page")

    logging.info(self.request.body)
    logging.info(self.request)

    last_creation_times = self.request.get(Core.Html.LAST_CREATION_TIME_TAG)
    some_time_found = False
    times_map = None

    logging.error(last_creation_times)
    if last_creation_times is not None and last_creation_times != "":
        times_map = json.loads(last_creation_times)
        some_time_found = True

    if some_time_found:
        for svc,time in times_map.iteritems():
            times_map[svc] = iso8601.parse_date(time)

    logging.info(times_map)

    userinfo = Apputil.Userinfo.get_from_request_safe(self)
    root_url = Apputil.Url.get_root_url(self)

    has_all_subs = Social.Subscriptions.has_all_subscriptions(userinfo,root_url)

    if has_all_subs or Social.Subscriptions.has_some_subscription(userinfo,root_url):

        html,items = _render_page(userinfo,root_url,times_map,some_time_found)
        self.response.out.write(html)

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
def _render_page(userinfo,root_url,start_times,some_time_found):
  items = Social.Subscriptions.get_timeline_items(userinfo,root_url,start_times)
  items_array = []
  for svc,item in items:
      items_array.append(item)
  return (Core.Html.make_home(items,root_url,some_time_found),items_array)


