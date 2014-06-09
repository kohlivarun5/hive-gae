import Core

from . import fb as Fb
from . import ig as Ig

import logging

SERVICES = [
    Fb,
    Ig
]

def get_subscriptions(userinfo,root_url):

  return map (
      lambda service:
        service.get_service_info(userinfo,root_url),
      SERVICES)

def get_timeline_items(userinfo,root_url):

    items_map = {}

    params = Core.Coretypes.Timeline_search_params(
            userinfo=userinfo,
            location=None)

    def get(svc):
        info = svc.get_service_info(userinfo,root_url)
        return (info.name,svc.get_items(params))
 
    results = Core.MtMapper.do(get,SERVICES)

    for (name,items) in results:
        if len(items) > 0:
            items_map[name] = items

    return items_map
