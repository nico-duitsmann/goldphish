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

"""Goldphish configuration handling"""

import configparser
import os
import sys

DEFAULT_CONFIG = os.path.join(os.getcwd(), 'config.ini')
DEFAULT_CONFIG_TEMPLATE = \
"""[http_server]
host = localhost
port = 80
custom_redirect = ; Specify a link or file for redirect after post request.

[cli]
bannerart_file = data/banner/default.txt
colored_banner = True
colored_output = True
default_hcolor = red

[cloner]
cloning_dir   = webroot ; Default cloning dir. Do not change if it's not necessary
timeout_sec   = 300  ; Cancel cloning website after timeout reached
ignore_robots = True ; By set it to true you agree with terms of use
auto_clean    = True ; Clean cloning dir folder after program exit

[ngrok]
authtoken = ; Request one at https://dashboard.ngrok.com/user/signup
subdomain = ; !Note: Custom subdomain only with paid account"""


class Config:
    """Config class."""

    config = configparser.ConfigParser(
                allow_no_value=True,
                inline_comment_prefixes=';')

    @staticmethod
    def restore(file):
        """Restore config file.
        
        :param file:
        """
        with open(file, 'r') as config_old:
            config_old = config_old.read()
        
        if config_old != DEFAULT_CONFIG_TEMPLATE:
            with open(file, 'w') as config_new:
                config_new.write(DEFAULT_CONFIG_TEMPLATE)
        
        del config_old

    @staticmethod
    def init_config(file):
        """Initialize config.
        
        :param file:
        """
        if file:
            Config.config.read(file)

    @staticmethod
    def set(section, option, value):
        """Set option in section.

        :param section:
        :param option:
        :param value:
        """
        if Config.config.has_option(section, option):
            Config.config.set(section, option, value)

    @staticmethod
    def get(section, option):
        """Return option from section.

        :param section:
        :param option:
        :return Config.config.get(section, option)
        """
        if Config.config.has_option(section, option):
            return Config.config.get(section, option)

    @staticmethod
    def get_boolean(section, option):
        """Return option from section as boolean.

        :param section:
        :param option:
        :return Config.config.getboolean(section, option)
        """
        if Config.config.has_option(section, option):
            return Config.config.getboolean(section, option)

    @staticmethod
    def get_int(section, option):
        """Return option from section as int.

        :param section:
        :param option:
        :return Config.config.getint(section, option)
        """
        if Config.config.has_option(section, option):
            return Config.config.getint(section, option)

    @staticmethod
    def get_float(section, option):
        """Return option from section as float.

        :param section:
        :param option:
        :return Config.config.getfloat(section, option)
        """
        if Config.config.has_option(section, option):
            return Config.config.getfloat(section, option)
