import facebook

import Core
import Glass 

import dateutil.parser
import logging
import traceback

import re
import time 

CALLBACK_LINK = "/fb_oauth2callback"

NAME="Facebook"

def get_service_info(userinfo,root_url,_):
  #return Core.Coretypes.Login_service(
  #  name=NAME, info=Core.Coretypes.ComingSoon())

  name = NAME
  if (_client(userinfo) is None):
    return Core.Coretypes.Login_service(
            name=name,
            info=Core.Coretypes.Unsubscribed(
              login_link=(_get_auth_uri(root_url))
            )
           )
  else:
    return Core.Coretypes.Login_service(name=name,
                   info=Core.Coretypes.Subscribed())

def get_access_token_from_code(code,root_url):
  logging.debug("Getting FB info")
  access = facebook.get_access_token_from_code(
            code,_get_redirect_uri(root_url),
            _APPLICATION_ID,_APPLICATION_SECRET)
  logging.info(access)
  return access["access_token"]

from httplib import HTTPException
def get_items(params,until_ts=None,is_retry=False):

  userinfo = params.userinfo 

  if until_ts is None and params.start_time:
    until_ts = params.start_time 

  client = _client(userinfo)

  logging.info(params)
  logging.info(until_ts)

  if client is None:
    return []

  try:
    request_object = {
      'fields' : 
        ",".join([
          'created_time',
          'updated_time',
          'from',
          'link',
          'full_picture',
          'picture',
          'message',
          'object_id',
          'description',
          'actions',
          'likes.limit(1).summary(true)',
          'comments.limit(1).summary(true)'
        ])
    }

    if params.start_time is None:
      request_object['limit'] = 15
    else:
      request_object['limit'] = 30

    if until_ts is not None:
      request_object['until'] = time.mktime(until_ts.timetuple())

    logging.info(request_object)
    news_feed = client.get_connections("me", "home",**request_object)
    logging.debug(news_feed)

  except facebook.GraphAPIError:
    logging.error("Failure to get FB news feed:{%s}"
                    %  (traceback.format_exc()))
    return []
  except HTTPException:
    logging.error("Failure to get FB news feed:{%s}"
                    %  (traceback.format_exc()))
    if is_retry:
      return []
    else:
      return get_items(params,until_ts,True)

  cards = []

  last_creation_time = None

  for post in news_feed['data']:
    post["created_time"] = dateutil.parser.parse(post["created_time"])

    if post["created_time"] != last_creation_time:
      if last_creation_time is None or last_creation_time > post["created_time"]:
        last_creation_time = post["created_time"]

    if 'link' in post and post['link'].find("posts") > -1:
      continue

    if  params.start_time is not None and last_creation_time >= params.start_time:
      continue

    if 'full_picture' in post:
      url =  post['full_picture']

      if (url.find("_t.") > -1 ):
        url = url.replace("_t.", "_n.")
      elif (url.find("_a.") > -1 ):
        url = url.replace("_a.", "_n.")
      elif (url.find("_s.") > -1 ):
        url = url.replsce("_s.", "_n.")
      elif (url.find("_q.") > -1 ):
        url = url.replqce("_q.", "_n.")

      logging.debug(url)
      url = re.sub('%2F[a-z][0-9]+x[0-9]+%2F','%2F',url)
      logging.debug(url)
      post['picture'] = url

    cards.append(Core.Coretypes.Timeline_item(
                  creation_time=last_creation_time,
                  data=post,
                  web_display=_card_display,
                  glass_display=_glass_display))

  logging.info(len(cards))
  logging.info(last_creation_time)
  if len(cards) == 0 and last_creation_time is not None and last_creation_time < until_ts:
    return get_items(params,last_creation_time,is_retry)


  return cards

_LIKE_ACTIVITY='like'

def apply_activity(userinfo,item,activity,_):
  client = _client(userinfo)

  if activity == _LIKE_ACTIVITY:
    client.put_like(item)

  return

############
## PRIVATE
############

_APPLICATION_ID="679802582055154"
_APPLICATION_SECRET = "e0d8bc2cc81829bb742311ae23117871"

def _get_auth_uri(root_url):
  redirect_uri = _get_redirect_uri(root_url)
  uri = facebook.auth_url(_APPLICATION_ID, redirect_uri,['read_stream','publish_actions'])
  return uri

def _get_redirect_uri(root_url):
  redirect_uri = ("%s%s" % (root_url, CALLBACK_LINK))
  return redirect_uri

def _client(userinfo):
  if (userinfo.fb_access_token is None):
    return None
  else:
    return facebook.GraphAPI(userinfo.fb_access_token)

def _like_creator(parent,item):
  return Core.Html.add_activity_inputs(
          parent,NAME,
          (item['object_id'] if 'object_id' in item else item['id']),
          _LIKE_ACTIVITY)

def _get_activities(data):
  likes_link = None
  #comment_link = None

  if 'actions' in data:
    for action in data['actions']:
      if action['name'] == 'Like':
        likes_link = _like_creator

      #if action['name'] == 'Comment':
        #    comment_link = action['link']

  activities = []

  count = 0

  if 'likes' in data and 'summary' in data['likes']:
    count=data['likes']['summary']['total_count']

  activities.append(
    Core.Coretypes.Item_activity(
          count,
          data=data,
          icon="/static/images/FB-ThumbsUp_29.png",
          link=likes_link))

  return activities

def _card_params(data,root_url):
  poster_info = data['from']

  poster = poster_info['name'].encode('ascii', 'xmlcharrefreplace')
  poster_link = "http://www.facebook.com/" + poster_info['id']

  text = None
  if 'message' in data:
    text = data['message'].encode('ascii', 'xmlcharrefreplace')
  elif 'description' in data:
    text = data['description'].encode('ascii', 'xmlcharrefreplace')

  return Core.Coretypes.Web_card_params(
    logo=root_url+"/static/images/FB-f-Logo__blue_29.png",
    poster=poster,
    poster_link=poster_link,
    post_link=(data['link'] if 'link' in data else None),
    photos=([data['picture']] if 'picture' in data else None),
    text=text,
    activities=_get_activities(data),
    creation_time=data['created_time']
  )


def _card_display(data,root_url):
  return Core.Html.make_web_card(
    _card_params(data,root_url))

def _glass_display(data,is_notify,root_url):
  params = _card_params(data,root_url)

  # Don't add links to FB glass!
  params = params._replace(**{'poster_link':None, 'post_link' :None})

  card = Glass.Card.of_params(
    NAME,
    params,
    is_notify,
    Core.Html.make_glass_card(params))

  return card
