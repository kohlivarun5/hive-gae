import Core
import Gae

def get_from_request(request_handler):
  userid = Core.Session.load_session_userid(request_handler)
  if userid:
    return Gae.Userinfo.get(userid)
  else:
    return None

def get_from_request_safe(request_handler):
  userid = get_from_request(request_handler)

  assert userid
  return userid
