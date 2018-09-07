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

"""Configuration settings are stored here."""

from goldphish.config import DEFAULT_CONFIG, Config

# program info
goldphish_version   = '0.1'
goldphish_copyright = 'Copyright (c) 2018 Nico Duitsmann'
goldphish_github    = 'https://github.com/nico-duitsmann/goldphish'

Config.init_config(DEFAULT_CONFIG)

# configurations
http_server_host = Config.get('http_server', 'host')
http_server_port = Config.get_int('http_server', 'port')
http_server_custom_redirect = Config.get('http_server', 'custom_redirect')

cli_bannerart_file = Config.get('cli', 'bannerart_file')
cli_colored_banner = Config.get_boolean('cli', 'colored_banner')
cli_colored_output = Config.get_boolean('cli', 'colored_output')
cli_default_hcolor = Config.get('cli', 'default_hcolor')

cloner_cloning_dir = Config.get('cloner', 'cloning_dir')
cloner_timeout_sec = Config.get_int('cloner', 'timeout_sec')
cloner_ignore_robots = Config.get_boolean('cloner', 'ignore_robots')
cloner_auto_clean = Config.get_boolean('cloner', 'auto_clean')

ngrok_authtoken = Config.get('ngrok', 'authtoken')
ngrok_subdomain = Config.get('ngrok', 'subdomain')

internal_server_error_template = \
"""<!DOCTYPE HTML PUBLIC "-//IETF//DTD HTML 2.0//EN">
<html><head>
<title>500 Internal Server Error</title>
</head><body>
<h1>Internal Server Error</h1>
<p>The server encountered an internal error or misconfiguration and was unable to complete your request</p>
<hr>
<address>Apache/2.4.18 (Ubuntu) Server at {} Port {}</address>
</body></html>"""
