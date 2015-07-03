# This file is part of Buildbot.  Buildbot is free software: you can
# redistribute it and/or modify it under the terms of the GNU General Public
# License as published by the Free Software Foundation, version 2.
#
# This program is distributed in the hope that it will be useful, but WITHOUT
# ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS
# FOR A PARTICULAR PURPOSE.  See the GNU General Public License for more
# details.
#
# You should have received a copy of the GNU General Public License along with
# this program; if not, write to the Free Software Foundation, Inc., 51
# Franklin Street, Fifth Floor, Boston, MA 02110-1301 USA.
#
# Copyright Buildbot Team Members

from buildbot.data import base
from buildbot.data import types
from buildbot.clients import newtryclient
from twisted.internet import defer


class Client2Data():
    pass


class ClientEndpoint(base.Endpoint):
    isCollection = True
    pathPatterns = """ 
        /clients/n:clientid
    """

    @defer.inlineCallbacks
    def get(self, resultSpec, kwargs):
        clientid = kwargs['clientid']
        bdict = yield self.master.db.clients.getClient(
            clientid=clientid)
        defer.returnValue([
            dict(clientid=bdict['clientid'],
                 name=bdict['name'],
                 repo=bdict['repo'],
                 diff=bdict['diff'])
                ])



class ClientsEndpoint(base.Endpoint):
    isCollection = True
    rootLinkName = 'clients'
    pathPatterns = """ 
        /clients
    """

    @defer.inlineCallbacks
    def get(self, resultSpec, kwargs):
        bdicts = yield self.master.db.clients.getClients()
        defer.returnValue([
            dict(clientid=bd['clientid'],
                 name=bd['name'],
                 repo=bd['repo'],
                 diff=bd['diff'])
            for bd in bdicts])

    def startConsuming(self, callback, options, kwargs):
        return self.master.mq.startConsuming(callback,('clients', None, None))





class Client(base.ResourceType):
    name = 'client'
    plural = 'clients'
    endpoints = [ClientEndpoint, ClientsEndpoint]
    keyFields = ['clientid']

    class EntityType(types.Entity):
        clientid = types.Integer()
        name = types.String()
        repo = types.String()
        diff = types.String()
    entityType = EntityType(name)
