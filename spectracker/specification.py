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

import os.path
import re

from spectracker.blueprint import BlueprintSet
from spectracker.contributors import Contributors
from spectracker.specparser import SpecParser


class Specification(object):
    def __init__(self, name, specfile, project, cycle, url):
        self.name = name
        self.specfile = specfile
        self.project = project
        self.cycle = cycle
        self.url = url
        self.blueprint_url = None
        self.blueprint = None
        self.phrases = None
        self.affiliation = None

    def extract_text_body(self):
        parser = SpecParser(self.specfile)
        parser.parse()

        self.title = parser.title
        self.blueprint_url = parser.blueprint
        self.phrases = parser.phrases

    def phrase_frequency(self):
        frequency = {}
        for phrase in self.phrases:
            frequency[phrase] = self.phrases.count(phrase)
        return frequency

    def annotate_with_launchpad(self, launchpad):
        if self.blueprint_url:
            self.blueprint = launchpad.load_blueprint(self.blueprint_url)

    def annotate_with_affiliation(self, launchpad, contributors):
        if not self.blueprint:
            self.annotate_with_launchpad(launchpad)

        if not self.blueprint:
            return []

        self.affiliation = contributors.affiliation(
            self.blueprint.contributors, self.cycle)
        print(self.name, self.affiliation)


class SpecificationSet(object):
    def __init__(self, projects, cycle, repocache):
        self.projects = projects
        self.cycle = cycle
        self.repocache = os.path.abspath(repocache)
        self.specs = []
        self.contributor_index = None
        self.launchpad = None

    def clone(self, specs=None):
        clone = SpecificationSet(self.projects, self.cycle, self.repocache)
        clone.contributor_index = self.contributor_index
        clone.launchpad = self.launchpad

        if specs:
            clone.specs = specs
        else:
            clone.specs = self.specs

        return clone

    def load_specs(self):
        for project in self.projects:
            specdir = os.path.join(self.repocache, project + "-specs",
                                   "specs", self.cycle)
            baseurl = 'http://specs.openstack.org/openstack'
            for root, directory, files in os.walk(specdir):
                for filename in files:
                    specfile = os.path.join(root, filename)
                    specurl = specfile.replace(self.repocache, baseurl)
                    specurl = specurl.replace('.rst', '.html')
                    self.add_spec(filename, specfile, project, specurl)

    def add_spec(self, filename, specfile, project, specurl):
        if os.path.isfile(specfile) and not os.path.islink(specfile):
            (specname, extension) = os.path.splitext(filename)
            if extension == '.rst' and specname not in ['index', 'template']:
                spec = Specification(specname, specfile,
                                     project, self.cycle, specurl)
                self.specs.append(spec)

    def parse_specs(self):
        for spec in self.specs:
            spec.extract_text_body()

    def aggregate_topic_frequency(self, skiptopics=None):
        frequency = {}

        first_char_pattern = re.compile('[a-z0-9]')
        for spec in self.specs:
            for phrase in spec.phrases:
                match = first_char_pattern.match(phrase)
                if not match:
                    continue

                if skiptopics and phrase in skiptopics:
                    continue

                if phrase in frequency:
                    frequency[phrase] += spec.phrases.count(phrase)
                else:
                    frequency[phrase] = spec.phrases.count(phrase)

        highfrequency = {k: v for k, v in frequency.items() if v > 10}

        return highfrequency

    def annotate_with_launchpad(self):
        if not self.contributor_index:
            self.contributor_index = Contributors(self.repocache)

        if not self.launchpad:
            self.launchpad = BlueprintSet(self.repocache)

        for spec in self.specs:
            spec.annotate_with_launchpad(self.launchpad)
            spec.annotate_with_affiliation(self.launchpad,
                                           self.contributor_index)

    def filter_by_company(self, company):
        self.annotate_from_launchpad()

        filtered_specs = []
        for spec in self.specs:
            if company in spec.affiliation:
                filtered_specs.append(spec)

        filtered_set = self.clone(specs=filtered_specs)

        return filtered_set
