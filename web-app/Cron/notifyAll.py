import Social
import Gae 
import Notify

import Apputil

import logging
import webapp2

class Handler(webapp2.RequestHandler):

  def get(self):
    """Handles cron jon to send to all users ."""
    logging.info('Inserting timeline items to all users')
    users = Gae.Userinfo.get_all()
    total_users = users.count()

    if total_users > 10:
        return 'Total user count is %d. Aborting broadcast to save your quota' % (
          total_users)

    for user in users:

      userid = user.key().name()
      logging.info("Processing userid:{%s}" % userid)

      userinfo = Apputil.Userinfo.get_from_request_safe(self)
      root_url = Apputil.Url.get_root_url(self)
      Gae.Deferred.do(_get_and_deliver,userinfo,root_url)


###############
# PRIVATES
###############

def _get_and_deliver(userinfo,root_url):
    items = Social.Subscriptions.get_timeline_items(userinfo,root_url)
    Gae.Deferred.do(Notify.Api.deliver_items,
                userinfo,
                items,
                False,
                userinfo.last_notify_time,
                Gae.Userinfo.update_last_notify_time)
