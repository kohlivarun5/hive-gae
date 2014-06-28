from google.appengine.ext import ndb

from apiclient.discovery import build_from_document
from apiclient.discovery import DISCOVERY_URI

import datetime
DISCOVERY_DOC_MAX_AGE = datetime.timedelta(hours=24)

class DiscoveryDocument(ndb.Model):
  document = ndb.StringProperty(required=True, indexed=False)
  updated = ndb.DateTimeProperty(auto_now=True, indexed=False)

  @property
  def expired(self):
    now = datetime.datetime.utcnow()
    return now - self.updated > DISCOVERY_DOC_MAX_AGE

def build(serviceName,version,creds):
    key = ndb.Key(DiscoveryDocument, serviceName, 
                  DiscoveryDocument, version, 
                  DiscoveryDocument, DISCOVERY_URI)
    discovery_doc = key.get()

    if discovery_doc is None or discovery_doc.expired:
      # If None, RetrieveDiscoveryDoc() will use default
      document = _RetrieveDiscoveryDoc(serviceName, version)
      discovery_doc = DiscoveryDocument(key=key, document=document)
      discovery_doc.put()

    http = httplib2.Http()
    if creds:
        # Authorize the Http instance with the passed credentials
        creds.authorize(http)
    return build_from_document(discovery_doc.document, http=http)

#### READ SERVICE JSON

import json
import os

# Libraries used by or included with Google APIs Client Library for Python
from apiclient.discovery import DISCOVERY_URI
from apiclient.discovery import _add_query_parameter
from apiclient.errors import HttpError
from apiclient.errors import InvalidJsonError
import httplib2
import uritemplate

def _RetrieveDiscoveryDoc(serviceName, version):

  discoveryServiceUrl=DISCOVERY_URI
  params = {'api': serviceName, 'apiVersion': version}
  requested_url = uritemplate.expand(discoveryServiceUrl, params)

  # REMOTE_ADDR is defined by the CGI spec [RFC3875] as the environment
  # variable that contains the network address of the client sending the
  # request. If it exists then add that to the request for the discovery
  # document to avoid exceeding the quota on discovery requests.
  if 'REMOTE_ADDR' in os.environ:
    requested_url = _add_query_parameter(requested_url, 'userIp',
                                         os.environ['REMOTE_ADDR'])

  http = httplib2.Http()
  resp, content = http.request(requested_url)
  if resp.status >= 400:
    raise HttpError(resp, content, uri=requested_url)

  try:
    service = json.loads(content)
  except ValueError:
    raise InvalidJsonError(
        'Bad JSON: %s from %s.' % (content, requested_url))

  # we return content instead of the JSON deserialized service because
  # build_from_document() consumes a string rather than a dictionary
  return content
