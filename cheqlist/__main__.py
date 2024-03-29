# -*- encoding: utf-8 -*-
# Cheqlist v0.3.2
# A simple Qt checklist.
# Copyright © 2015-2023, Chris Warrick.
# See /LICENSE for licensing information.

"""
Run the app.

:Copyright: © 2015-2023, Chris Warrick.
:License: BSD (see /LICENSE).
"""

from cheqlist import log, logpath
from cheqlist.app import QtWidgets, Main
import sys
import traceback

__all__ = ('main',)


def main():
    """The main routine for the UI."""
    try:
        app = QtWidgets.QApplication(sys.argv)
        app.setApplicationName("Cheqlist")
        main = Main(app)  # NOQA
        sys.exit(app.exec_())
    except Exception as e:
        log.exception(e)
        # tb ends with newline
        tb = ''.join(traceback.format_exception_only(type(e), e))
        QtWidgets.QMessageBox.critical(
            None, "Cheqlist", "An exception occurred:\n\n{0}\n"
            "Please report a bug in Cheqlist and attach recent log entries.\n"
            "The log is stored in {1}".format(tb, logpath))
        sys.exit(1)

if __name__ == '__main__':
    main()
