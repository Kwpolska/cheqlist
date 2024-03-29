# -*- encoding: utf-8 -*-
# Cheqlist v0.3.2
# A simple Qt checklist.
# Copyright © 2015-2023, Chris Warrick.
# All rights reserved.
#
# Redistribution and use in source and binary forms, with or without
# modification, are permitted provided that the following conditions are
# met:
#
# 1. Redistributions of source code must retain the above copyright
#    notice, this list of conditions, and the following disclaimer.
#
# 2. Redistributions in binary form must reproduce the above copyright
#    notice, this list of conditions, and the following disclaimer in the
#    documentation and/or other materials provided with the distribution.
#
# 3. Neither the name of the author of this software nor the names of
#    contributors to this software may be used to endorse or promote
#    products derived from this software without specific prior written
#    consent.
#
# THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS
# "AS IS" AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT
# LIMITED TO, THE IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR
# A PARTICULAR PURPOSE ARE DISCLAIMED.  IN NO EVENT SHALL THE COPYRIGHT
# OWNER OR CONTRIBUTORS BE LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL,
# SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT
# LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES; LOSS OF USE,
# DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND ON ANY
# THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT
# (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE
# OF THIS SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.

"""
A simple Qt checklist.

:Copyright: © 2015-2023, Chris Warrick.
:License: BSD (see /LICENSE).
"""

import os
import sys
import pkg_resources
import io
import logging
import time
from cheqlist import appdirs
try:
    import configparser
except ImportError:
    import ConfigParser as configparser

__title__ = 'Cheqlist'
__version__ = '0.3.2'
__author__ = 'Chris Warrick'
__license__ = '3-clause BSD'
__docformat__ = 'restructuredtext en'

__all__ = ()

# Time
_starttime = time.time()

# import gettext
# G = gettext.translation('Cheqlist', '/usr/share/locale', fallback='C')
# _ = G.gettext

# Config directory setup
if sys.platform == 'darwin':
    confdir = os.path.expanduser('~/Library/Application Support/Cheqlist')
else:
    if sys.platform == 'win32':
        confhome = os.path.normpath(appdirs._get_win_folder("CSIDL_LOCAL_APPDATA"))
    else:
        confhome = os.getenv('XDG_CONFIG_HOME') or os.path.expanduser('~/.config/')

    kwdir = os.path.join(confhome, 'kwpolska')
    confdir = os.path.join(kwdir, 'cheqlist')

    for d in (confhome, kwdir):
        if not os.path.exists(d):
            os.mkdir(d)

if not os.path.exists(confdir):
    os.mkdir(confdir)

confpath = os.path.join(confdir, 'cheqlist.ini')
logpath = os.path.join(confdir, 'cheqlist.log')

# Logging configuration
logging.basicConfig(format='%(asctime)-15s [%(levelname)-7s] '
                    ':%(name)-10s: %(message)s',
                    filename=logpath,
                    level=logging.DEBUG)
log = logging.getLogger('cheqlist')
console = logging.StreamHandler()
console.setLevel(logging.INFO)
console.setFormatter(logging.Formatter('[%(levelname)-7s] '
                     ':%(name)-10s: %(message)s'))
logging.getLogger('').addHandler(console)
log.info('*** Cheqlist v' + __version__)


if not os.path.exists(confpath):
    log.warn("cheqlist.ini does not exist, creating")
    with open(confpath, 'wb') as fh:
        fh.write(pkg_resources.resource_string(
            'cheqlist', 'data/cheqlist.ini.skel'))

# Configuration file support
config = configparser.ConfigParser()
config.read_string(pkg_resources.resource_string(
            'cheqlist', 'data/cheqlist.ini.skel').decode('utf-8'))
config.read([confpath], encoding='utf-8')
log.info("Read config from cheqlist.ini")


def config_write():
    with io.open(confpath, 'w', encoding='utf-8') as fh:
        config.write(fh)
    log.info("Config written to cheqlist.ini")
