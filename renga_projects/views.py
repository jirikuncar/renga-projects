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
"""Define REST view handlers."""

import json
import uuid

from aio_pika import DeliveryMode, Message
from aiohttp import web

from .config import RENGA_MQ_CMD_ROUTING, RENGA_MQ_EVENTS_ROUTING
from .models import Project


async def index(request):
    """Return all available projects."""
    session = await request.app['graph'].session()
    projects = await session.traversal(Project).toList()
    return web.json_response(
        {
            'projects': projects,
        }, status=200)


async def create(request):
    """Create new project."""
    data = await request.json()

    project = {
        'identifier': uuid.uuid4().hex,
        'name': data['name'],
        'labels': data.get('labels', []),
    }

    msg = {
        'type': 'create_project',
        'actor': {
                'user_id': 0,
        },
        'payload': project,
    }

    published = await request.app['api'].publish(
        Message(
            json.dumps(msg).encode('utf-8'),
            content_type='application/json',
            delivery_mode=DeliveryMode.PERSISTENT),
        routing_key=RENGA_MQ_CMD_ROUTING)

    if published:
        return web.json_response(project, status=201)
    raise web.HTTPNotAcceptable()


async def view(request):
    """Return information about a project."""
    session = await request.app['graph'].session()
    project = await session.traversal(Project).has(
        Project.identifier, request.match_info['project_id']).next()
    print(project)
    return web.json_response(project.to_dict())


def setup_routes(app):
    """Register routes on application."""
    app.router.add_get('/', index)
    app.router.add_post('/', create)
    app.router.add_get('/{project_id:[0-9a-f]+}', view)
