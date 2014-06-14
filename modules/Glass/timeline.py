


def deliver_cards(
        userinfo,
        items,
        mirror_service,
        is_notify):

    for item in items:
        body = item.glass_display(item.data)
        if body is None:
            continue

        body = _update_body(is_notify)


def _body_of_params(body,is_notify,name):

    body['bundleId'] = "Hive_bundle_"+name

    if is_notify:
        body['notification'] = {'level': 'DEFAULT'}

    body['menuItems'] = []

    body['menuItems'].extend([
      {
        "action": "CUSTOM",
        "id": "Hive_refresh_"+name,
        "values": [{
          "displayName": "Refresh",
          "iconUrl": 
          "http://findicons.com/files/icons/2152/snowish/128/gtk_refresh.png"
        }]
      },
      {
        'action': 'TOGGLE_PINNED'
      }
    ])

def create_body(params):
    body = {}
    if params.links is not None:

        links = map(
            lambda (name,link):

            body['menuItems'].append(
            ({
                'action': 'OPEN_URI',
                'payload': link,
                "values": [{ "displayName": name, }]
            }
            if name is not None else
            {
                'action': 'OPEN_URI',
                'payload': link
            })
            ), params.links)

    return None
