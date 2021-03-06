import Core

from Social import fb as Fb
from Social import ig as Ig
from Social import tumblr as Tumblr
from Social import twitter as Twitter

import logging

SERVICES = [
    Ig,
    Twitter,
    Tumblr,
    Fb,
]

def get_subscriptions(userinfo,root_url,userinfo_saver):

  return map (
          lambda (info,svc): info,
      _get_subscriptions(userinfo,root_url,userinfo_saver))

def has_some_subscription(userinfo,root_url,userinfo_saver):
    subscriptions = get_subscriptions(userinfo,root_url,userinfo_saver)
    
    has_some_subscription = reduce(
            (lambda acc,service:
                acc or 
                (type(service.info) is Core.Coretypes.Subscribed)), 
            subscriptions, False)

    return has_some_subscription
    
def has_all_subscriptions(userinfo,root_url,userinfo_saver):
    subscriptions = get_subscriptions(userinfo,root_url,userinfo_saver)
    
    has_all_subscriptions = reduce(
            (lambda acc,service:
                acc and 
                (type(service.info) is Core.Coretypes.Subscribed)), 
            subscriptions, True)

    return has_all_subscriptions


from collections import OrderedDict
def get_timeline_items(userinfo,root_url,start_times,userinfo_saver):

    items_map = {}

    logging.info(start_times)
   
    def get(svc):
        info = svc.get_service_info(userinfo,root_url,userinfo_saver)
        logging.info("Start job for %s" % (info.name))

        logging.info(info.name)
        logging.info(start_times)

        start_time = None
        if start_times and info.name in start_times:
            start_time = start_times[info.name]

        if start_times and start_time is None:
            return (info.name,[])

        logging.info(start_time)
        params = Core.Coretypes.Timeline_search_params(
            userinfo=userinfo,
            start_time=start_time,
            root_url=root_url,
            location=None)
        logging.info("End job for %s" % (info.name))
        return (info.name,svc.get_items(params))
 
    logging.info("Start threads with %d items" % (len(SERVICES)))
    results = Core.MtMapper.do(get,SERVICES)
    #results = map(get,SERVICES) #Core.MtMapper.do(get,SERVICES)
    logging.info("Done with %d items" % (len(SERVICES)))

    items_map = {}
    for (service,items) in results:
        for item in items:
            items_map[item.creation_time] = (service,item)

    od = OrderedDict(sorted(items_map.items()))
    items = []
    for _, v in od.iteritems():
        items.append(v)

    logging.info("Found %d items" % (len(items)))

    items = filter(
            lambda (svc,item): 
            (start_times is None or (svc in start_times and item.creation_time < start_times[svc])),
            items)

    logging.info(start_times)
    logging.info("Found %d items after filter" % (len(items)))
    items.reverse()
    return items 

def apply_activity(userinfo,root_url,svc_name,item,activity,activity_data,userinfo_saver):
    services = _get_subscriptions(userinfo,root_url,userinfo_saver)

    for (info,service) in services:
        if info.name == svc_name:
            service.apply_activity(userinfo,item,activity,activity_data)
            return

def _get_subscriptions(userinfo,root_url,userinfo_saver):
  return map (
      lambda service:
        (service.get_service_info(userinfo,root_url,userinfo_saver),service),
      SERVICES)
