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

from docutils import nodes
import docutils.parsers.rst
from docutils.parsers.rst import Directive
from docutils.parsers.rst import roles
import docutils.utils

import re
from textblob import TextBlob


class SpecParser(object):
    def __init__(self, specfile):
        self.specfile = specfile
        self.doctree = None
        self.title = None
        self.blueprint = None
        self.phrases = None

    def load_file(self):
        with open(self.specfile) as spec_fh:
            self.body = spec_fh.read()

    def parse_file(self):
        roles.register_generic_role('ref', nodes.emphasis)
        docutils.parsers.rst.directives.register_directive("literalinclude",
                                                           MockLiteralInclude)
        docutils.parsers.rst.directives.register_directive("nwdiag",
                                                           MockBlockDiag)
        parser = docutils.parsers.rst.Parser()

        settings = docutils.frontend.OptionParser(
            components=(docutils.parsers.rst.Parser,)).get_default_values()

        document = docutils.utils.new_document(self.specfile, settings)
        parser.parse(self.body, document)

        self.doctree = document

    def spec_scanner(self):
        # Scan the document tree for paragraphs of text
        url_pattern = re.compile(
            'https://blueprints\.launchpad\.net/[a-z]+/\+spec/[a-z0-9\-]+')
        paragraphs = []
        if len(self.doctree):
            for section in self.doctree:
                if isinstance(section, nodes.section):
                    for element in section:
                        if isinstance(element, nodes.title) and not self.title:
                            # The first title in the first section is the
                            # document title
                            self.title = element.astext()

                        elif isinstance(element, nodes.paragraph):
                            text = element.astext()
                            match = url_pattern.search(text)
                            if match:
                                self.blueprint = match.group()
                            else:
                                paragraphs.append(text)

                            for subelement in element:
                                if isinstance(subelement, nodes.target):
                                    link = subelement.attributes["refuri"]
                                    match = url_pattern.search(link)
                                    if match:
                                        self.blueprint = match.group()

                        elif isinstance(element, nodes.section):
                            for subelement in element:
                                if isinstance(subelement, nodes.paragraph):
                                    paragraphs.append(subelement.astext())

        return paragraphs

    def parse_text(self):
        paragraphs = self.spec_scanner()
        textparser = TextBlob(" ".join(paragraphs))
        self.phrases = textparser.noun_phrases

    def parse(self):
        self.load_file()
        self.parse_file()
        self.parse_text()


# Sphinx has a 'literalinclude', 'blockdiag', and 'nwdiag' directives
# that docutils doesn't have. We don't need the content, so just mock
# the directives. Parsing succeeds, while ignoring the directive.

class MockLiteralInclude(Directive):
    required_arguments = 1
    optional_arguments = 0
    final_argument_whitespace = True
    option_spec = {}
    has_content = False

    def run(self):
        include_file = docutils.parsers.rst.directives.uri(self.arguments[0])
        include_node = nodes.literal_block(rawsource=include_file)
        return [include_node]


class MockBlockDiag(Directive):
    required_arguments = 0
    optional_arguments = 0
    final_argument_whitespace = True
    option_spec = {}
    has_content = True

    def run(self):
        self.assert_has_content()
        text = '\n'.join(self.content)
        block_node = nodes.literal_block(rawsource=text)
        return [block_node]
