# -*- encoding: utf-8 -*-
# Cheqlist v0.3.0
# A simple Qt checklist.
# Copyright © 2015-2016, Chris Warrick.
# See /LICENSE for licensing information.

"""
Undo commands for Cheqlist.

:Copyright: © 2015-2016, Chris Warrick.
:License: BSD (see /LICENSE).
"""

from PyQt5.QtWidgets import QUndoCommand
from PyQt5 import QtCore

__all__ = ('CommandAdd', 'CommandDelete', 'CommandClear', 'CommandCheck',
           'CommandUnCheck', 'CommandBold', 'CommandUnBold', 'CommandItalic',
           'CommandUnItalic', 'CommandUnderline', 'CommandUnUnderline',
           'CommandStrikeOut', 'CommandUnStrikeOut')


class CheqlistUndoCommand(QUndoCommand):
    """Generic Undo command."""

    prefix = ""

    def __init__(self, item, window):
        """Create the action."""
        self.item = item
        self.window = window
        self.desc = ' '.join((self.prefix, item.text()))
        super(CheqlistUndoCommand, self).__init__(self.desc)


class CommandAdd(CheqlistUndoCommand):
    """Add a task."""

    prefix = "Add"

    def undo(self):
        """Undo the command."""
        self.window.tasklist.takeItem(self.window.tasklist.row(self.item))
        del self.window.lastText[id(self.item)]

    def redo(self):
        """Redo the command."""
        self.window.tasklist.addItem(self.item)
        self.window.lastText[id(self.item)] = self.item.text()


class CommandDelete(CheqlistUndoCommand):
    """Delete a task."""

    prefix = "Delete"

    def undo(self):
        """Undo the command."""
        self.window.tasklist.addItem(self.item)
        self.window.lastText[id(self.item)] = self.item.text()

    def redo(self):
        """Redo the command."""
        self.window.tasklist.takeItem(self.window.tasklist.row(self.item))
        del self.window.lastText[id(self.item)]


class CommandClear(QUndoCommand):
    """Clear the list."""

    desc = "Clear"

    def __init__(self, window):
        """Create the action."""
        self.window = window
        self.items = list(self.window.items())
        super(CommandClear, self).__init__(self.desc)

    def undo(self):
        """Undo the command."""
        for i in self.items:
            self.window.tasklist.addItem(i)

    def redo(self):
        """Redo the command."""
        for i in self.items:
            self.window.tasklist.takeItem(self.window.tasklist.row(i))


class CommandEdit(QUndoCommand):
    """Edit a task."""

    prefix = "Edit"

    def __init__(self, item, window, oldText, newText):
        """Create the action."""
        self.item = item
        self.window = window
        self.desc = ' '.join((self.prefix, newText))
        self.oldText = oldText
        self.newText = newText
        super(QUndoCommand, self).__init__(self.desc)

    def undo(self):
        """Undo the command."""
        self.window.lastText[id(self.item)] = self.oldText
        self.item.setText(self.oldText)

    def redo(self):
        """Redo the command."""
        self.window.lastText[id(self.item)] = self.newText
        self.item.setText(self.newText)


class CommandCheck(CheqlistUndoCommand):
    """Mark a task done."""

    prefix = "Check"
    undoValue = QtCore.Qt.Unchecked
    redoValue = QtCore.Qt.Checked

    def undo(self):
        """Undo the command."""
        self.window.lastState[id(self.item)] = self.undoValue
        self.item.setCheckState(self.undoValue)

    def redo(self):
        """Redo the command."""
        self.window.lastState[id(self.item)] = self.redoValue
        self.item.setCheckState(self.redoValue)


class CommandUnCheck(CommandCheck):
    """Mark a task undone."""

    prefix = "Uncheck"
    undoValue = QtCore.Qt.Checked
    redoValue = QtCore.Qt.Unchecked


class CommandFormat(CheqlistUndoCommand):
    """Generic formatting command (base class)."""

    undoValue = False
    functionName = ""

    def _changeFont(self, value):
        """Change the font to the desired formatting."""
        f = self.item.font()
        getattr(f, self.functionName)(value)
        self.item.setFont(f)

    def undo(self):
        """Undo the command."""
        self._changeFont(self.undoValue)

    def redo(self):
        """Redo the command."""
        self._changeFont(not self.undoValue)


class CommandBold(CommandFormat):
    """Make something bold."""

    prefix = "Bold"
    functionName = "setBold"


class CommandUnBold(CommandFormat):
    """Make something not bold."""

    prefix = "Remove Bold"
    functionName = "setBold"
    undoValue = True


class CommandItalic(CommandFormat):
    """Make something italic."""

    prefix = "Italicize"
    functionName = "setItalic"


class CommandUnItalic(CommandFormat):
    """Make something not italic."""

    prefix = "Deitalicize"
    functionName = "setItalic"
    undoValue = True


class CommandUnderline(CommandFormat):
    """Make something underlined."""

    prefix = "Underline"
    functionName = "setUnderline"


class CommandUnUnderline(CommandFormat):
    """Make something not underlined."""

    prefix = "Remove Underline"
    functionName = "setUnderline"
    undoValue = True


class CommandStrikeOut(CommandFormat):
    """Make something struck out."""

    prefix = "Strike Out"
    functionName = "setStrikeOut"

    def undo(self):
        """Undo the command."""
        self._changeFont(self.undoValue)
        if self.window.ignoreStruckOut:
            self.window.updateProgressBar()

    def redo(self):
        """Redo the command."""
        self._changeFont(not self.undoValue)
        if self.window.ignoreStruckOut:
            self.window.updateProgressBar()


class CommandUnStrikeOut(CommandStrikeOut):
    """Make something not struck out."""

    prefix = "Remove Strike Out"
    undoValue = True


class CommandPatternCheck(QUndoCommand):
    """Generic Check Pattern command."""

    desc = ""
    pattern = None

    def __init__(self, window):
        """Create the action."""
        self.window = window
        self.items = {}
        for i in self.window.items():
            self.items[id(i)] = i.checkState()
        super(CommandPatternCheck, self).__init__(self.desc)

    def undo(self):
        """Undo the command."""
        self.window.updateUI_disable()
        for i in self.window.items():
            self.window.lastState[id(i)] = self.items[id(i)]
            i.setCheckState(self.items[id(i)])
        self.window.updateUI_enable()

    def redo(self):
        """Redo the command."""
        self.window.updateUI_disable()
        for i in self.window.items():
            self.window.lastState[id(i)] = self.pattern
            i.setCheckState(self.pattern)
        self.window.updateUI_enable()


class CommandCheckAll(CommandPatternCheck):
    """Check all items."""

    pattern = QtCore.Qt.Checked
    desc = "Check All"


class CommandCheckNone(CommandPatternCheck):
    """Uncheck all items."""

    pattern = QtCore.Qt.Unchecked
    desc = "Uncheck All"


class CommandCheckInvert(CommandPatternCheck):
    """Check all items."""

    desc = "Invert Selection"

    def redo(self):
        """Redo the command."""
        self.window.updateUI_disable()
        for i in self.window.items():
            if self.items[id(i)] == QtCore.Qt.Checked:
                ns = QtCore.Qt.Unchecked
            else:
                ns = QtCore.Qt.Checked
            self.window.lastState[id(i)] = ns
            i.setCheckState(ns)
        self.window.updateUI_enable()
