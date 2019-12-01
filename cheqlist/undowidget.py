# -*- encoding: utf-8 -*-
# Cheqlist v0.3.2
# A simple Qt checklist.
# Copyright © 2015-2019, Chris Warrick.
# See /LICENSE for licensing information.

"""
The Cheqlist app.

:Copyright: © 2015-2019, Chris Warrick.
:License: BSD (see /LICENSE).
"""

try:
    from PySide2 import QtWidgets
except ImportError:
    from PyQt5 import QtWidgets

__all__ = ('UndoWidget',)


class UndoWidget(QtWidgets.QUndoView):
    """Undo view with checkbox setting."""

    _mw = None

    def showEvent(self, event):
        """Check the action associated with this window."""
        self._mw.actionShowUndoWindow.setChecked(True)

    def hideEvent(self, event):
        """Uncheck the action associated with this window."""
        self._mw.actionShowUndoWindow.setChecked(False)
