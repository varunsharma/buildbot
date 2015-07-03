# This file is part of Buildbot. Buildbot is free software: you can
# redistribute it and/or modify it under the terms of the GNU General Public
# License as published by the Free Software Foundation, version 2.
#
# This program is distributed in the hope that it will be useful, but WITHOUT
# ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS
# FOR A PARTICULAR PURPOSE. See the GNU General Public License for more
# details.
#
# You should have received a copy of the GNU General Public License along with
# this program; if not, write to the Free Software Foundation, Inc., 51
# Franklin Street, Fifth Floor, Boston, MA 02110-1301 USA.
#
# Copyright Buildbot Team Members

import sqlalchemy as sa


def upgrade(migrate_engine):
    metadata = sa.MetaData()
    metadata.bind = migrate_engine

    clients = sa.Table('clients', metadata,
                    sa.Column('clientid', sa.Integer, primary_key=True),
                    # client's name
                    sa.Column('name', sa.Text, nullable=False),
                    # sha1 of name; used for a unique index
                    sa.Column('name_hash', sa.String(40), nullable=False),
                    # link of the repository to compare get the diff from
                    sa.Column('repo', sa.String(100), nullable=False),
                    # the diff of the patch to try
                    sa.Column('diff', sa.String(1000), nullable=False),
                    )


    # create the new tables
    clients.create()

    # indices
    idx = sa.Index('client_id', clients.c.clientid)
    idx.create()
    idx = sa.Index('client_name_hash', clients.c.name_hash, unique=True)
    idx.create()
