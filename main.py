# Add the library location to the path
import sys
sys.path.insert(0, '.')
sys.path.insert(0, '_libs')
sys.path.insert(0, '_modules')

import webapp2

# Import all All handler modules
import Home
import Oauth
import Subscriptions
import Cron

ROUTES = (
    Home.ROUTES
  + Oauth.ROUTES
  + Subscriptions.ROUTES
  + Cron.ROUTES
  )

app = webapp2.WSGIApplication(ROUTES)
