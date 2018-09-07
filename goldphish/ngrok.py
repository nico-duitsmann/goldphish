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

"""Ngrok utils."""

import json
import os
import shutil
import subprocess
import sys
import time
import zipfile
from platform import system
from urllib.request import urlopen

from goldphish.config import Config
from goldphish.output import clear, colorize
from goldphish.storage import ngrok_authtoken


class Ngrok:
    """Ngrok class."""

    NGROK_ROOT = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 'tools', 'ngrok')

    class Installer(object):
        """Ngrok installer class."""

        NGROK_LINKS = {
            'linux': {
                '32': 'https://bin.equinox.io/c/4VmDzA7iaHb/ngrok-stable-linux-386.zip',
                '64': 'https://bin.equinox.io/c/4VmDzA7iaHb/ngrok-stable-linux-amd64.zip'
            },
            'darwin': {
                '32': 'https://bin.equinox.io/c/4VmDzA7iaHb/ngrok-stable-darwin-386.zip',
                '64': 'https://bin.equinox.io/c/4VmDzA7iaHb/ngrok-stable-darwin-amd64.zip',
            },
            'windows': {
                '32': 'https://bin.equinox.io/c/4VmDzA7iaHb/ngrok-stable-windows-386.zip',
                '64': 'https://bin.equinox.io/c/4VmDzA7iaHb/ngrok-stable-windows-amd64.zip',
            },
            'freebsd': {
                '32': 'https://bin.equinox.io/c/4VmDzA7iaHb/ngrok-stable-freebsd-386.zip',
                '64': 'https://bin.equinox.io/c/4VmDzA7iaHb/ngrok-stable-freebsd-amd64.zip',
            },
        }

        def __init__(self):
            try:
                self.run()
            except KeyboardInterrupt:
                sys.exit('\nInstallation cancelled by user.')

        def download(self, link):
            """Download ngrok for specific platform.

            :param link:
            :return:
            """
            path = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 'data', 'temp')
            if not os.path.exists(path): os.mkdir(path)

            filename = os.path.join(path, 'ngrok.zip')

            dest = Ngrok.NGROK_ROOT
            if not os.path.exists(dest): os.mkdir(dest)
            print('Downloading %s..' % link)

            with urlopen(link) as response, open(filename, 'wb') as out_file:
                shutil.copyfileobj(response, out_file)

            print('Unzipping file..')
            zip = zipfile.ZipFile(filename, 'r')
            zip.extractall(dest)
            zip.close()

            print('Cleaning up..')
            os.remove(filename)
            print('Successful installed ngrok.')

            self.configure(dest)

        def get_authtoken(self):
            """Check ngrok authtoken.
            
            :return authtoken
            """
            authtoken = Config.get('ngrok', 'authtoken')
            if authtoken == "":
                authtoken = input(
                    'Please enter your authtoken (https://dashboard.ngrok.com/user/signup): ')
            
            installed = os.path.join(Ngrok.NGROK_ROOT, 'installed.success')
            with open(installed, 'w') as installed_file:
                installed_file.write('Goldphish ngrok installer @ {}\nngrok successful installed with authtoken: {}'.format(
                    time.asctime(), authtoken
                ))
            return authtoken

        def configure(self, dest):
            """Configure ngrok.

            :param dest:
            :return:
            """
            print('Configuring ngrok..')

            file = 'ngrok'
            if os.name == 'posix':
                executable = os.path.join(dest, file)
                os.chmod(executable, 777)
                authtoken = self.get_authtoken()
                subprocess.call(['sudo', executable, 'authtoken', authtoken], stdout=subprocess.DEVNULL)
            else:
                file = 'ngrok.exe'
                executable = os.path.join(dest, file)
                authtoken = self.get_authtoken()
                subprocess.call(
                    [executable, 'authtoken', authtoken], stdout=subprocess.DEVNULL)

            if Ngrok.ngrok_is_installed():
                print('Done. You can now use goldphish with ngrok.\n')
            else:
                print('Something went wrong. Please install and configure ngrok manually.\n')

        def run(self):
            """Run the installer."""
            print('\nNgrok was not found. Installing it now..')
            
            is_64bit = sys.maxsize > 2 ** 32
            _system = system().lower()
            
            if _system == 'windows':
                if is_64bit:
                    self.download(Ngrok.Installer.NGROK_LINKS['windows']['64'])
                else:
                    self.download(Ngrok.Installer.NGROK_LINKS['windows']['32'])
            elif _system.startswith('linux'):
                if is_64bit:
                    self.download(Ngrok.Installer.NGROK_LINKS['linux']['64'])
                else:
                    self.download(Ngrok.Installer.NGROK_LINKS['linux']['32'])
            elif _system == 'darwin':
                if is_64bit:
                    self.download(Ngrok.Installer.NGROK_LINKS['darwin']['64'])
                else:
                    self.download(Ngrok.Installer.NGROK_LINKS['darwin']['32'])
            elif _system == 'freebsd':
                if is_64bit:
                    self.download(Ngrok.Installer.NGROK_LINKS['freebsd']['64'])
                else:
                    self.download(Ngrok.Installer.NGROK_LINKS['freebsd']['32'])

            time.sleep(2)
            clear()

    @staticmethod
    def ngrok_is_installed():
        """Check ngrok installation.
        
        :return bool
        """
        path = Ngrok.NGROK_ROOT
        if os.path.exists(os.path.join(path, 'installed.success')):
            return True
        else:
            return False

    @staticmethod
    def get_public_url():
        """Return tunnels public url.
        
        :return public_url
        """
        try:
            with urlopen("http://localhost:4040/api/tunnels") as conn:
                api_data = json.loads(conn.read().decode('utf-8'))
                
            tunnels = api_data['tunnels']
            ngrok_public_url = None
            
            for tunnel in tunnels:
                if tunnel['proto'] != 'https':
                    continue
                ngrok_public_url = tunnel['public_url']
            assert ngrok_public_url is not None
            return ngrok_public_url
        except Exception as e:
            print("{}\nCould not find ngrok public url. "
                  "Please manually run `ngrok http $PORT.".format(e))

    @staticmethod
    def start(port):
        """Start ngrok client.

        :param port:
        :return public_url
        """
        file = 'ngrok'
        if os.name == 'posix':
            executable = os.path.join(Ngrok.NGROK_ROOT, file)
            subprocess.Popen(['sudo', executable, 'http', str(port)], stdout=subprocess.PIPE, stderr=subprocess.STDOUT)

            return Ngrok.get_public_url()
        else:
            file = 'ngrok.exe'
            executable = os.path.join(Ngrok.NGROK_ROOT, file)
            subprocess.Popen([executable, 'http', str(port)], stdout=subprocess.PIPE, stderr=subprocess.STDOUT)

            return Ngrok.get_public_url()
