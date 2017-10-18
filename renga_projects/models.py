# -*- coding: utf-8 -*-
#
# Copyright 2017 Swiss Data Science Center (SDSC)
# A partnership between École Polytechnique Fédérale de Lausanne (EPFL) and
# Eidgenössische Technische Hochschule Zürich (ETHZ).
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
"""Define project models."""

from urllib.parse import urlparse

import goblin

from aiogremlin import Cluster
from gremlin_python.process.traversal import Cardinality


class Project(goblin.Vertex):
    """Basic model for project vertecies."""

    __label__ = 'project:project'

    identifier = goblin.Property(goblin.String)
    name = goblin.Property(goblin.String, db_name='project:project_name')
    labels = goblin.VertexProperty(goblin.String, card=Cardinality.list_)


def get_hashable_id(val):
    """Return hashable id even for ``dict``."""
    if isinstance(val, dict) and "@type" in val and "@value" in val:
        if val["@type"] == "janusgraph:RelationIdentifier":
            val = val["@value"]["value"]
    return val


def parse_cluster_url(url):
    """Return mapping from cluster URL definition."""
    config = urlparse(url)
    kwargs = {}
    for key, type_ in (('host', str), ('port', int), ('scheme', str)):
        value = getattr(config, key, None)
        if value:
            kwargs[key] = type_(value)

    print(kwargs)
    if 'host' in kwargs:
        kwargs['hosts'] = [kwargs.pop('host')]
    return kwargs


async def connect(url, loop):
    """Connect to a cluster defined by a URL."""
    cluster = await Cluster.open(loop, **parse_cluster_url(url))
    # TODO , message_serializer=message_serializer))
    graph = goblin.Goblin(cluster, get_hashable_id=get_hashable_id)
    graph.register(Project)
    return graph
