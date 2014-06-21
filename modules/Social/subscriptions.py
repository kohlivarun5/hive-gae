import Core

from Social import fb as Fb
from Social import ig as Ig

SERVICES = [
    Ig,
    Fb
]

def get_subscriptions(userinfo,root_url):

  return map (
      lambda service:
        service.get_service_info(userinfo,root_url),
      SERVICES)

def has_some_subscription(userinfo,root_url):
    subscriptions = get_subscriptions(userinfo,root_url)
    
    has_some_subscription = reduce(
            (lambda acc,service:
                acc or 
                (type(service.info) is Core.Coretypes.Subscribed)), 
            subscriptions, False)

    return has_some_subscription
    
def has_all_subscriptions(userinfo,root_url):
    subscriptions = get_subscriptions(userinfo,root_url)
    
    has_all_subscriptions = reduce(
            (lambda acc,service:
                acc and 
                (type(service.info) is Core.Coretypes.Subscribed)), 
            subscriptions, True)

    return has_all_subscriptions


from collections import OrderedDict
def get_timeline_items(userinfo,root_url):

    items_map = {}

    params = Core.Coretypes.Timeline_search_params(
            userinfo=userinfo,
            location=None)

    def get(svc):
        info = svc.get_service_info(userinfo,root_url)
        return (info.name,svc.get_items(params))
 
    results = Core.MtMapper.do(get,SERVICES)

    items_map = {}
    for (name,items) in results:
        for item in items:
            items_map[item.creation_time] = item

    od = OrderedDict(sorted(items_map.items()))
    items = []
    for _, v in od.iteritems():
        items.append(v)

    items.reverse()
    return items 
