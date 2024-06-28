# -*- coding: utf-8 -*-
# SPDX-FileCopyrightText: 2024 KUNBUS GmbH
# SPDX-License-Identifier: GPL-2.0-or-later
"""Start main application of this package."""

# If we are running from a wheel, add the wheel to sys.path
if __package__ == "":
    from os.path import dirname
    from sys import path

    # __file__ is package-*.whl/package/__main__.py
    # Resulting path is the name of the wheel itself
    package_path = dirname(dirname(__file__))
    path.insert(0, package_path)

if __name__ == "__main__":
    import sys

    try:
        # Use absolute import in the __main__ module
        from noderedrevpinodes_server.revpi_server import main

        # Run the main application of this package
        sys.exit(main())

    except Exception as e:
        sys.stderr.write(f"Can not start __main__ module: {e}\n")
        sys.exit(1)
