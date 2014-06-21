from Oauth import main as Main

import Social

ROUTES = [
    (Social.Gapi.CALLBACK_LINK,Main.GapiCallbackHandler),
    (Social.Fb.CALLBACK_LINK,Main.FbCallbackHandler),
    (Social.Ig.CALLBACK_LINK,Main.IgCallbackHandler)
]
