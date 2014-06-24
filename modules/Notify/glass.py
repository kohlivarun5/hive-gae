import Social

def deliver_items(userinfo,items,is_notify):

    cards = map(lambda item:
            item.glass_display(
                item.data,is_notify),items)
    
    mirror_service = Social.Gapi.create_service(
            'mirror', 'v1', userinfo.credentials)

    map((lambda card:
         mirror_service.timeline().insert(body=card).execute()
         if card is not None else None),
         cards)
