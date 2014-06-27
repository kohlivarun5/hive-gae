# Add the library location to the path
import sys
sys.path.insert(0, '_libs')
sys.path.insert(0, '_modules')


import Gae
import Notify

def home_main_defer(
    userid,
    items,
    update_last_notify_time):

    userinfo = Gae.Userinfo.get(userid)
    Notify.Api.deliver_items(
                userinfo,
                items,
                True,
                userinfo.last_notify_time,
                update_last_notify_time)
