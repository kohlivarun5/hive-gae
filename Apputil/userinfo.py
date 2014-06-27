import Core
import Gae

def get_from_request(request_handler):
  userid = Core.Session.load_session_userid(request_handler)
  if userid:
    return Gae.Userinfo.get(userid)
  else:
    return None

def get_from_request_safe(request_handler):
  userinfo = get_from_request(request_handler)

  assert userinfo
  return userinfo

def get_id_safe(request_handler):
  userid = Core.Session.load_session_userid(request_handler)
  assert userid
  return userid
