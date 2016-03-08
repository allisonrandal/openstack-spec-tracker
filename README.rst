============
Spec Tracker
============

Specification Tracking Tool for OpenStack

Inspired by the ReleaseStatus tool (retired in the Mitaka cycle), the Spec
Tracker gathers information from the OpenStack -specs repos, Launchpad, and
Gerrit, and produces static HTML that shows key themes for the release cycle,
and estimated progress toward completion of all specs for the cycle.

* Free software: Apache license
* Source: https://github.com/allisonrandal/openstack-spec-tracker

Prerequisites
-------------

You'll need the following Python modules installed:
 - launchpadlib
 - jinja2
 - yaml

You'll also need a valid SSH key for accessing Gerrit via SSH
installed in ~/.gerritssh/id_rsa.

Usage
-----

python3 generate_static_html.py

It may take a few minutes to run, depending on the number of
projects and how many specs they contain.

Configuration
-------------

The YAML configuration file describes the series and projects
you want to generate data for. See comments in the example file
spec-tracker.yaml.sample for details.
