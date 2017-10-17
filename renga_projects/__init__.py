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
"""Service to manage project interactions with the Renga platform."""

import json
import os
import uuid

from aio_pika import connect_robust, Message, DeliveryMode
from aiohttp import web

from .version import __version__

# import asyncio
# import uvloop
# asyncio.set_event_loop_policy(uvloop.EventLoopPolicy())

__all__ = ('__version__', 'app')

RENGA_MQ_URL = os.environ.get('RENGA_MQ_URL', 'amqp://guest:guest@localhost/')
RENGA_MQ_CMD_ROUTING = os.environ.get('RENGA_MQ_CMD_ROUTING', 'renga-commands')
RENGA_MQ_EVENTS_ROUTING = os.environ.get('RENGA_MQ_EVENTS_ROUTING',
                                         'renga-events')
RENGA_GRAPH_URL = os.environ.get('RENGA_GRAPH_URL',
                                 'ws://localhost:8182/gremlin')


async def index(request):
    """Return all available projects."""
    g = request.app['g']
    data = g.V().hasLabel('project:project').valueMap('id', 'name').toList()
    # data = g.V().has('type', 'project:project').toList()
    # data = [v.__dict__ for v in g.V()]
    return web.json_response(
        {
            'projects': data,
        }, status=200)


async def create(request):
    """Create new project."""
    data = await request.json()

    project = {
        'identifier': uuid.uuid4().hex,
        'name': data['name'],
        'labels': data.get('labels', []),
    }

    data = {
        'type': 'create_project',
        'actor': {
            'user_id': 0,
        },
        'payload': project,
    }

    published = await request.app['api'].publish(
        Message(
            json.dumps(data).encode('utf-8'),
            content_type='application/json',
            delivery_mode=DeliveryMode.PERSISTENT),
        routing_key=RENGA_MQ_CMD_ROUTING)

    if published:
        return web.json_response(project, status=201)
    raise web.HTTPNotAcceptable()


async def view(request):
    """Return information about a project."""
    g = request.app['g']
    project = g.V().hasLabel('project:project').has(
        'id', request.match_info['project_id']).valueMap('id', 'name').next()
    print(project)
    return web.json_response({
        'identifier': project['id'],
        'name': project['name'],
    })


def setup_routes(app):
    """Register routes on application."""
    app.router.add_get('/', index)
    app.router.add_post('/', create)
    app.router.add_get('/{project_id:[0-9a-f]+}', view)


async def on_startup(app):
    """Create a connection to message queue and open a channel."""
    app['connection'] = connection = await connect_robust(
        RENGA_MQ_URL, loop=app.loop)
    app['channel'] = channel = await connection.channel()
    app['api'] = channel.default_exchange

    from gremlin_python.structure.graph import Graph
    from gremlin_python.driver.driver_remote_connection import \
        DriverRemoteConnection
    from gremlin_python.process.strategies import ReadOnlyStrategy

    graph = Graph()
    app['g'] = graph.traversal().withRemote(
        DriverRemoteConnection(RENGA_GRAPH_URL, 'g')).withStrategies(
            ReadOnlyStrategy)


async def on_shutdown(app):
    """Close the connection to message queue."""
    await app['connection'].close()
    await app['g'].close()


app = web.Application()
setup_routes(app)

app.on_startup.append(on_startup)
app.on_shutdown.append(on_shutdown)
