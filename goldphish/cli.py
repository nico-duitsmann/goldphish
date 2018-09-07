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

"""Goldphish command line interface."""

import sys

from docopt import docopt

from goldphish.output import colorize
from goldphish.server import Server
from goldphish.storage import (cli_bannerart_file, cli_colored_banner,
                               goldphish_copyright, goldphish_github,
                               goldphish_version)


class Cli(object):
    """Goldphish command line interface class."""

    def __init__(self, doc):
        self.args = docopt(doc, version=goldphish_version)
        self.run()

    def load_cli(self, banner):
        """Cli loader.

        :param banner:
        :return
        """
        banner = banner.format(colorize('Goldphish phishing server ' + goldphish_version, 'white', attrs=[]),
                               colorize(goldphish_copyright, 'white', attrs=[]),
                               colorize(goldphish_github, 'white', attrs=[]))

        if not self.args['--no-banner']:
            if cli_colored_banner:
                print(colorize(banner))
            else:
                print(banner)

    def run(self):
        """Run the cli.

        :return
        """
        try:
            self.load_cli(open(cli_bannerart_file, 'r').read())
            server = Server(args=self.args)
            server.run()
        except Exception as e:
            sys.exit(e)
