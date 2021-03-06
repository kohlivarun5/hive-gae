
def of_params(
        bundleId,
        params,
        is_notify,
        html):

    if html is None:
        return None

    body = {}

    body['html'] = html

    body['bundleId'] = "Hive_bundle_"+bundleId

    if is_notify:
        body['notification'] = {'level': 'DEFAULT'}

    body['menuItems'] = []

    if params.post_link is not None:
        body['menuItems'].append({
            'action': 'OPEN_URI',
            'payload': params.post_link,
        })

    if params.poster_link is not None:
        link = {
            'action': 'OPEN_URI',
            'payload': params.poster_link,
        }

        if params.poster is not None:
            link['values'] = [{
                'displayName' : params.poster }]
        body['menuItems'].append(link)


    body['menuItems'].extend([
      {
        "action": "CUSTOM",
        "id": "Hive_refresh_"+bundleId,
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

    return body
