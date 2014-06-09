from pyh import *
from . import coretypes as Coretypes

def make_home(items_map,alert=None):

  # Loop and get each items display

  main = div(cl="row")
  d = main << div(style="margin-top:5px;")

  for name, items in items_map.iteritems():
    for item in items:
      display = item.web_display(item.data)
      if display:
        d << _make_card(display)

  return _make_page([main],alert)

def make_subscriptions(subscriptions,alert=None):

  divs = []

  for service in subscriptions:

    main = div(cl="span4")
    d = main << h2(service.name)
    d = d << table(bgcolor="#FFFFFF",cl="table table-bordered")
    row = (d << tr())

    d = row << td(colspan="4", align="justify")

    if type(service.info) is Coretypes.Subscribed:
      d << button(("Already subscribed to "+service.name),
                   cl="btn btn-block btn-danger", 
                   disabled="",type='submit')

    elif type(service.info) is Coretypes.Unsubscribed:
      d << a(button(("Login to "+service.name),
                   cl="btn btn-block btn-success", 
                   type="submit"),
             href=service.info.login_link,
             style="text-decoration:none")

    else:
       raise AssertionError()

    divs.append(main)

  return _make_page(divs,alert)


def _addJS(tag, *arg):
  for f in arg: 
    tag += script(src=f)

def _addCSS(tag, *arg):
  for f in arg:
    tag += link(media="screen",rel='stylesheet', type='text/css', href=f)


def _make_page(divs,alert=None):
  page = PyH('{Hive}')

  page.head << link(rel="shortcut icon", sizes="196x196",
                    href="/static/images/main_icon.png")
  page.head << link(rel="apple-touch-icon", href="/static/images/main_icon.png")
  page.head << link(rel="shortcut icon", href="/static/images/favicon.ico")

  page.head << meta(name="mobile-web-app-capable", content="yes")
  page.head << meta(name="viewport", content="width=device-width, initial-scale=1.0")
  page.head << meta(name="viewport", content="width=device-width, initial-scale=1, minimum-scale=1.0, maximum-scale=1.0, minimal-ui")

  _addCSS(page.head,
      '/static/bootstrap/css/bootstrap.min.css',
      '/static/bootstrap/css/bootstrap-responsive.min.css',
      '/static/main.css')

  _addJS(page.body,
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

  if alert:
    data_div << div(alert,cl="alert alert-info")

  if divs:
    map(lambda d: data_div << d, divs)

  return page.render()

def make_web_card(params):

    if params is None or params.photo is None:
        return None

    main = article(cl='photo')
    d = main << a()
    d << img(src=params.photo,width="100%",height="100%")

    if params.post_link:
        d.attributes['href'] = params.post_link

    return main


def _make_card(display):
  main = div(cl="span4")
  d = main << table(style="background-color:#F5F5F9",
                    cl="table table-bordered")
  d = d << tr()
  d = d << td(display,style="padding:30px")

  return main
