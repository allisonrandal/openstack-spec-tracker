# Copyright 2011 Thierry Carrez <thierry@openstack.org>
#
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

from launchpadlib.launchpad import Launchpad
from lazr.restfulclient.errors import NotFound


class Blueprint(object):
    priorities = ('Essential', 'High', 'Medium', 'Low', 'Undefined', 'Not')

    implementations = ('Implemented', 'Deployment', 'Needs Code Review',
                       'Beta Available', 'Good progress', 'Slow progress',
                       'Blocked', 'Needs Infrastructure', 'Started',
                       'Not started', 'Unknown', 'Deferred', 'Informational')

    def __init__(self, lbp):
        self.name = lbp.name
        self.pname = lbp.target.name
        self.whiteboard = lbp.whiteboard
        self.priority = lbp.priority
        self.implementation = lbp.implementation_status
        if lbp.milestone:
            self.milestonename = lbp.milestone.name
            self.milestonedate = lbp.milestone.date_targeted or '2099-12-30'
            self.milestonelink = lbp.milestone.web_link
        else:
            self.milestonename = ''
            self.milestonedate = '2099-12-31'
            self.milestonelink = ''
        self.implementationindex = self.implementations.index(
            self.implementation)
        self.priorityindex = self.priorities.index(self.priority)
        self.reviews = []

        self.contributors = []
        if lbp.assignee:
            self.assignee = lbp.assignee.name
            self.contributors.append(lbp.assignee.name)
        else:
            self.assignee = ''

        if lbp.drafter:
            self.drafter = lbp.drafter.name
            self.contributors.append(lbp.drafter.name)
        else:
            self.drafter = ''


class BlueprintSet(object):
    def __init__(self, repocache):
        self.launchpad = Launchpad.login_anonymously(
            'spec-tracker',
            'production',
            repocache + '/launchpadlib-cache',
            version='devel')

    def load_blueprint(self, url):
        api_url = url.replace('blueprints.launchpad.net',
                              'api.launchpad.net/devel')
        try:
            lbp = self.launchpad.load(api_url)
        except NotFound:
            return None

        blueprint = Blueprint(lbp)
        return blueprint
