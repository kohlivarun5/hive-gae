import pytumblr

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

CALLBACK_LINK = "/tumblr_oauth2callback"

NAME="Tumblr"

def get_service_info(userinfo,root_url):
  name = NAME
  if (_client(userinfo) is None):
    return Core.Coretypes.Login_service(
            name=name,
            info=Core.Coretypes.Unsubscribed(
              login_link=(_get_auth_uri(root_url,userinfo))
              )
           )
  else:
    return Core.Coretypes.Login_service(name=name, info=Core.Coretypes.Subscribed())

def get_access_token_from_code(oauth_token,oauth_verifier,userinfo,root_url):

    token = oauth2.Token(oauth_token,userinfo.tumblr_request_secret)
    token.set_verifier(oauth_verifier)

    consumer = _get_consumer()
    client = oauth2.Client(consumer, token)

    resp, content = client.request(_ACCESS_TOKEN_URL, "POST")
    access_token = dict(urlparse.parse_qsl(content))
    logging.info(access_token)
    return access_token

def get_items(params,offset=None,last_found_time=None):

    userinfo = params.userinfo 
    client = _client(userinfo)

    logging.info(params)
    logging.info(offset)

    if client is None:
      return []

    try:
        limit = 2 if params.start_time else 1
        dashboard = client.dashboard(**{'limit':limit, 'offset':offset, 'type':'photo'})
        logging.debug(dashboard)

    except:
        logging.error("Failure to get Tumblr feed:{%s}"
                        %  (traceback.format_exc()))
        return []

    if 'posts' not in dashboard:
        return []

    cards = []

    count = 0
    found_time = None
    logging.info(params.start_time)
    logging.info(last_found_time)
    for post in dashboard['posts']:
      count = count + 1
      timestamp = post['timestamp']
      last_creation_time = pytz.utc.localize(datetime.datetime.fromtimestamp(timestamp))
      post['timestamp'] = last_creation_time
      logging.debug(last_creation_time)

      if last_found_time is None or last_creation_time < last_found_time:
          found_time = last_creation_time

      if params.start_time is not None and last_creation_time >= params.start_time:
          continue

      cards.append(Core.Coretypes.Timeline_item(
                creation_time=last_creation_time,
                data=post,
                web_display=_card_display,
                glass_display=_glass_display))

    logging.info(offset)
    logging.info(found_time)
    logging.info(count)

    if found_time and len(cards) == 0 and count > 0:
       return get_items(params,(offset+count if offset is not None else count),found_time)

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

_APPLICATION_ID="KUkjPwVV7P4L3xqTaiGJ1VJv0HwRUfo1zanyHyUSCilxw65pH2"
_APPLICATION_SECRET = "sHOedvzUimwEz5u109WtSVmTUSSCQx7ftsT3ziSnbWzhoNLOn4"

_REQUEST_TOKEN_URL = 'http://www.tumblr.com/oauth/request_token'
_AUTHORIZATION_URL = 'http://www.tumblr.com/oauth/authorize'
_ACCESS_TOKEN_URL = 'http://www.tumblr.com/oauth/access_token'

def _get_consumer():
    return oauth2.Consumer(_APPLICATION_ID, _APPLICATION_SECRET)

def _get_auth_uri(root_url,userinfo):

    client = oauth2.Client(_get_consumer())
    resp, content = client.request(_REQUEST_TOKEN_URL, "GET")

    request_token = dict(urlparse.parse_qsl(content))
    auth_url = "%s?oauth_token=%s" % (_AUTHORIZATION_URL, request_token['oauth_token'])
    logging.info(auth_url)

    userinfo.tumblr_request_token = request_token['oauth_token']
    userinfo.tumblr_request_secret = request_token['oauth_token_secret']
    Gae.Userinfo.put(userinfo)

    return auth_url

def _get_redirect_uri(root_url):
    redirect_uri = ("%s%s" % (root_url, CALLBACK_LINK))
    return redirect_uri

def _client(userinfo):
  if (    (userinfo.tumblr_oauth_token is None)
       or (userinfo.tumblr_oauth_secret is None)):
    return None
  else:

    logging.debug(userinfo.tumblr_request_secret)
    logging.debug(userinfo.tumblr_oauth_token)
    logging.debug(userinfo.tumblr_oauth_secret)

    client = pytumblr.TumblrRestClient(
                _APPLICATION_ID,
                _APPLICATION_SECRET,
                userinfo.tumblr_oauth_token,
                userinfo.tumblr_oauth_secret)

    return client

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

def _card_params(data,root_url):

    poster = data['blog_name']#poster_info['name'].encode('ascii', 'xmlcharrefreplace')
    poster_link = data['post_url']

    text = None
    #if 'caption' in data:
    #    text = data['caption']
    
    photo = None
    if 'photos' in data and len(data['photos']) > 0:
        photo = data['photos'][0]['original_size']['url']


    return Core.Coretypes.Web_card_params(
        logo=root_url+"/static/images/tumblr_logo_white_blue_32.png",
        poster=poster,
        poster_link=poster_link,
        post_link=poster_link,
        photo=photo,
        text=text,
        activities=_get_activities(data),
        creation_time=data['timestamp']
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
