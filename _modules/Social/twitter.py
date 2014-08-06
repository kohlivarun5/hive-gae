import tweepy

import Core
import Gae
import Glass 

import logging
import traceback

import json
import oauth2
import urlparse
 
import pytz
import datetime


CALLBACK_LINK = "/twitter_oauth2callback"

NAME="Twitter"

def get_service_info(userinfo,root_url):
  name = NAME
  if (_client(userinfo,root_url) is None):
    return Core.Coretypes.Login_service(
            name=name,
            info=Core.Coretypes.Unsubscribed(
              login_link=(_get_auth_uri(root_url,userinfo))
              )
           )
  else:
    return Core.Coretypes.Login_service(name=name, info=Core.Coretypes.Subscribed())

def get_access_token_from_code(oauth_token,oauth_verifier,userinfo,root_url):
  token = oauth2.Token(oauth_token,userinfo.twitter_request_secret)
  token.set_verifier(oauth_verifier)

  consumer = _get_consumer()
  client = oauth2.Client(consumer, token)

  resp, content = client.request(_ACCESS_TOKEN_URL, "POST")
  logging.info(resp)
  logging.info(content)
  access_token = dict(urlparse.parse_qsl(content))
  logging.info(access_token)
  return access_token

def get_items(params,max_id=None,max_id_time=None):

  userinfo = params.userinfo 
  client = _client(userinfo,params.root_url)

  logging.info(params)

  if client is None:
    return []

  try:
    count = 30 if params.start_time else 20
    dashboard = client.home_timeline(count=count,max_id=max_id)
    logging.debug(dashboard)

  except:
    logging.error("Failure to get Twitter feed:{%s}"
                  %  (traceback.format_exc()))
    return []

  cards = []

  count = 0
  found_time = None
  found_id = None
  logging.info(params.start_time)

  for post in dashboard:

    count = count + 1
    post.created_at =  pytz.utc.localize(post.created_at)
    last_creation_time = post.created_at
    id = post.id
    if max_id_time is None or last_creation_time < max_id_time:
      found_id = id
      found_time = last_creation_time

    if params.start_time is not None and last_creation_time >= params.start_time:
      continue 

    #Only use photo tweets
    if not ( \
        'extended_entities' in post._json and \
        'media' in post._json['extended_entities'] and \
        len(post._json['extended_entities']['media']) > 0 and \
        post._json['extended_entities']['media'][0]['type'] == 'photo'
           ):
      continue

    cards.append(Core.Coretypes.Timeline_item(
              creation_time=last_creation_time,
              data=post,
              web_display=_card_display,
              glass_display=_glass_display))

  logging.info(found_time)
  logging.info(count)

  if found_time and len(cards) == 0 and count > 0:
    return get_items(params,found_id,found_time)

  logging.info(len(cards))
  return cards


_LIKE_ACTIVITY='like'

def _json_object_hook(d): return namedtuple('X', d.keys())(*d.values())
def _json2obj(data): return json.loads(data.replace('\"','"'), object_hook=_json_object_hook)

def apply_activity(userinfo,item,activity,_):
    logging.info(item)

    client = _client(userinfo)
    data = _json2obj(item)
    if activity == _LIKE_ACTIVITY:
        client.like(item.id,item.reblog_key)

    return

############
## PRIVATE
############

_APPLICATION_ID="wVNq8OD84WGCU4ly3wzeg"
_APPLICATION_SECRET = "mhJMASHpNvbQUco9vIB8Eo04fzR9nQ7LCf5nH4dcHw"


_REQUEST_TOKEN_URL = 'https://api.twitter.com/oauth/request_token'
_AUTHORIZATION_URL = 'https://api.twitter.com/oauth/authorize'
_ACCESS_TOKEN_URL = 'https://api.twitter.com/oauth/access_token'

def _get_auth(root_url):
  return tweepy.OAuthHandler(_APPLICATION_ID, _APPLICATION_SECRET,
          ( "%s%s" % (root_url,CALLBACK_LINK)))


def _get_consumer():
  return oauth2.Consumer(_APPLICATION_ID, _APPLICATION_SECRET)

def _get_auth_uri(root_url,userinfo):

  logging.info("Getting twitter auth uri")

  tweepy_auth = _get_auth(root_url)
  uri = tweepy_auth.get_authorization_url()
  request_token = tweepy_auth.request_token

  userinfo.twitter_request_token = tweepy_auth.request_token.key
  userinfo.twitter_request_secret = tweepy_auth.request_token.secret
  Gae.Userinfo.put(userinfo)
  return uri

def _get_redirect_uri(root_url):
  redirect_uri = ("%s%s" % (root_url, CALLBACK_LINK))
  return redirect_uri

def _client(userinfo,root_url):
  if (    (userinfo.twitter_oauth_token is None)
       or (userinfo.twitter_oauth_secret is None)):
    return None
  else:
    tweepy_auth = _get_auth(root_url)
    tweepy_auth.set_access_token(
      userinfo.twitter_oauth_token,
      userinfo.twitter_oauth_secret)
    tweepy_api = tweepy.API(tweepy_auth)
    return tweepy_api

def _like_creator(parent,item):
    j = json.dumps({
                'id'        : item['id'],
                'reblog_key' : item['reblog_key']
                }).replace('"','\"')
    logging.info(j)
    return Core.Html.add_activity_inputs(
            parent,NAME,
            j,
            _LIKE_ACTIVITY)

def _get_activities(data):
  return []
  """
  likes_link = None

  #logging.info(data)
  #if 'id' in data and 'reblog_key' in data:
  #    likes_link = _like_creator

  activities = []
  
  count = 0

  if 'note_count' in data:
      count=data['note_count']

  activities.append(
      Core.Coretypes.Item_activity(
      count,
      data=data,
      icon="/static/images/glyph-heart-pop.png",
      link=likes_link))

  return activities
  """

def _card_params(data,root_url):

  poster = data.user.screen_name.encode('ascii', 'xmlcharrefreplace')
  poster_link = None

  text = data.text.encode('ascii', 'xmlcharrefreplace')
    
  assert  'extended_entities' in data._json and \
          'media' in data._json['extended_entities']
  photo = None 
  photo = data._json['extended_entities']['media'][0]['media_url']

  return Core.Coretypes.Web_card_params(
        logo=root_url+"/static/images/Twitter_logo_blue.png",
        poster=poster,
        poster_link=poster_link,
        post_link=data._json['extended_entities']['media'][0]['url'],
        photo=photo,
        text=text,
        activities=_get_activities(data),
        creation_time=data.created_at
    )


def _card_display(data,root_url):
  return Core.Html.make_web_card(
            _card_params(data,root_url))

def _glass_display(data,is_notify,root_url):
  params = _card_params(data,root_url)

  card = Glass.Card.of_params(
            NAME,
            params,
            is_notify,
            Core.Html.make_glass_card(params))

  return card 
