import Gae
def create(service, version, creds=None):
    return Gae.DiscoveryDocument.build(service,version,creds)
