import Core

from oauth2client.client import flow_from_clientsecrets

CALLBACK_LINK = "/oauth2callback"

def get_service_info(userinfo,root_url):
  name = "Google Glass"
  if (userinfo.credentials is None):
    return Core.Coretypes.Login_service(
            name=name,
            info=Core.Coretypes.Unsubscribed(
              login_link=(get_redirect_uri(root_url))
              )
           )
  else:
    return Core.Coretypes.Login_service(
                name=name, info=Core.Coretypes.Subscribed())

def get_auth_flow(root_url):
  """Create OAuth2.0 flow controller."""
  flow = flow_from_clientsecrets('client_secrets.json', scope=_SCOPES)
  # Dynamically set the redirect_uri based on the request URL. This is
  # extremely convenient for debugging to an alternative host without manually
  # setting the redirect URI.
  flow.redirect_uri = ("%s%s" % (root_url, CALLBACK_LINK))
  return flow 

def get_redirect_uri(root_url,is_prompt=True):
  flow = _get_auth_flow(root_url)

  if is_prompt:
    flow.params['approval_prompt'] = 'force'
  uri = flow.step1_get_authorize_url()
  # Perform the redirect.
  return str(uri)
_SCOPES = ('https://www.googleapis.com/auth/glass.timeline '
          'https://www.googleapis.com/auth/glass.location '
          'https://www.googleapis.com/auth/userinfo.profile')

def _get_auth_flow(root_url):
  """Create OAuth2.0 flow controller."""
  flow = flow_from_clientsecrets('client_secrets.json', scope=_SCOPES)
  # Dynamically set the redirect_uri based on the request URL. This is
  # extremely convenient for debugging to an alternative host without manually
  # setting the redirect URI.
  flow.redirect_uri = ("%s%s" % (root_url, CALLBACK_LINK))
  return flow 
