from . import fb as Fb

def get_subscriptions(userinfo,root_url):
  return [
    Fb.get_service_info(userinfo,root_url)
  ]
