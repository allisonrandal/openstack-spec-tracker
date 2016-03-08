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

import argparse
import yaml

from spectracker import specification

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument(
        '--config',
        default='spectracker.yaml',
        help='Configuration file (default: spectracker.yaml)',
    )
    parser.add_argument(
        '-o', '--output',
        default='output',
        help='Output directory (default: output/)',
    )
    parser.add_argument(
        '--repocache',
        default='cache/repos',
        help='Cache directory for specs repos (default: cache/repos)',
    )
    args = parser.parse_args()

    with open(args.config) as config_fh:
        config = yaml.load(config_fh)

    spec_set = specification.SpecificationSet(config['projects'], config['cycle'], args.repocache)
    spec_set.load_specs()
