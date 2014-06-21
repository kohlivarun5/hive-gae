from instagram import client, subscriptions

import Core

import pytz

import logging

CALLBACK_LINK = "/ig_oauth2callback"

def get_service_info(userinfo,root_url):
  name = "Instagram"
  if (_client(userinfo) is None):
    return Core.Coretypes.Login_service(
            name=name,
            info=Core.Coretypes.Unsubscribed(
              login_link=(_get_auth_uri(root_url))
              )
           )
  else:
    return Core.Coretypes.Login_service(name=name, info=Core.Coretypes.Subscribed())

def get_access_token_from_code(code,root_url):
    logging.debug("Getting FB info")
    access,_ = _get_auth(root_url).exchange_code_for_access_token(code)
    logging.info(access)
    return access


def get_items(params):

  client = _client(params.userinfo)

  if client is None:
    return []

  logging.info(client)

  media_feed, _ = client.user_media_feed()

  cards = []
  for media in media_feed:
    cards.append(Core.Coretypes.Timeline_item(
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

def _get_activities(data):
    activities = []
    activities.append(
            Core.Coretypes.Item_activity(
            count=data.like_count,
            icon="/static/images/glyph-heart-pop.png",
            data=None,
            link=None))

    return activities

def _card_display(data):

    poster = data.user.username.encode('ascii', 'xmlcharrefreplace')
    poster_link = "http://www.instagram.com/" + poster


    return Core.Html.make_web_card(Core.Coretypes.Web_card_params(
        logo="/static/images/Instagram_Icon_Large.png",
        poster=poster,
        poster_link=poster_link,
        post_link=data.link,
        photo=data.get_standard_resolution_url(),
        text=(data.caption.text.encode('ascii', 'xmlcharrefreplace') 
                if data.caption else None),
        activities=_get_activities(data)
    ))
