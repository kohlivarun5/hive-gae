import facebook

import Core
from Core import Coretypes

import dateutil.parser
import logging
import traceback

CALLBACK_LINK = "/fb_oauth2callback"


def get_service_info(userinfo,root_url):
  name = "Facebook"
  if (_client(userinfo) is None):
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


def get_items(params):

    userinfo = params.userinfo
    client = _client(userinfo)
    if client is None:
      return []

    try:
        news_feed = client.get_connections("me", "home")
    except facebook.GraphAPIError:
        logging.error("Failure to get FB news feed:{%s}"
                        %  (traceback.format_exc()))
        return []

    cards = []
    
    for post in news_feed['data']:
      if 'picture' in post:
        post['picture'] = post['picture'].replace("_s.","_n.")
      cards.append(Coretypes.Timeline_item(
                creation_time=
                  dateutil.parser.parse(post["created_time"]),
                data=post,
                web_display=_card_display,
                glass_display=_card_display))

    logging.debug(cards)
    return cards


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

def _client(userinfo):
  if (userinfo.fb_access_token is None):
    return None
  else:
    return facebook.GraphAPI(userinfo.fb_access_token)


def _card_display(data):

    poster_info = data['from']

    poster = poster_info['name'].encode('ascii', 'xmlcharrefreplace')
    poster_link = "http://www.facebook.com/" + poster_info['id']

    return Core.Html.make_web_card(Coretypes.Web_card_params(
        poster=poster,
        poster_link=poster_link,
        post_link=(data['link'] if 'link' in data else None),
        photo=(data['picture'] if 'picture' in data else None)
    ))
