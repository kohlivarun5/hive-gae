# Add the library location to the path
import sys
sys.path.insert(0, '_libs')
sys.path.insert(0, '_modules')

import Social

import Gae
import Notify

from google.appengine.ext import deferred

def defer_notifications(
    userid,
    items,
    is_notify,
    update_last_notify_time):

    userinfo = Gae.Userinfo.get(userid)
    Notify.Api.deliver_items(
                userinfo,
                items,
                is_notify,
                userinfo.last_notify_time,
                update_last_notify_time)

def get_items_and_deliver(userid,root_url):
    userinfo = Gae.Userinfo.get(userid)
    items = Social.Subscriptions.get_timeline_items(userinfo,root_url)
    defer_notifications(
        userinfo.key().name(),
        items,
        False,
        Gae.Userinfo.update_last_notify_time)
