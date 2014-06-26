from google.appengine.ext import deferred

def do(*args, **kwargs):
    deferred.defer(*args,**kwargs)
