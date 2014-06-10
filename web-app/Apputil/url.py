from urlparse import urlparse

def get_root_url(request_handler):
  pr = urlparse(request_handler.request.url)
  root_url = '%s://%s' % (pr.scheme, pr.netloc)
  return root_url
