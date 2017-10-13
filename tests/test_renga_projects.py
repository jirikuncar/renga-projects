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

"""Module tests."""

from __future__ import absolute_import, print_function

from flask import Flask

from renga_projects import RengaProjects


def test_version():
    """Test version import."""
    from renga_projects import __version__
    assert __version__


def test_init():
    """Test extension initialization."""
    app = Flask('testapp')
    ext = RengaProjects(app)
    assert 'renga-projects' in app.extensions

    app = Flask('testapp')
    ext = RengaProjects()
    assert 'renga-projects' not in app.extensions
    ext.init_app(app)
    assert 'renga-projects' in app.extensions


def test_view(app):
    """Test view."""
    RengaProjects(app)
    with app.test_client() as client:
        res = client.get("/")
        assert res.status_code == 200
        assert 'Welcome to Renga-Projects' in str(res.data)
