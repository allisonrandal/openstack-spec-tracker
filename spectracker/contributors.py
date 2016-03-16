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
from datetime import timedelta
import json
import os.path


class Contributors(object):
    def __init__(self, repocache):
        datafile = os.path.join(repocache, "stackalytics",
                                "etc", "default_data.json")
        with open(datafile) as data_fh:
            self.data = json.load(data_fh)
        self.user_index = None
        self.release_index = None

    def build_user_index(self):
        self.user_index = {}
        for user in self.data['users']:
            if 'launchpad_id' in user:
                userid = user['launchpad_id']
                self.user_index[userid] = user

    def build_release_index(self):
        self.release_index = {}
        previous_end = None
        for release in self.data['releases']:
            name = release['release_name'].lower()
            end_date = datetime.strptime(release['end_date'], "%Y-%b-%d")
            if name != 'prehistory':
                start_date = previous_end + timedelta(days=1)
                self.release_index[name] = {'end': end_date,
                                            'start': start_date}
            previous_end = end_date

    def affiliation(self, users, cycle):
        if not self.user_index:
            self.build_user_index()

        if not self.release_index:
            self.build_release_index()

        cycle_start = self.release_index[cycle]['start']
        for userid in users:
            companies = set()
            if userid in self.user_index:
                user = self.user_index[userid]
                if 'companies' in user:
                    for company in user['companies']:
                        if company['end_date']:
                            final = datetime.strptime(company['end_date'],
                                                      "%Y-%b-%d")
                            if final > cycle_start:
                                companies.add(company['company_name'])
                        else:
                            companies.add(company['company_name'])

        return list(companies)
