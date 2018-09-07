#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Goldphish phishing server.
(c) 2018 Nico Duitsmann.
Licensed under GNU GPLv3.

Usage:
    goldphish <website> [options]

Arguments:
    website             The website to clone to.

Options:
    -h --help           Show this help and exit.
    -v --version        Show version and exit.

    -a <host>           Http server address.
    -p <port>           Http server port number.
    
    --ngrok             Use ngrok for local server tunneling.

    --config-restore    Restore config.ini to defaults.
    --no-banner         Dont print banner art.

By using goldphish u agree to the terms of use.
For more info read DISCLAIMER in the installation dir.
"""

import sys

if sys.version_info[0] < 3: sys.exit('Python2 is not supported in this version. Exiting.')

from goldphish.cli import Cli

if __name__ == '__main__':
    Cli(__doc__)
