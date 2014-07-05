from pyh import *
from Core import coretypes as Coretypes

import logging

def make_home(items,root_url,alert=None):

  # Loop and get each items display

  main = div(cl="row")
  d = main << div(style="margin-top:5px;")

  for item in items:
      display = item.web_display(item.data,root_url)
      if display:
        d << _make_card(display)

  return _make_page(Coretypes.PAGE_TAB.Home,[main],alert)

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

  return _make_page(Coretypes.PAGE_TAB.Subscriptions,divs,alert)

_MAX_TEXT_LENGTH = 70 #Unix !
_ELIPSES = " ..."

def _format_text(text):

    if len(text) <= _MAX_TEXT_LENGTH:
        return text

    # Text is greater than length, first we split words, then traverse
    # THe first word do exceed limit is dropped and we put elipses and return!
    words = text.split()
    text = ""
    for word in words:
        word_len = len(word)
        text_len = len(text)
        if (word_len + text_len) > _MAX_TEXT_LENGTH:
            return text + _ELIPSES
        else:
            text = text + " " + word
    return text

ACTIVITY_POST_ROUTE = '/'
def _make_activities(activities):
    
    main = div(style="font-size:78%;padding-right:5px;",
               align="right")

    for activity in activities:
        d = main # << a()
        logging.debug(activity)
        if activity.link:
            d = d << form(action=ACTIVITY_POST_ROUTE,
                          method="post")
            d << input(type="image",src=activity.icon,
                       width="20",height="20",
                       style="padding-right:2px",
                       alt=activity.count)
            activity.link(d,activity.data)

        else:
            d << img(activity.count,width="20",height="20",
                     style="padding-right:2px;",
                     src=activity.icon)

        if activity.count > 0:
            d << b(activity.count,style="vertical-align:middle;color:#073642")

    return main

def make_web_card(params):

    if params is None or params.photo is None:
        return None

    main = article(cl='photo')
    d = main << a()

    if params.poster:
        d1 = d << p()

        d2 = d1 << a(b(params.poster))
        if params.poster_link:
            d2.attributes['href'] = params.poster_link

       
    d = d << table(cl="table table-bordered",
                    style="\
                    table-layout:fixed;\
                    background-color:#F6F7F8;\
                    margin-bottom:10px;\
                    ",
                   )

    if params.text:
        d1 = d << tr()
        d1 = d1 << td(style="padding:3px 5px 2px 5px")

        d1 = d1 << p(params.text,
                     cl="expandableText expandableTextBase")

    d2 = a(img(src=params.photo,width="100%",height="100%"))
    if params.post_link:
        d2.attributes['href'] = params.post_link

    d << tr(td(d2))
    
    if params.logo:
        main << img(style="padding-left:5px;",
                      src=params.logo,width="20",height="20",align="left")
    
    if params.activities and len(params.activities) > 0 :
        main << _make_activities(params.activities)

    return main

def make_glass_card(params):
    if params is None or params.photo is None:
        return None

    main = article(cl='photo')
    main << img(src=params.photo,width="100%",height="100%")
    main << div(cl="overlay-gradient-tall-dark")

    #head = main << header()
    # head ** Put poster pic here
    #head << h1(params.poster)

    if params.text:
        s = main << section()
        s << p(b(params.text), cl="text-auto-size")

    foot = main << footer()
    d1 = foot << div(cl="blue")

    if params.logo:
        d1 << img(src=params.logo,width="34",height="34",
                  align="left")

    d1 << ("@"+(params.poster.replace(" ", "")))

    #logging.info(main.render())

    return main.render()

###################################
## PRIVATES
##################################
def _addJS(tag, *arg):
  for f in arg: 
    tag += script(src=f)

def _addCSS(tag, *arg):
  for f in arg:
    tag += link(rel='stylesheet', type='text/css', href=f)

def _addClickToExpand(tag):

    css_style = r"""
.expandableTextBase {
    text-overflow: ellipsis;
    display: block;
    width:100%;
    margin:2px;
    word-wrap:break-word;
    font-size:110%;
    font-family:monospace;
    color:#657b83;
    padding:2px
}

.expandableText {
    white-space: nowrap;
    overflow: hidden;
}
"""
#.expandableText:hover {
#    text-decoration:none;
#    border-bottom: 1px solid #657b83;
#}
#
#"""

    tag += style(css_style,type="text/css")

    js_script = r"""
//<![CDATA[ 
$(window).load(function(){
$(function () {
    $(".expandableTextBase").click(function () {
        $(this).toggleClass("expandableText");
        $(this).toggleClass("expandedText");
    })
});
});
//]]>  
"""

    tag += script(js_script,type="text/javascript")

def _make_page(tab,divs,alert=None):
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

  def _create_tab(name,link,is_active):
    tab = li(a(name,href=link))
    if is_active:
      tab.attributes['cl'] = 'nav nav-tabs'

    tab << a(name,href=link)
    return tab


  def _make_navbar():
    main = div(cl="navbar navbar-inverse navbar-fixed-top")
    navbar = ((main << div(cl="navbar-inner")) << div(cl="container-fluid"))
    navbar << a((b("{Hive}") + " : " + i("Your social hub")),
                 cl="brand", href="/",style="padding-right:1cm;")
  
    navbar << div(a("Subscriptions",
                    cl="brand navbar-form right", href="/subscriptions"))

    return main
  
  #def _make_navbar_2():
  #  main = div(cl="navbar navbar-inverse navbar-fixed-top")
  #  navbar = main << div(cl="container")
  #  brand  = navbar << div(cl="navbar navbar-header")
  #  brand << a((b("{Hive}") + " : " + i("Your social hub")),
  #             cl="navbar navbar-brand", href="#",style="padding-right:1cm;")

  #  tabs = navbar << div(cl="navbar")
  #  tabs = tabs << ul(cl="nav navbar-nav",id="bs-example-navbar-collapse-1")
  #  tabs << li(a("Home",href="/"),cl="active")
  #  tabs << li(a("Subscriptions",href="/subscriptions"),cl="active")

  #  return main

  page << _make_navbar()
  data_div = page << div(cl="container")

  if alert:
    data_div << div(alert,cl="alert alert-info")

  if divs:
    map(lambda d: data_div << d, divs)

  _addClickToExpand(page.body)

  return page.render()



def _make_card(display):
  main = div(cl="span4")
  d = main << table(style="background-color:#F5F5F9;box-shadow: 5px 5px 10px 5px #888;",
                    cl="table table-bordered")
  d = d << tr()
  d = d << td(display,style="padding:10px")

  return main 

def add_activity_inputs(parent,name,item,activity):

    parent << input(type="hidden", name="service", value=name)
    parent << input(type="hidden", name="item", value=item)
    parent << input(type="hidden", name="activity", value=activity)
    return parent
