from collections import namedtuple


ComingSoon    = namedtuple('ComingSoon', [])
Subscribed    = namedtuple('Subscribed', [])
Unsubscribed  = namedtuple('Unsubscribed',['login_link'])
Login_service = namedtuple('Login_service',['name','info'])

Location      = namedtuple('Location',['lat','long'])


Timeline_search_params = namedtuple('Timeline_search_params', [
      'userinfo'
    , 'location'
    , 'start_time'
    , 'root_url'
])

Timeline_item = namedtuple("Timeline_item", [
      'creation_time'
    , 'data'
    , 'web_display'
    , 'glass_display'
])

Item_activity = namedtuple("Item_activity", [
      'count'
    , 'icon'
    , 'data'
    , 'link'
])

Web_card_params = namedtuple("Web_card_params",[
      'poster'
    , 'poster_link'
    , 'post_link'
    , 'photos'
    , 'text'
    , 'logo'
    , 'activities'
    , 'creation_time'
])

##############
## ENUMS
##############

def _enum(*sequential, **named):
    enums = dict(zip(sequential, range(len(sequential))), **named)
    reverse = dict((value, key) for key, value in enums.iteritems())
    enums['reverse_mapping'] = reverse
    return type('Enum', (), enums)

PAGE_TAB = _enum("Home","Subscriptions")
