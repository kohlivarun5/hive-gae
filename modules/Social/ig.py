from instagram import client, subscriptions

import Core
from Core import Coretypes

import pytz

import logging

CALLBACK_LINK = "/ig_oauth2callback"

def get_service_info(userinfo,root_url):
  name = "Instagram"
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
    access,_ = _get_auth(root_url).exchange_code_for_access_token(code)
    access = access
    logging.info(access)
    return access


def get_items(params):

  client = _client(params.userinfo)

  if client is None:
    return []

  logging.info(client)

  media_feed, next = client.user_media_feed()

  cards = []
  for media in media_feed:
    cards.append(Coretypes.Timeline_item(
      creation_time=
        pytz.utc.localize(media.created_time),
      data=media,
      web_display=_card_display,
      glass_display=_card_display))

  logging.debug(cards)
  return cards


############
## PRIVATE
############

_APPLICATION_ID = "d00138f8d3c648d09c649b352d2df266"
_APPLICATION_SECRET = "65cc79818cbe4c72a63e721c6c2d3221"


def _get_auth(root_url):

  CONFIG = {
      'client_id': _APPLICATION_ID,
      'client_secret': _APPLICATION_SECRET,
      'redirect_uri': ("%s%s" % (root_url, CALLBACK_LINK))
  }
  return client.InstagramAPI(**CONFIG)


def _get_auth_uri(root_url):
  auth = _get_auth(root_url)
  uri = auth.get_authorize_url(scope=["likes","comments"])
  return uri

def _client(userinfo):
  if (userinfo.ig_access_token is None):
    return None
  else:
    return client.InstagramAPI(access_token=userinfo.ig_access_token)

def _card_display(data):

    poster = data.user.username.encode('ascii', 'xmlcharrefreplace')
    poster_link = "http://www.instagram.com/" + poster


    return Core.Html.make_web_card(Coretypes.Web_card_params(
        poster=poster,
        poster_link=poster_link,
        post_link=data.link,
        photo=data.get_standard_resolution_url()
    ))
