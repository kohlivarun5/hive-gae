import facebook

from Core import Coretypes

import dateutil.parser
import logging


CALLBACK_LINK = "/fb_oauth2callback"

def get_service_info(userinfo,root_url):
  name = "Facebook"
  if (userinfo.fb_access_token is None):
    return Coretypes.Login_service(
            name=name,
            info=Coretypes.Unsubscribed(
              login_link=(_get_auth_uri(root_url))
              )
           )
  else:
    return Coretypes.Login_service(name=name, info=Coretypes.Subscribed())

def get_access_token_from_code(code,root_url):
    logging.debug("Getting FB info")
    access = facebook.get_access_token_from_code(
            code,_get_redirect_uri(root_url),
            _APPLICATION_ID,_APPLICATION_SECRET)
    logging.info(access)
    return access["access_token"]

############
## PRIVATE
############

_APPLICATION_ID="679802582055154"
_APPLICATION_SECRET = "e0d8bc2cc81829bb742311ae23117871"

def _get_auth_uri(root_url):
    redirect_uri = _get_redirect_uri(root_url)
    uri = facebook.auth_url(_APPLICATION_ID, redirect_uri,['read_stream'])
    return uri

def _get_redirect_uri(root_url):
    redirect_uri = ("%s%s" % (root_url, CALLBACK_LINK))
    return redirect_uri



def _get_client(access_token):
    return facebook.GraphAPI(access_token)
