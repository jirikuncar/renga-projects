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

import os

RENGA_MQ_URL = os.environ.get('RENGA_MQ_URL', 'amqp://guest:guest@localhost/')
"""Define AMQP endpoint url."""

RENGA_MQ_CMD_ROUTING = os.environ.get('RENGA_MQ_CMD_ROUTING', 'renga-commands')
"""Define name of command queue."""

RENGA_MQ_EVENTS_ROUTING = os.environ.get('RENGA_MQ_EVENTS_ROUTING',
                                         'renga-events')
"""Define name of event queue."""

RENGA_GRAPH_URL = os.environ.get('RENGA_GRAPH_URL',
                                 'ws://localhost:8182/gremlin')
"""Define Gremlin endpoint url."""
