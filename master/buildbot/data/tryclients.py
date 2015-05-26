from buildbot.data import base


class TryClient(base.ResourceType):
    name = 'tryclient'
    endpoints = []
    keyFields = ['tryclientid']

    class EntityType(types.Entity):
        tryclientid = types.Integer()
        name = types.String()
        num_taps = types.Integer()
        closes_at = types.Integer()
    entityType = EntityType()


class PubEndpoint(base.Endpoint):
    pathPattern = ( 'tryclient', 'i:tryclientid' )
    def get(self, resultSpec, kwargs):
        return self.master.db.tryclients.getPub(kwargs['tryclientid'])

class PubResourceType(base.ResourceType):
    @base.updateMethod
    @defer.inlineCallbacks
    def setPubTapList(self, pubid, beers):
        pub = yield self.master.db.pubs.getPub(pubid)
        self.produceMessage(pub, ’taps-updated’)
