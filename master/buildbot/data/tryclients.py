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
from buildbot.clients import NewTryClient
from twisted.internet import defer


class tryClient2Data(tc):
    pass


class TryClientEndpoint(base.Endpoint):
    isCollection = False
    pathPatterns = """ 
        /tryclient
        /tryclient/i:tryclientid
    """

    @defer.inlineCallbacks
    def get(self, resultSpec, kwargs):
        bdicts = yield self.master.db.tryclients.getTryClient(
            tryclientid=kwargs.get('tryclientid', None))
        defer.returnValue([
            dict(tryclientid=bd['tryclientid'],
                 name=bd['name'],
                 repo=bd['repo'],
                 diff=bd['diff'])
            for bd in bdicts])


class TryClient(base.ResourceType):
    name = 'tryclient'
    endpoints = [TryClientEndpoint]
    keyFields = ['tryclientid']

    class EntityType(types.Entity):
        tryclientid = types.Identifier()
        repo = types.String()
        diff = types.String()
    entityType = EntityType(name)
