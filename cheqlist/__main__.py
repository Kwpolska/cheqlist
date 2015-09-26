# -*- encoding: utf-8 -*-
# Cheqlist v0.1.4
# A simple Qt checklist.
# Copyright © 2015, Chris Warrick.
# See /LICENSE for licensing information.

"""
Run the app.

:Copyright: © 2015, Chris Warrick.
:License: BSD (see /LICENSE).
"""

from cheqlist.app import QtWidgets, Main
import sys

__all__ = ('main',)


def main():
    """The main routine for the UI."""
    # if '-h' in sys.argv or '--help' in sys.argv:
    app = QtWidgets.QApplication(sys.argv)
    main = Main(app)
    main  # because vim python-mode doesn't like NOQA
    sys.exit(app.exec_())

if __name__ == '__main__':
    main()
