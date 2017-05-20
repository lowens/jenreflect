#!/usr/bin/env python

from setuptools import setup
import os

package_version=os.getenv("package_version", "0.0.0")

setup(
    name='jenreflect',
    version=package_version,
    description='Jenkins offline mirror tool',
    author='Larry Owens',
    author_email='laurence.owens@gmail.com',
    packages=['jenreflect'],
    install_requires=[
        'requests',
    ],
    tests_require=[
        'nose',
    ],
    test_suite='nose.collector',
    entry_points={
        'console_scripts': [
            'jenreflect = jenreflect.mirror:main',
        ],
    },
)
