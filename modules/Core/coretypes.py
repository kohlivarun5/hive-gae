from collections import namedtuple

Subscribed    = namedtuple('Subscribed', [])
Unsubscribed  = namedtuple('Unsubscribed',['login_link'])
Login_service = namedtuple('Login_service',['name','info'])

