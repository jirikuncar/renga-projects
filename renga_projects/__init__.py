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

from aio_pika import DeliveryMode, Message, connect_robust
from aiohttp import web

from .config import RENGA_GRAPH_URL, RENGA_MQ_URL
from .version import __version__
from .views import setup_routes

# import asyncio
# import uvloop
# asyncio.set_event_loop_policy(uvloop.EventLoopPolicy())

__all__ = ('__version__', 'app')



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
