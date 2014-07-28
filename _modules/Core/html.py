from pyh import *
from Core import coretypes as Coretypes

import pytz
import logging

def make_home(items,root_url,is_page_request,alert=None):

  # Loop and get each items display

  main = div(cl="row")
  d = main << div(style="margin-top:5px;")

  last_creation_time = None

  service_times = {}
  for (service,item) in items:
      last_creation_time = item.creation_time
      service_times[service] = last_creation_time

      display = item.web_display(item.data,root_url)
      if display:
        d << _make_card(display)

  scripts = []
  if last_creation_time is not None:
    scripts = _appendInfiniteScroll(main,d,service_times,root_url)

  if is_page_request:
      return d.render()
  else:
    return _make_page(Coretypes.PAGE_TAB.Home,
                      [main],scripts,alert,addLoader=True)

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

  return _make_page(Coretypes.PAGE_TAB.Subscriptions,divs,[],alert)

_MAX_TEXT_LENGTH = 80 #Unix !
_ELIPSES = " ..."

def _is_longer_than_limit(text):
    return len(text) > _MAX_TEXT_LENGTH

#def _format_text(text):
#
#    if len(text) <= _MAX_TEXT_LENGTH:
#        return text
#
#    # Text is greater than length, first we split words, then traverse
#    # THe first word do exceed limit is dropped and we put elipses and return!
#    words = text.split()
#    text = ""
#    for word in words:
#        word_len = len(word)
#        text_len = len(text)
#        if (word_len + text_len) > _MAX_TEXT_LENGTH:
#            return text + _ELIPSES
#        else:
#            text = text + " " + word
#    return text

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

import re
def _make_poster_text(poster):
    return "@"+re.sub(r'\s+', '', poster) 

_EASTERN = pytz.timezone('US/Eastern')
def _make_time_stamp(time):
    return time.astimezone(_EASTERN).strftime("%d %b, %I:%M %p")

def make_web_card(params):

    if params is None or params.photo is None:
        return None

    main = article(cl='photo')
    d = main 

    d = d << table(cl="table",
                    style="\
                    table-layout:fixed;\
                    background:#F1ECDE url("+_get_card_background()+") repeat;\
                    margin-bottom:10px;\
                    ",
                   )

    d2 = a(img(src=params.photo,
               style="max-height:520px;display:block;margin:auto;\
                      box-shadow: 0px 0px 12px 0px #646464;",
               height="100%"))

    
    if params.post_link:
        d2.attributes['href'] = params.post_link

    d << tr(td(d2))

    if params.text:
        is_longer_than_limit = _is_longer_than_limit(params.text)

        d1 = d << tr()
        d1 = d1 << td(style="padding:12px 10px 0px 10px")

        cl_prop="expandableTextBase"
        if is_longer_than_limit:
            cl_prop += " expandableText"


        d1 = d1 << p(params.text,
                     cl=cl_prop,
                     onClick="")

    if params.poster:
        d1 = p(style="margin:auto auto auto 5px;")
        main << div(d1,style="padding:0 0 5px 25px;display:inline-block;margin:0 auto;")

        d2 = d1 << a(b(_make_poster_text(params.poster)))
        if params.poster_link:
            d2.attributes['href'] = params.poster_link

    bottom_div = main << div(style="clear:both;text-align:center")

    if params.logo:
        d = div(style="display:inline-block;float:left")
        d << img(style="padding-left:5px;",
                 src=params.logo,width="20",height="20",align="left")
        d << p(_make_time_stamp(params.creation_time),
               style="float:left;\
                      color:#657b83;\
                      font-family: 'Hind', sans-serif;\
                      text-align:left;\
                      display:inline-block;\
                      opacity:0.65;\
                      vertical-align:middle;\
                      font-size:80%;\
                      padding-left:3px;\
                      padding-top:2px;\
                      ")

        bottom_div << d
   
    if params.activities and len(params.activities) > 0 :
        bottom_div << div(_make_activities(params.activities),
                          style="display:inline-block;float:right")

    
    return main

def make_glass_card(params):
    if params is None or params.photo is None:
        return None

    main = article(cl='photo')
    main << img(src=params.photo,
                style="display:block;margin:auto;",
                height="100%")

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
    word-wrap:break-word;
    color:#657b83;
    padding:2px;
    margin:0 0 0 0;
    //font-weight:600;
    font-family: 'Hind', sans-serif;
    text-align:center;
}

.expandableText {
    white-space: nowrap;
    overflow: hidden;
    margin:0 0 5px 0;
}

.loadmoreajaxloaderDiv {
    postion:absolute;
    left: 50%;
}

"""

    tag += style(css_style,type="text/css")

    js_script = r"""
//<![CDATA[ 
$("body").on('click', '.expandableTextBase', function () {
    $(this).toggleClass("expandableText");
    $(this).toggleClass("expandedText");
});
//]]>  
"""

    tag += script(js_script,type="text/javascript")

LAST_CREATION_TIME_TAG='last_creation_time'

def _appendInfiniteScroll(main,d,last_creation_times,root_url):
    _WRAPPER_ID = "infiniteCardsWrapper"
    _LAST_CREATION_TIME_ID="LAST_CREATED_DIV"

    jquery = r"""
//<![CDATA[ 

$(window).scroll(function() {
    if (this.params === undefined)
    {
        this.params = {};
        this.params.extensionFactor = 0.6;
        this.params.nextUpdateLocation 
            = ($(document).height() * this.params.extensionFactor);
        this.params.is_loading = false;
    }

    var params = this.params;

    if(!params.is_loading && $(window).scrollTop() > params.nextUpdateLocation)
    {
        params.is_loading = true;

        var div = $('#"""+_WRAPPER_ID+"""');
        console.log("Initiating infinite scroll");
    
        var times_map = {};
        var some_time_found = false;
        $('."""+_LAST_CREATION_TIME_ID+"""').each(function(i,e) {
            some_time_found = true;
            times_map[e.name] = e.value;
        });
            

        if (!some_time_found)
        { return; }

        $('.loadmoreajaxloaderDiv').show();
        console.log(times_map)
        var data = {
            """+LAST_CREATION_TIME_TAG+""" : JSON.stringify(times_map)
        };

        $.ajax({
          url: '"""+root_url+"""',
          data: data,
          success: function(html) {

              params.is_loading = false;
              $('.loadmoreajaxloaderDiv').hide();
              if(html)
              {
                console.log("Got html");
                var before =  $(document).height();

                $('."""+_LAST_CREATION_TIME_ID+"""').each(function(){
                    this.remove();
                });
                $('#"""+_WRAPPER_ID+"""').append(html); 

                var after =  $(document).height();
                var diff = after - before;

                params.nextUpdateLocation += diff * params.extensionFactor;
              }
          },
          error : function(){
              console.log("Got error");
              params.is_loading = true;
              $('.loadmoreajaxloaderDiv').hide();
          }
        });
    }
});
//]]>  
"""

    main.attributes["id"] = _WRAPPER_ID 

    for service,time in last_creation_times.iteritems():
        d << input(cl=_LAST_CREATION_TIME_ID,type="hidden",
                   value=time,name=service,
                   id=_LAST_CREATION_TIME_ID)


    return [script(jquery,type="text/javascript")]


def _make_page(tab,divs,scripts,alert=None,addLoader=False):
  page = PyH('{Hive}')

  page.head << link(rel="shortcut icon", sizes="196x196",
                    href="/static/images/main_icon.png")

  page.head << link(rel="stylesheet", type='text/css',
                    href="https://fonts.googleapis.com/css?family=Hind:500")

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

  css_style = """
* {
  -webkit-border-radius: 0 !important;
     -moz-border-radius: 0 !important;
          border-radius: 0 !important;
}
.table td {
  border-top:0px;
}

.table th, .table td {
  padding:0px;
}

.p {
  margin:0 0 0 0;
}

"""

  page.head << style(css_style,type="text/css")
  
  page.body.attributes["style"] = "background-color:#dedede"

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
  
  page << _make_navbar()
  data_div = page << div(cl="container",
                         style="display:block;\
                                margin-left:auto;\
                                margin-right:auto;\
                                max-width:750px;")

  if alert:
    data_div << div(alert,cl="alert alert-info")

  if divs:
    map(lambda d: data_div << d, divs)

  if addLoader:
 
   reload_pill = img(cl="loadmoreajaxloader",
                      style="display:block;margin:auto",
                      src="/static/images/ajax-loader.gif",
                      width="35",
                      height="35")
 
   reload_row = div(div(div(_make_card(reload_pill,True),
                       style="margin-top:5px;"),
                       cl="row",
                       style="margin-left:0;"),
                    cl="container loadmoreajaxloaderDiv")


   page.body << reload_row


  _addClickToExpand(page.body)

  for script in scripts:
      page.body << script

  return page.render()

def _get_card_background(display_config=None):
    return "'/static/images/card-background.png'"

def _make_card(display,is_width_100=False):
  main = div(cl="span",
             style="display:block;\
                    margin-left:auto;\
                    margin-right:auto;")

  if is_width_100 :
      main.attributes['style'] += " width:100%;"

  d = main << table(cl="table",
                    style="background:#F1ECDE \
                          url("+_get_card_background()+") repeat;\
                          margin-bottom:40px;\
                          box-shadow: 0px 0px 7px 0px #646464;")

  d = d << tr()
  d = d << td(display,style="padding:10px")

  return main 

def add_activity_inputs(parent,name,item,activity):

    parent << input(type="hidden", name="service", value=name)
    parent << input(type="hidden", name="item", value=item)
    parent << input(type="hidden", name="activity", value=activity)
    return parent
