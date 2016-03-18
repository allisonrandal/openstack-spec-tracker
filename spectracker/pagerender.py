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

from datetime import datetime
from jinja2 import Environment
from jinja2 import FileSystemLoader
import os.path


def render_keytopics(template_dir, output_dir, topics, cycle):
    template_file = "keytopics.html"
    template_env = Environment(loader=FileSystemLoader(template_dir))
    keytopics_tmpl = template_env.get_template(template_file)

    output_file = os.path.join(output_dir, template_file)

    with open(output_file, 'w') as fh:
        fh.write(keytopics_tmpl.render(series=cycle,
                                       date=str(datetime.utcnow()),
                                       frequency=topics))


def render_spec_list(template_dir, output_dir, spec_list):
    template_file = "specifications.html"
    template_env = Environment(loader=FileSystemLoader(template_dir))
    keytopics_tmpl = template_env.get_template(template_file)

    output_file = os.path.join(output_dir, template_file)

    with open(output_file, 'w') as fh:
        fh.write(keytopics_tmpl.render(date=str(datetime.utcnow()),
                                       specset=spec_list))
