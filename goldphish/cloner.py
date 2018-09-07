#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# Copyright 2018 Nico Duitsmann. All Rights Reserved.
#
# Licensed under the GNU General Public License, Version 3.0.
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#      https://www.gnu.org/licenses/gpl-3.0.html
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

"""Goldphish website cloner."""

import html
import os
import subprocess
import sys
from urllib.request import urlopen

import lxml.html

from goldphish.storage import cloner_ignore_robots


class SiteCloner(object):
    """Website cloner.
    
    :param website:
    :param cloning_dir:
    """

    def __init__(self, website, cloning_dir):
        self.website = website
        self.cloning_dir = cloning_dir

    @DeprecationWarning
    def check_wget(self):
        """Check wget installation (on posix)."""
        try:
            subprocess.call(["wget"], stdout=subprocess.DEVNULL)
        except OSError:
            print('wget was not found on this computer but its required.')
            print('Please install wget and restart goldphish. Exiting.')
            sys.exit()

    def remove_form_action(self):
        """Remove form action attribute."""
        index = os.path.join(self.cloning_dir, 'index.html')

        if not os.path.isfile(index):
            index = input('Website has no index file. Please specify the index file (e.g. login.html): ')
            index = os.path.join(self.cloning_dir, index)

        with open(index, 'r') as index_file:
            _html = index_file.read()
        
        action = lxml.html.fromstring(_html).find('.//form').action
        action = html.escape(action)
        new_html = _html.replace(action, '')
        
        with open(index, 'w') as new_index:
            new_index.write(new_html)
        print('%s overwritten and successful modified.' % index)

    def clone(self):
        """Try to clone website with wget."""      
        if os.name != 'posix':
            wget = os.path.join('tools', 'wget', 'wget.exe')
        else:
            # self.check_wget()
            wget = 'wget'
        
        print('\nCloning {} to {} ..'.format(self.website, self.cloning_dir))

        if cloner_ignore_robots:
            robots = 'off'
        else:
            robots = 'on'
        
        subprocess.call([wget,
                        '--quiet',
                        '--adjust-extension',
                        '--span-hosts',
                        '--convert-links',
                        '--backup-converted',
                        '--no-directories',
                        '--timestamping',
                        '--page-requisites',
                        '-e robots=%s' % robots,
                        '--directory-prefix=' +
                        self.cloning_dir,
                        self.website])
        try:
            self.remove_form_action()
        except:
            pass
