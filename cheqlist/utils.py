
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

SERIALIZE_FSTR = ' - [{x}] {markers}{text}{end_markers}\n'
zwnj = '\u200C'

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
        underline = False
        strikethrough = False
        if line.startswith('<u>'):
            underline = True
            line = line[3:-4].strip()
        if line.startswith('~~'):
            strikethrough = True
            line = line[2:-2].strip()
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

        # Remove ZWNJ (see below)
        if line[0] == zwnj:
            line = line[1:].strip()

        yield (line, checked, bold, italic, underline, strikethrough)


def serialize_qt(items, log=True):
    """Serialize a Qt item list into GitHub Flavored Markdown."""
    done = 0
    for i in items:
        markers = ''
        x = 'x' if i.checkState() else ' '
        f = i.font()
        if f.bold():
            markers += '**'
        if f.italic():
            markers += '*'

        end_markers = markers

        if f.strikeOut():
            markers = '~~' + markers
            end_markers += '~~'
        if f.underline():
            markers = '<u>' + markers
            end_markers += '</u>'

        # Add ZWNJ to preserve non-markup text characters
        text = i.text()
        if text.startswith(('*', '~~', '<u>', '_')):
            text = zwnj + text
        yield SERIALIZE_FSTR.format(x=x, markers=markers, end_markers=end_markers, text=text)
        done += 1
    if log:
        cheqlist.log.info("{0} tasks serialized".format(done))