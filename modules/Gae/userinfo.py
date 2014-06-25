from google.appengine.ext import db
from oauth2client.appengine import CredentialsProperty

import logging

import datetime
import pytz

class Userinfo(db.Model):
  """Datastore entity for storing OAuth2.0 credentials.

  The CredentialsProperty is provided by the Google API Python Client, and is
  used by the Storage classes to store OAuth 2.0 credentials in the data store.
  """
  credentials = CredentialsProperty()

  creation_time = db.DateTimeProperty(auto_now_add=True)
  update_time = db.DateTimeProperty(auto_now=True)

  twitter_oauth_token_key = db.StringProperty(required=False)
  twitter_oauth_token_key = db.StringProperty(required=False)
  twitter_oauth_token_secret = db.StringProperty(required=False)
  twitter_oauth_verifier = db.StringProperty(required=False)
  twitter_access_token = db.StringProperty(required=False)
  twitter_access_secret = db.StringProperty(required=False)

  ig_access_token = db.StringProperty(required=False)
  fb_access_token = db.StringProperty(required=False)

  last_notify_time = db.DateTimeProperty(required=False)

def get(userid):
    logging.info("Getting creds for{%s}" % userid)
    userinfo = Userinfo.get_by_key_name(userid)

    if userinfo is not None and userinfo.last_notify_time is not None:
        logging.debug("Loading user debug")
        logging.debug(userinfo.last_notify_time)
        userinfo.last_notify_time = pytz.utc.localize(
                userinfo.last_notify_time)

    return userinfo

def put(userinfo):
  userinfo.put()

from oauth2client.appengine import StorageByKeyName
def put_credentials(userid,creds):
    StorageByKeyName(Userinfo, userid, 'credentials').put(creds)

def update_last_notify_time(userinfo):
    userinfo.last_notify_time = datetime.datetime.now(pytz.utc)

    logging.debug("Saving user debug")
    logging.debug(userinfo.last_notify_time)

    put(userinfo)

