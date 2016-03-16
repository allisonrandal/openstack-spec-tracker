# -*- coding: utf-8 -*-

# Licensed under the Apache License, Version 2.0 (the "License"); you may
# not use this file except in compliance with the License. You may obtain
# a copy of the License at
#
#      http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS, WITHOUT
# WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the
# License for the specific language governing permissions and limitations
# under the License.

import fixtures
import os.path
from spectracker.tests import base

from spectracker.specparser import SpecParser

_SPEC_FILE_SAMPLE = """
..
 This work is licensed under a Creative Commons Attribution 3.0 Unported
 License.

 http://creativecommons.org/licenses/by/3.0/legalcode

==========================================
Example Spec - The title of your blueprint
==========================================

Include the URL of your launchpad blueprint:

https://blueprints.launchpad.net/nova/+spec/example

A single paragraph of prose that operators can understand. The title and this
first paragraph should be used as the subject line and body of the commit
message respectively.

Problem description
===================

Provide a detailed description of the problem. What problem is this blueprint
addressing?

Use Cases
---------

What use cases does this address? What impact on actors does this change have?
Ensure you are clear about the actors in each use case: Developer, End User,
Deployer etc.

Proposed change
===============

Here is where you cover the change you propose to make in detail. How do you
propose to solve this problem?

If this is one part of a larger effort make it clear where this piece ends. In
other words, what's the scope of this effort?

"""


class TestSpecParser(base.TestCase):

    def test_instantiate(self):
        parser = SpecParser('fake-file')
        self.assertEqual(parser.specfile, 'fake-file')

    def test_parser(self):
        example_file = os.path.join(self.temp_dir, 'example.rst')
        with open(example_file, 'w') as f:
            f.write(_SPEC_FILE_SAMPLE)

        parser = SpecParser(example_file)
        parser.parse()

        self.assertEqual(parser.body,
                         _SPEC_FILE_SAMPLE)

        self.assertEqual(parser.title,
                         'Example Spec - The title of your blueprint')

        self.assertEqual(parser.blueprint,
                         'https://blueprints.launchpad.net/nova/+spec/example')

        self.assertEqual(parser.phrases.count('launchpad blueprint'), 1)

    def setUp(self):
        super(TestSpecParser, self).setUp()
        self.temp_dir = self.useFixture(fixtures.TempDir()).path
