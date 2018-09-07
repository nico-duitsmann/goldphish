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

"""Goldphish console output utils."""

import os

from termcolor import colored

from goldphish.storage import cli_colored_output, cli_default_hcolor


def clear():
    """Clear console screen."""
    os.system('cls' if os.name == 'nt' else 'clear')

def colorize(message, color=cli_default_hcolor, attrs=['bold']):
    """Colorize string.

    :param message
    :param color
    :param attrs
    :return message
    """
    if cli_colored_output:
    	return colored(message, color, attrs=attrs)
    else:
    	return message
