from Cron import notifyAll as NotifyAll

ROUTES = [
  ('/cron_notifyAll', NotifyAll.Handler),
]
