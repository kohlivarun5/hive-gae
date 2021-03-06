# Add the library location to the path
import sys
sys.path.insert(0, '.')
sys.path.insert(0, '_libs')
sys.path.insert(0, '_modules')

import Social
import Gae
import Notifications

from google.appengine.ext import deferred

def defer_notifications(
    userid,
    items,
    root_url,
    is_notify,
    update_last_notify_time):

    userinfo = Gae.Userinfo.get(userid)
    Notifications.Deliver.deliver_items(
                userinfo,
                items,
                root_url,
                is_notify,
                userinfo.last_notify_time,
                update_last_notify_time)

def get_items_and_deliver(userid,root_url):
    userinfo = Gae.Userinfo.get(userid)
    itemTuples = Social.Subscriptions.get_timeline_items(userinfo,root_url,None,Gae.Userinfo.put)
    items = [] 
    for (service,item) in itemTuples:
        items.append(item)

    defer_notifications(
        userinfo.key().name(),
        items,
        root_url,
        False,
        Gae.Userinfo.update_last_notify_time)
