import Social
import Gae 
import Notify


import Apputil

from google.appengine.ext import deferred
import deferutil as DeferUtil

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

      userinfo = Gae.Userinfo.get(userid)
      root_url = Apputil.Url.get_root_url(self)
      deferred.defer(
              DeferUtil.get_items_and_deliver, 
              userinfo.key().name(),root_url)


###############
# PRIVATES
###############


