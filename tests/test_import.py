# -*- coding: utf-8 -*-
# SPDX-FileCopyrightText: 2023 KUNBUS GmbH
# SPDX-License-Identifier: GPL-2.0-or-later
"""Test module import."""

import unittest


class ModuleImport(unittest.TestCase):
    def test_import(self):
        """Test the import of the module."""
        import noderedrevpinodes_server

        self.assertEqual(type(noderedrevpinodes_server.__version__), str)
