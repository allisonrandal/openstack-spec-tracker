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

import glob
import os.path
from os import listdir

from spectracker.specparser import SpecParser

class Specification:
    def __init__(self, name, specfile, project, cycle):
        self.name = name
        self.specfile = specfile
        self.project = project
        self.cycle = cycle

    def extract_text_body(self):
        parser = SpecParser(self.specfile)
        parser.parse()

        self.title = parser.title
        self.blueprint_url = parser.blueprint
        self.phrases = parser.phrases
        print(self.phrases)

    def phrase_frequency(self):
        frequency = {}
        for phrase in self.phrases:
            frequency[phrase] = self.phrases.count(phrase)
        return frequency

class SpecificationSet:
    def __init__(self, projects, cycle, repocache):
        self.projects = projects
        self.cycle = cycle
        self.repocache = os.path.abspath(repocache)
        self.specs = []

    def load_specs(self):
        for project in self.projects:
            specdir = os.path.join(self.repocache, project+"-specs", "specs", self.cycle, "approved")
            for filename in listdir(specdir):
                specfile = os.path.join(specdir, filename)
                if os.path.isfile(specfile) and not os.path.islink(specfile):
                    (specname, extension) = os.path.splitext(filename)
                    self.add_spec(specname, specfile, project)

    def add_spec(self, specname, specfile, project):
        spec = Specification(specname, specfile, project, self.cycle)
        self.specs.append(spec)

    def parse_specs(self):
        for spec in self.specs:
            spec.extract_text_body()
