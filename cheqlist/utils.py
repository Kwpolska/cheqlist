
# -*- encoding: utf-8 -*-
# Cheqlist v0.3.0
# A simple Qt checklist.
# Copyright © 2015-2016, Chris Warrick.
# See /LICENSE for licensing information.

"""
Utilties, mainly for parsing and file support.

:Copyright: © 2015-2016, Chris Warrick.
:License: BSD (see /LICENSE).
"""

import cheqlist
import re

SERIALIZE_FSTR = ' - [{x}] {markers}{text}{end_markers}\n'
zwnj = '\u200C'

RE_X = re.compile(r'\[([ *xX])\] ?(.*)')
RE_FMT = re.compile(r'^((?:\*|_|~~|<u>)*)(.*?)((?:\*|_|~~|</u>)*)$')
RE_BOLD = re.compile(r'(\*\*|__)(.*?)\1')
RE_ITALIC = re.compile(r'(\*|_)(.*?)\1')
RE_UNDERLINE = re.compile(r'(<u>)(.*?)(</u>)')
RE_STRIKEOUT = re.compile(r'(~~)(.*?)(~~)')


def _re_match(regex, line):
    """Match a regular expression and substitute it."""
    out = regex.sub(r'\2', line)
    return line != out, out


def parse_lines(lines):
    """Parse lines into entries."""
    for lineO in lines:
        line = lineO.strip()
        if line.startswith(('- ', '* ')):
            line = line[2:].strip()
        match = RE_X.match(line)
        if match:
            checked_text, line = match.groups()
            checked = checked_text != ' '
        else:
            checked = False

        bold = False
        italic = False
        underline = False
        strikeOut = False
        match = RE_FMT.match(line)
        if match:
            fmt_start, line, fmt_end = match.groups()
            fmt = fmt_start + 'f' + fmt_end
            bold, fmt = _re_match(RE_BOLD, fmt)
            italic, fmt = _re_match(RE_ITALIC, fmt)
            underline, fmt = _re_match(RE_UNDERLINE, fmt)
            strikeOut, fmt = _re_match(RE_STRIKEOUT, fmt)

            if fmt != 'f':
                cheqlist.log.warn(
                    "Failed to parse formats: %r left over from %r (%r; %d%d%d%d)",
                    fmt, lineO, line, bold, italic, underline, strikeOut)

            # Remove ZWNJ (see below)
            if line[0] == zwnj:
                line = line[1:-1]
            line = line.strip()

        yield (line, checked, bold, italic, underline, strikeOut)


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
            text = zwnj + text + zwnj
        yield SERIALIZE_FSTR.format(x=x, markers=markers,
                                    end_markers=end_markers, text=text)
        done += 1
    if log:
        cheqlist.log.info("{0} tasks serialized".format(done))


def config_bool(value):
    """Represent a boolean in a way compatible with configparser."""
    return "true" if value else "false"
