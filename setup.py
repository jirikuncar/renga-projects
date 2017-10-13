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

from setuptools import find_packages, setup

readme = open('README.rst').read()
history = open('CHANGES.rst').read()

tests_require = [
    'check-manifest>=0.25',
    'coverage>=4.0',
    'isort>=4.2.2',
    'pydocstyle>=1.0.0',
    'pytest-cache>=1.0',
    'pytest-cov>=1.8.0',
    'pytest-pep8>=1.0.6',
    'pytest>=2.8.0',
]

extras_require = {
    'docs': [
        'Sphinx>=1.6.1',
    ],
    'tests': tests_require,
}

extras_require['all'] = []
for reqs in extras_require.values():
    extras_require['all'].extend(reqs)

setup_requires = [
    'pytest-runner>=2.6.2',
]

install_requires = [
    'aio-pika>=1.4.2',
    'aiohttp>=2.2.5',
    'gremlinpython==3.2.3',
]

packages = find_packages()


# Get the version string. Cannot be done with import!
g = {}
with open(os.path.join('renga_projects', 'version.py'), 'rt') as fp:
    exec(fp.read(), g)
    version = g['__version__']

setup(
    name='renga-projects',
    version=version,
    description=__doc__,
    long_description=readme + '\n\n' + history,
    keywords='Renga service projects',
    license='Apache License 2.0',
    author='Swiss Data Science Center (SDSC)',
    author_email='contact@datascience.ch',
    url='https://github.com/SwissDataScienceCenter/renga-projects',
    packages=packages,
    zip_safe=False,
    include_package_data=True,
    platforms='any',
    entry_points={
    },
    extras_require=extras_require,
    install_requires=install_requires,
    setup_requires=setup_requires,
    tests_require=tests_require,
    classifiers=[
        'Environment :: Web Environment',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: Apache Software License',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Topic :: Internet :: WWW/HTTP :: Dynamic Content',
        'Topic :: Software Development :: Libraries :: Python Modules',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.6',
        'Development Status :: 1 - Planning',
    ],
)
