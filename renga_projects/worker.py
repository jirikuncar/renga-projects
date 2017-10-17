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
"""Implement worker for storing projects in knowledge graph."""
import os
import json

import asyncio
import aio_pika

from gremlin_python.structure.graph import Graph
from gremlin_python.driver.driver_remote_connection import DriverRemoteConnection

from renga_projects import RENGA_GRAPH_URL, RENGA_MQ_URL, RENGA_MQ_CMD_ROUTING, \
    RENGA_MQ_EVENTS_ROUTING


async def main(loop):
    """Read messages and create nodes in the graph."""
    connection = await aio_pika.connect_robust(RENGA_MQ_URL, loop=loop)
    channel = await connection.channel()
    await channel.set_qos(prefetch_count=1)

    api = await channel.declare_queue(RENGA_MQ_CMD_ROUTING, durable=True)

    events = await channel.declare_exchange(RENGA_MQ_EVENTS_ROUTING,
                                            aio_pika.ExchangeType.FANOUT)

    graph = Graph()
    g = graph.traversal().withRemote(
        DriverRemoteConnection(RENGA_GRAPH_URL, 'g'))

    async for message in api:
        with message.process():
            print(message.body)
            data = json.loads(message.body)['payload']

            project = g.addV('project:project').property(
                'name', data['name']
            ).property('id', data['identifier']).next()
            print(project)

            await events.publish(
                aio_pika.Message(
                    message.body,
                    content_type='application/json',
                    delivery_mode=aio_pika.DeliveryMode.PERSISTENT),
                routing_key=RENGA_MQ_EVENTS_ROUTING)


if __name__ == "__main__":
    loop = asyncio.get_event_loop()
    loop.run_until_complete(main(loop))
    loop.close()
