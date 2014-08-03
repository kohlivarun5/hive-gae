import sessions

# Load the secret that is used for client side sessions
# Create one of these for yourself with, for example:
# python -c "import os; print os.urandom(64)" > session.secret
SESSION_SECRET = open('session.secret').read()

def load_session_userid(request_handler):
  """Load userid from the current session."""
  session = sessions.LilCookies(request_handler, SESSION_SECRET)
  userid = session.get_secure_cookie(name='userid')
  return userid

def store_userid(request_handler, userid):
  """Store current user's ID in session."""
  session = sessions.LilCookies(request_handler, SESSION_SECRET)
  session.set_secure_cookie(name='userid', value=userid,expires_days=None)
