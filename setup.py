# -*- coding: utf-8 -*-
"""Setup-script for noderedrevpinodes-server."""
# SPDX-FileCopyrightText: 2024 KUNBUS GmbH
# SPDX-License-Identifier: GPL-2.0-or-later

from setuptools import find_namespace_packages, setup

from src.noderedrevpinodes_server.__about__ import __version__

with open("README.md") as fh:
    # Load long description from readme file
    long_description = fh.read()

setup(
    name="noderedrevpinodes_server",
    version=__version__,
    packages=find_namespace_packages("src"),
    package_dir={"": "src"},
    include_package_data=True,
    python_requires=">= 3.7",
    install_requires=[
        "bcrypt",
        "cryptography",
        "distro",
        "revpimodio2",
        "websockets",
    ],
    entry_points={
        "console_scripts": [
            "noderedrevpinodes-server = noderedrevpinodes_server.revpi_server:main",
        ],
    },
    platforms=["revolution pi"],
    url="https://revolutionpi.com/",
    license="LGPL-3.0-only",
    license_files=["LICENSE.txt"],
    author="erminas GmbH, KUNBUS GmbH",
    author_email="support@kunbus.com",
    maintainer="KUNBUS GmbH",
    maintainer_email="support@kunbus.com",
    description="Server backend for the RevPi-NodeRed-Nodes",
    long_description=long_description,
    long_description_content_type="text/markdown",
    keywords=["revpi", "revolution pi", "plc", "automation"],
    classifiers=[
        # A list of all classifiers: https://pypi.org/pypi?%3Aaction=list_classifiers
        "Development Status :: 5 - Production/Stable",
        "Environment :: No Input/Output (Daemon)",
        "Intended Audience :: Manufacturing",
        "License :: OSI Approved :: GNU Lesser General Public License v3 (LGPLv3)",
        "Operating System :: POSIX",
        "Topic :: System :: Operating System",
    ],
)
