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

import sqlalchemy as sa
import sqlalchemy.exc
from buildbot.db import base
from twisted.internet import defer


class ClientConnectorComponent(base.DBConnectorComponent):

    @defer.inlineCallbacks
    def addClient(self, name, repo=None, diff=None):
        def thd(conn):
            try:
                tbl = self.db.model.clients
                q = tbl.insert()
                conn.execute(q, name=name, repo=repo, diff=diff)
            except (sa.exc.IntegrityError, sa.exc.ProgrammingError):
                pass
        return self.db.pool.do(thd)

    @defer.inlineCallbacks
    def removeClient(self, clientid):
        def thd(conn):
            tbl = self.db.model.clients
            conn.execute(tbl.delete(
                whereclause=(tbl.c.clientid == clientid)))
        return self.db.pool.do(thd)

    @defer.inlineCallbacks
    def findClientId(self, name):
        tbl = self.db.model.clients
        name_hash = self.hashColumns(name)
        return self.findSomethingId(
            tbl=tbl,
            whereclause=(tbl.c.name_hash == name_hash),
            insert_values=dict(
                name=name,
                name_hash=name_hash,
            ))

    @defer.inlineCallbacks
    def getClient(self, clientid):
        client = yield self.getClients(_clientid=clientid)
        if client:
            defer.returnValue(client[0])

    def getClients(self, _clientid=None):
        def thd(conn):
            client_tbl = self.db.model.clients

            wc = None
            if _clientid:
                wc = (client_tbl.c.id == _clientid)

            q = sa.select([client_tbl.c.id, client_tbl.c.name],
                          whereclause=wc)

            return [dict(id=row.id, name=row.name)
                    for row in conn.execute(q).fetchall()]
        return self.db.pool.do(thd)
