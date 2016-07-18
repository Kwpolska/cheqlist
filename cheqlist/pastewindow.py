# -*- encoding: utf-8 -*-
# Cheqlist v0.3.0
# A simple Qt checklist.
# Copyright © 2015-2016, Chris Warrick.
# See /LICENSE for licensing information.

"""
The Cheqlist app.

:Copyright: © 2015-2016, Chris Warrick.
:License: BSD (see /LICENSE).
"""

from PyQt5 import QtCore, QtGui, QtWidgets

__all__ = ('PasteWindow',)


class PasteWindow(QtWidgets.QDialog):
    """A simple window to paste items."""

    _mw = None

    def __init__(self, main):
        """Create main window."""
        super(PasteWindow, self).__init__()
        self._mw = main

        self.gridLayout = QtWidgets.QGridLayout(self)
        self.pasteButton = QtWidgets.QPushButton(
            QtGui.QIcon.fromTheme("edit-paste"), "&Paste", self)
        self.clearButton = QtWidgets.QPushButton(
            QtGui.QIcon.fromTheme("edit-clear"), "&Clear", self)
        self.textBox = QtWidgets.QPlainTextEdit(self)
        self.label = QtWidgets.QLabel(
            "Every line below will be added to the list.\n"
            "GitHub Flavored Markdown is supported for basic markup "
            "(done status, <b>**bold**</b>, <i>*italic*</i>, "
            "<u>&lt;u&gt;underline&lt;/u&gt;</u>, <s>~~strikeout~~</s>).",
            self)
        self.label.setTextFormat(QtCore.Qt.RichText)
        self.label.setWordWrap(True)
        self.buttonBox = QtWidgets.QDialogButtonBox(self)
        self.buttonBox.setOrientation(QtCore.Qt.Horizontal)
        self.buttonBox.setStandardButtons(
            QtWidgets.QDialogButtonBox.Ok |
            QtWidgets.QDialogButtonBox.Cancel)

        self.pasteButton.clicked.connect(self.paste)
        self.clearButton.clicked.connect(self.clear)

        self.gridLayout.addWidget(self.label, 0, 0, 2, 3)
        self.gridLayout.addWidget(self.pasteButton, 0, 3, 1, 1)
        self.gridLayout.addWidget(self.clearButton, 1, 3, 1, 1)
        self.gridLayout.addWidget(self.textBox, 2, 0, 1, 4)
        self.gridLayout.addWidget(self.buttonBox, 3, 0, 1, 4)

        self.setWindowTitle("Paste into Cheqlist")
        self.setWindowIcon(QtGui.QIcon.fromTheme("edit-paste"))
        self.setModal(True)
        self.resize(400, 400)
        self.buttonBox.accepted.connect(self.accept)
        self.buttonBox.rejected.connect(self.reject)
        QtCore.QMetaObject.connectSlotsByName(self)

        # Get clipboard contents
        self.paste()

    def paste(self, event=None):
        """Paste clipboard contents into the textbox."""
        self.textBox.clear()
        self.textBox.paste()

    def clear(self, event=None):
        """Clear the textbox."""
        self.textBox.clear()
