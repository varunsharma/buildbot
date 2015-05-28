from buildbot.data import base



class TryClientEndpoint(base.Endpoint):
    isCollection = False
    pathPatterns = """ 
        /tryclient
        /tryclient/i:tryclientid
    """

    def get(self, resultSpec, kwargs):
        return self.master.db.tryclients.getPub(kwargs['tryclientid'])


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
    entityType = EntityType()
