#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""The setup script."""

from setuptools import setup, find_packages

with open('README.md') as readme_file:
    readme = readme_file.read()

with open('HISTORY.md') as history_file:
    history = history_file.read()

requirements = [
    'paho-mqtt',
    'influxdb',
    'cloudant',
    'ibmiotf',
    'chariot_base',
    'gunicorn',
    'falcon',
    'falcon_jsonify'
]

setup_requirements = []

test_requirements = []

setup(
    author="George Theofilis",
    author_email='g.theofilis@clmsuk.com',
    classifiers=[
        'License :: OSI Approved :: Eclipse Public License 1.0',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: Implementation :: CPython',
        'Programming Language :: Python :: Implementation :: PyPy',
    ],
    description="Python Boilerplate contains all the boilerplate you need to create a Python package.",
    install_requires=requirements,
    license="EPL-1.0",
    long_description=readme + '\n\n' + history,
    long_description_content_type='text/markdown',
    include_package_data=True,
    keywords='chariot_northbound_dispatcher',
    name='chariot_northbound_dispatcher',
    packages=find_packages(include=[
        'chariot_northbound_dispatcher',
        'chariot_northbound_dispatcher.*'
    ]),
    setup_requires=setup_requirements,
    test_suite='tests',
    tests_require=test_requirements,
    url='https://github.com/theofilis/chariot_northbound_dispatcher',
    version='0.1.0',
    zip_safe=False,
)
