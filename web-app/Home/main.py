import webapp2
import logging

class Handler(webapp2.RequestHandler):
  """Request Handler for the home endpoint."""

  def get(self):
    """Render the page."""

    html = _render_page([])
    self.response.out.write(html)

########## PRIVATES ##################
import Core
def _render_page(items):
  return Core.Html.make_page(None)
