#    Licensed under the Apache License, Version 2.0 (the "License"); you may
#    not use this file except in compliance with the License. You may obtain
#    a copy of the License at
#
#         http://www.apache.org/licenses/LICENSE-2.0
#
#    Unless required by applicable law or agreed to in writing, software
#    distributed under the License is distributed on an "AS IS" BASIS, WITHOUT
#    WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the
#    License for the specific language governing permissions and limitations
#    under the License.

import docutils.parsers.rst
import docutils.utils
from docutils import nodes

import re

class SpecParser:
    def __init__(self, specfile):
        parser = docutils.parsers.rst.Parser()

        with open(specfile) as spec_fh:
            body = spec_fh.read()

        settings = docutils.frontend.OptionParser(components=(docutils.parsers.rst.Parser,)).get_default_values()
        document = docutils.utils.new_document(specfile, settings)
        parser.parse(body, document)

        self.doctree = document
        self.blueprint = None

    def spec_title(self):
        # The first title in the first section is the document title
        if len(self.doctree):
            for section in self.doctree:
                if isinstance(section, nodes.section):
                    for element in section:
                        if isinstance(element, nodes.title):
                            return element.astext()

    def spec_paragraphs(self):
        # Scan the document tree for paragraphs of text
        url_pattern = re.compile('https://blueprints\.launchpad\.net/[a-z]+/\+spec/[a-z\-]+')
        paragraphs = []
        if len(self.doctree):
            for section in self.doctree:
                if isinstance(section, nodes.section):
                    for element in section:
                        if isinstance(element, nodes.paragraph):
                            text = element.astext()
                            match = url_pattern.match(text)
                            if match:
                                self.blueprint = match.group()
                            else:
                                paragraphs.append(text)
                        elif isinstance(element, nodes.section):
                            for subelement in element:
                                if isinstance(subelement, nodes.paragraph):
                                    paragraphs.append(subelement.astext())

        return paragraphs
