from buildbot.data import base
from buildbot.data import types


class TryClientEndpoint(base.Endpoint):
    isCollection = False
    pathPatterns = """ 
        /tryclient
        /tryclient/i:tryclientid
    """

    def get(self, resultSpec, kwargs):
        return 'hi'
#        return self.master.db.tryclient.getTryClient(kwargs['tryclientid'])


class TryClient(base.ResourceType):
    name = 'tryclient'
    endpoints = [TryClientEndpoint]
    keyFields = ['tryclientid']

    class EntityType(types.Entity):
        tryclientid = types.Integer()
        name = types.String()
        label = types.String()
        repo = types.String()
        patch = types.String()
    entityType = EntityType(name)
