import Core
import Gae
import Social

import Apputil

import httplib2
from oauth2client.client import AccessTokenRefreshError

import logging

def auth_required(handler_method):
  """A decorator to require that the user has authorized the Glassware."""

  def check_auth(self, *args):
    root_url = Apputil.Url.get_root_url(self)
    redirect_url = Social.Gapi.get_redirect_uri(root_url)

    userinfo = _load_session_userinfo(self)

    logging.info(userinfo)

    if userinfo is None:
      return self.redirect(redirect_url)


    self.userid = Core.Session.load_session_userid(self)
    self.credentials = userinfo.credentials

    self.mirror_service = Apputil.Service.create('mirror', 'v1', self.credentials)

    if self.credentials:
      try:
        self.credentials.refresh(httplib2.Http())
        return handler_method(self, *args)
      except AccessTokenRefreshError:
        # Access has been revoked.
        Core.Session.store_userid(self, '')
        credentials_entity = userinfo.credentials
        if credentials_entity:
          credentials_entity.delete()

    self.redirect(redirect_url)

  return check_auth

def _load_session_userinfo(request_handler):
  """Load credentials from the current session."""
  return Apputil.Userinfo.get_from_request(request_handler)
