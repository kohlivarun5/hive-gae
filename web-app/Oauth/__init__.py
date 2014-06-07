from . import main as Main
from . import util as Util

import Social

ROUTES = [
    (Social.Gapi.CALLBACK_LINK,Main.GapiCallbackHandler),
    (Social.Fb.CALLBACK_LINK,Main.FbCallbackHandler)
]
