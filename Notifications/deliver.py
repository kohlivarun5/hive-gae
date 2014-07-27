import Gae
import Notify

import logging

CONSUMERS = [
    Notify.Glass
]

def deliver_items(
        userinfo,
        itemsList,
        root_url,
        is_notify,
        last_notify_time,
        update_time_callback):

    items = []
    for item in itemsList:
        if last_notify_time is None or item.creation_time > last_notify_time:
            items.append(item)

    items = reversed(items)

    for consumer in CONSUMERS:
        consumer.deliver_items(
                userinfo,
                items,
                is_notify,
                Gae.DiscoveryDocument.build,
                root_url)

    update_time_callback(userinfo)
