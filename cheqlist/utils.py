
# -*- encoding: utf-8 -*-
# Cheqlist v0.1.6
# A simple Qt checklist.
# Copyright © 2015-2016, Chris Warrick.
# See /LICENSE for licensing information.

"""
Utilties, mainly for parsing and file support.

:Copyright: © 2015-2016, Chris Warrick.
:License: BSD (see /LICENSE).
"""

import cheqlist

SERIALIZE_FSTR = ' - [{x}] {asterisks}{text}{asterisks}\n'

def parse_lines(lines):
    """Parse lines into entries."""
    for line in lines:
        line = line.strip()
        if line.startswith(('- ', '* ')):
            line = line[2:].strip()
        if line.startswith('['):
            checked = line[1] in ('x', 'X', '*')
            line = line[3:].strip()
        else:
            checked = False
        bold = False
        italic = False
        if line.startswith(('_**', '*__')):
            # mixed styles
            bold = True
            italic = True
            line = line[3:-3].strip()
        if line.startswith(('**', '__')):
            bold = True
            line = line[2:-2].strip()
        if line.startswith(('*', '_')):
            italic = True
            line = line[1:-1].strip()
        yield (line, checked, bold, italic)


def serialize_qt(items, log=True):
    """Serialize a Qt item list into GitHub Flavored Markdown."""
    done = 0
    for i in items:
        asterisks = ''
        x = 'x' if i.checkState() else ' '
        f = i.font()
        if f.bold():
            asterisks += '**'
        if f.italic():
            asterisks += '*'
        yield SERIALIZE_FSTR.format(x=x, asterisks=asterisks, text=i.text())
        done += 1
    if log:
        cheqlist.log.info("{0} tasks serialized".format(done))
