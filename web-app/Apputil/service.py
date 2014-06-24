import Social
import httplib2

from apiclient.discovery import build

def create(service, version, creds=None):
    return Social.Gapi.create_service(service,version,creds)
