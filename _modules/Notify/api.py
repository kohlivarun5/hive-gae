from Notify import glass as Glass

CONSUMERS = [
    Glass
]

def deliver_items(
        userinfo,
        items,
        is_notify,
        last_notify_time,
        update_time_callback):

    items = filter(
            lambda item:
            item.creation_time > last_notify_time 
            if last_notify_time is not None
            else True,
            items)

    items = reversed(items)

    for consumer in CONSUMERS:
        consumer.deliver_items(
                userinfo,
                items,
                is_notify)

    update_time_callback(userinfo)
