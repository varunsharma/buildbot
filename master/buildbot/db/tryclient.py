from buildbot.db import base
from twisted.internet import defer


class TryClientConnectorComponent(base.DBConnectorComponent):

    def getTryClient(self, name):
        return 'Hi from %s' %name

