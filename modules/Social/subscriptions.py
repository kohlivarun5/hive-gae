import Core

from . import fb as Fb

SERVICES = [
    Fb
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

  for svc in SERVICES:
    info = svc.get_service_info(userinfo,root_url)

    items = svc.get_items(params)
    if len(items) > 0:
      items_map[info.name] = items

  return items_map
