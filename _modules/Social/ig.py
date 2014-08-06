from instagram import client, subscriptions

import Core
import Glass

import pytz

import logging

CALLBACK_LINK = "/ig_oauth2callback"

NAME = "Instagram"

def get_service_info(userinfo,root_url):
  name = NAME
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
    logging.debug("Getting IG info")
    access,_ = _get_auth(root_url).exchange_code_for_access_token(code)
    logging.info(access)
    return access


def get_items(params):
  return _get_items_impl(params)

def _get_items_impl(params,media_id=None):
  client = _client(params.userinfo)

  if client is None:
    return []

  logging.info(media_id)

  count = 7 if params.start_time else 3
  media_feed, next_ptr = client.user_media_feed(count=count,max_id=media_id)

  logging.info(media_feed)
  #logging.info(next_ptr)

  cards = []

  next_media_id = None

  for media in media_feed:

    next_media_id = media.id

    media.created_time = pytz.utc.localize(media.created_time)
    creation_time = media.created_time

    if params.start_time and creation_time >= params.start_time:
        continue

    cards.append(Core.Coretypes.Timeline_item(
      creation_time=creation_time,
      data=media,
      web_display=_card_display,
      glass_display=_glass_display))

  logging.info(len(cards))
  if next_ptr is None or len(cards) > 0:
    return cards

  if len(cards) == 0:
    return _get_items_impl(params,next_media_id)
  
  return cards


_LIKE_ACTIVITY='like'

def apply_activity(userinfo,item,activity,_):
    client = _client(userinfo)

    logging.info(activity)
    if activity == _LIKE_ACTIVITY:
        logging.info(activity)
        client.like_media(media_id=item)

    return


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

def _like_creator(parent,item):
    return Core.Html.add_activity_inputs(
            parent,NAME,
            item.id,
            _LIKE_ACTIVITY)

def _get_activities(data):
    activities = []
    activities.append(
            Core.Coretypes.Item_activity(
            count=data.like_count,
            icon="/static/images/glyph-heart-pop.png",
            data=data,
            link=_like_creator))

    return activities

def _card_params(data,root_url):
    poster = data.user.username.encode('ascii', 'xmlcharrefreplace')
    poster_link = "http://www.instagram.com/" + poster

    return Core.Coretypes.Web_card_params(
        logo=root_url+"/static/images/Instagram_Icon_Large.png",
        poster=poster,
        poster_link=poster_link,
        post_link=data.link,
        photo=data.get_standard_resolution_url(),
        text=(data.caption.text.encode('ascii', 'xmlcharrefreplace') 
                if data.caption else None),
        activities=_get_activities(data),
        creation_time=data.created_time
    )

def _card_display(data,root_url):
    return Core.Html.make_web_card(
            _card_params(data,root_url))

def _glass_display(data,is_notify,root_url):
    params = _card_params(data,root_url)
    return Glass.Card.of_params(
            NAME,
            params,
            is_notify,
            Core.Html.make_glass_card(params))
