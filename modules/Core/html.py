from pyh import *

def _addJS(tag, *arg):
  for f in arg: 
    tag += script(src=f)

def _addCSS(tag, *arg):
  for f in arg:
    tag += link(media="screen",rel='stylesheet', type='text/css', href=f)


def make_page(items):
  page = PyH('{Hive}')

  page.head << link(rel="shortcut icon", sizes="196x196",
                    href="/static/images/main_icon.png")
  page.head << link(rel="apple-touch-icon", href="/static/images/main_icon.png")
  page.head << link(rel="shortcut icon", href="/static/images/favicon.ico")

  page.head << meta(name="mobile-web-app-capable", content="yes")
  page.head << meta(name="viewport", content="width=device-width, initial-scale=1.0")
  page.head << meta(name="viewport", content="width=device-width, initial-scale=1, minimum-scale=1.0, maximum-scale=1.0, minimal-ui")

  addCSS(page.head,
      '/static/bootstrap/css/bootstrap.min.css',
      '/static/bootstrap/css/bootstrap-responsive.min.css',
      '/static/main.css')

  addJS(page.body,
      '//ajax.googleapis.com/ajax/libs/jquery/1.9.1/jquery.min.js',
      '/static/bootstrap/js/bootstrap.min.js'
      )

  page.body.attributes["style"] = "background-color:#F1ECDE"

  d = page << div(cl="navbar navbar-inverse navbar-fixed-top")
  nav_div = ((d << div(cl="navbar-inner")) << div(cl="container"))

  nav_div << a((b("{Hive}") + " : " + i("Your social hub")),
               cl="brand", href="/",style="padding-right:1cm;")

  nav_div << div(a("Subscriptions",
                 cl="brand navbar-form right", href="/subscriptions"))

  data_div = page << div(cl="container")
  if items:
    data_div << items

 
  return page.render()
