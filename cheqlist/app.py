# -*- encoding: utf-8 -*-
# Cheqlist v0.1.3
# A simple Qt checklist.
# Copyright © 2015, Chris Warrick.
# See /LICENSE for licensing information.

"""
The Cheqlist app.

:Copyright: © 2015, Chris Warrick.
:License: BSD (see /LICENSE).
"""

import os
import io
import time
import cheqlist
from PyQt5 import QtCore, QtGui, QtWidgets

__all__ = ('Main',)


class Main(QtWidgets.QMainWindow):

    """The main window of the app."""

    def __init__(self, app):
        """Create the GUI."""
        super(Main, self).__init__()
        self.app = app
        self.setWindowIcon(QtGui.QIcon.fromTheme("checkbox"))
        self.centralwidget = QtWidgets.QWidget(self)
        self.verticalLayout = QtWidgets.QVBoxLayout(self.centralwidget)
        self.tasklist = QtWidgets.QListWidget(self.centralwidget)
        self.tasklist.setDragDropMode(QtWidgets.QAbstractItemView.DragDrop)
        self.tasklist.setDefaultDropAction(QtCore.Qt.MoveAction)

        self.verticalLayout.addWidget(self.tasklist)
        self.progressBar = QtWidgets.QProgressBar(self.centralwidget)
        self.progressBar.setTextVisible(True)
        self.progressBar.setFormat("%v/%m (%p%)")
        self.updateProgressBar()
        self.verticalLayout.addWidget(self.progressBar)
        self.setCentralWidget(self.centralwidget)
        self.toolBar = QtWidgets.QToolBar("Main", self)
        self.toolBar.setIconSize(QtCore.QSize(16, 16))
        self.toolBar.setMovable(False)
        self.addToolBar(QtCore.Qt.TopToolBarArea, self.toolBar)
        menu = self.menuBar()
        self.fileMenu = menu.addMenu("&File")
        self.editMenu = menu.addMenu("&Edit")
        # self.helpMenu = menu.addMenu("&Help")

        self.actionAdd = QtWidgets.QAction(
            QtGui.QIcon.fromTheme("list-add"), "&Add", self, shortcut='Ctrl+T',
            toolTip="Add", triggered=self.addItemHandler)

        self.actionEdit = QtWidgets.QAction(
            QtGui.QIcon.fromTheme("edit-rename"), "&Edit", self,
            shortcut='Ctrl+E', toolTip="Edit", triggered=self.editItemHandler)

        self.actionDelete = QtWidgets.QAction(
            QtGui.QIcon.fromTheme("list-remove"), "&Delete", self,
            shortcut='Delete', toolTip="Delete", triggered=self.delItemHandler)

        self.actionBold = QtWidgets.QAction(
            QtGui.QIcon.fromTheme("format-text-bold"), "&Bold", self,
            shortcut='Ctrl+B', toolTip="Bold", checkable=True,
            triggered=self.boldItemHandler)

        self.actionItalic = QtWidgets.QAction(
            QtGui.QIcon.fromTheme("format-text-italic"), "&Italic", self,
            shortcut='Ctrl+I', toolTip="Italic", checkable=True,
            triggered=self.italicItemHandler)

        self.actionOpen = QtWidgets.QAction(
            QtGui.QIcon.fromTheme("document-open"), "&Open", self,
            shortcut='Ctrl+O', toolTip="Open", triggered=self.openHandler)

        self.actionSave = QtWidgets.QAction(
            QtGui.QIcon.fromTheme("document-save"), "&Save", self,
            shortcut='Ctrl+S', toolTip="Save", triggered=self.saveHandler)

        self.actionClear = QtWidgets.QAction(
            QtGui.QIcon.fromTheme("edit-clear-list"), "Clea&r", self,
            shortcut='Ctrl+R', toolTip="Clear", triggered=self.clear)

        self.actionQuit = QtWidgets.QAction(
            QtGui.QIcon.fromTheme("application-exit"), "&Quit", self,
            shortcut='Ctrl+Q', toolTip="Quit", triggered=self.quit)

        self.actionCheckAll = QtWidgets.QAction(
            "Check &All", self, toolTip="Check all items in the list.",
            triggered=self.checkAll)

        self.actionCheckNone = QtWidgets.QAction(
            "&Uncheck All", self, toolTip="Uncheck all items in the list.",
            triggered=self.checkNone)

        self.actionCheckInvert = QtWidgets.QAction(
            "In&vert Selection", self, toolTip="Check all unchecked items "
            "and uncheck all checked items.", triggered=self.checkInvert)

        self.toolBar.addAction(self.actionAdd)
        self.toolBar.addAction(self.actionDelete)
        self.toolBar.addSeparator()
        self.toolBar.addAction(self.actionBold)
        self.toolBar.addAction(self.actionItalic)
        self.toolBar.addSeparator()
        self.toolBar.addAction(self.actionOpen)
        self.toolBar.addAction(self.actionSave)
        self.toolBar.addAction(self.actionClear)

        self.fileMenu.addAction(self.actionOpen)
        self.fileMenu.addAction(self.actionSave)
        self.fileMenu.addSeparator()
        self.fileMenu.addAction(self.actionQuit)

        self.editMenu.addAction(self.actionAdd)
        self.editMenu.addAction(self.actionEdit)
        self.editMenu.addAction(self.actionDelete)
        self.editMenu.addAction(self.actionClear)
        self.editMenu.addSeparator()
        self.editMenu.addAction(self.actionBold)
        self.editMenu.addAction(self.actionItalic)
        self.editMenu.addSeparator()
        self.editMenu.addAction(self.actionCheckAll)
        self.editMenu.addAction(self.actionCheckNone)
        self.editMenu.addAction(self.actionCheckInvert)

        self.tasklist.itemChanged.connect(self.updateUI)
        self.tasklist.itemSelectionChanged.connect(self.selectionHandler)

        # sample items
        self.addItem("Item 1")
        self.addItem("Item 2")

        self.setWindowTitle("Cheqlist")
        self.resize(220, 1000)
        # self.setWindowOpacity(0.85)
        # self.setWindowFlags(QtCore.Qt.FramelessWindowHint)

        QtCore.QMetaObject.connectSlotsByName(self)
        self.show()
        cheqlist.log.info("Startup finished in {0:0.2f} s".format(
                          time.time() - cheqlist._starttime))

    # Item handling
    def items(self):
        """Yield items in the task list."""
        for n in range(0, self.tasklist.count()):
            yield self.tasklist.item(n)

    def clear(self, event=None):
        """Clear the task list."""
        self.tasklist.clear()
        cheqlist.log.info("List cleared")
        self.updateUI()

    def addItem(self, text="New item", edit=False, checked=False, bold=False,
                italic=False):
        """Add an item to the task list."""
        item = QtWidgets.QListWidgetItem(text, self.tasklist)
        item.setFlags(QtCore.Qt.ItemIsSelectable |
                      QtCore.Qt.ItemIsEditable |
                      QtCore.Qt.ItemIsDragEnabled |
                      QtCore.Qt.ItemIsDropEnabled |
                      QtCore.Qt.ItemIsUserCheckable |
                      QtCore.Qt.ItemIsEnabled)
        if checked:
            item.setCheckState(QtCore.Qt.Checked)
        else:
            item.setCheckState(QtCore.Qt.Unchecked)
        self.tasklist.addItem(item)
        f = item.font()
        if bold:
            f.setBold(True)
        if italic:
            f.setItalic(True)
        item.setFont(f)
        if edit:
            item.setSelected(True)
            self.tasklist.editItem(item)
        self.updateUI()
        return self.tasklist.row(item)

    # File handling
    def serialize(self):
        """Serialize a list into GitHub Flavored Markdown."""
        fstr = ' - [{x}] {asterisks}{text}{asterisks}\n'
        for i in self.items():
            asterisks = ''
            x = 'x' if i.checkState() else ' '
            f = i.font()
            if f.bold():
                asterisks += '**'
            if f.italic():
                asterisks += '*'
            yield fstr.format(x=x, asterisks=asterisks, text=i.text())
        cheqlist.log.info("{0} tasks serialized".format(len(i)))

    def loadFromText(self, items):
        """Load items from a text file."""
        for i in items:
            i = i.strip()
            if i.startswith(('- ', '* ')):
                i = i[2:].strip()
            if i.startswith('['):
                checked = i[1] in ('x', 'X', '*')
                i = i[3:].strip()
            else:
                checked = False
            bold = False
            italic = False
            if i.startswith(('_**', '*__')):
                # mixed styles
                bold = True
                italic = True
                i = i[3:-3].strip()
            if i.startswith(('**', '__')):
                bold = True
                i = i[2:-2].strip()
            if i.startswith(('*', '_')):
                italic = True
                i = i[1:-1].strip()
            self.addItem(i, False, checked, bold, italic)

        cheqlist.log.info("{0} tasks loaded".format(len(i)))

    # Action handling
    def addItemHandler(self, event):
        """Add an empty item."""
        self.addItem('', True)

    def editItemHandler(self, event):
        """Edit the currently selected item."""
        for i in self.tasklist.selectedItems():
            self.tasklist.editItem(i)

    def delItemHandler(self, event):
        """Delete the currently selected item."""
        for i in self.tasklist.selectedItems():
            self.tasklist.takeItem(self.tasklist.row(i))
        self.updateUI()

    def updateProgressBar(self):
        """Update progress bar."""
        count = self.tasklist.count()
        value = 0
        for i in self.items():
            if i.checkState():
                value += 1
        self.progressBar.setMaximum(count)
        self.progressBar.setValue(value)

    def boldItemHandler(self, event):
        """Toggle bold on an item."""
        for i in self.tasklist.selectedItems():
            f = i.font()
            f.setBold(not f.bold())
            i.setFont(f)

    def italicItemHandler(self, event):
        """Toggle italic on an item."""
        for i in self.tasklist.selectedItems():
            f = i.font()
            f.setItalic(not f.italic())
            i.setFont(f)

    def openHandler(self, event):
        """Open a file."""
        openmode = cheqlist.config.get('directories', 'open_from')
        lastdir = cheqlist.config.get('directories', 'lastdir')
        path = os.path.expanduser(cheqlist.config.get('directories', openmode))
        fname, _ = QtWidgets.QFileDialog.getOpenFileName(
            self, "Open", path,
            "Markdown checklist files (*.cheqlist *.checklist *.md "
            "*.mdown *.markdown)")

        if not fname:
            return

        newpath = os.path.dirname(fname)
        if newpath == lastdir:
            cheqlist.config.set('directories', 'lastdir', newpath)
            cheqlist.config_write()

        cheqlist.log.info("Opening file " + fname)

        with io.open(fname, 'r', encoding='utf-8') as fh:
            self.clear()
            self.loadFromText(fh.readlines())

    def saveHandler(self, event):
        """Save a file."""
        fname, _ = QtWidgets.QFileDialog.getSaveFileName(
            self, "Save", os.path.expanduser('~'),
            "Markdown checklist files (*.cheqlist *.checklist *.md "
            "*.mdown *.markdown)")

        if not fname:
            return

        cheqlist.log.info("Saving to file " + fname)

        with io.open(fname, 'w', encoding='utf-8') as fh:
            fh.writelines(self.serialize())

    def quit(self, event=None):
        """Display a message on quit via Ctrl+Q."""
        cheqlist.log.info("*** Goodbye!")
        QtWidgets.qApp.quit()

    def closeEvent(self, event=None):
        """Display a message on quit via the X button."""
        cheqlist.log.info("*** Goodbye!")
        super(Main, self).closeEvent(event)
        QtWidgets.qApp.quit()

    def checkAll(self, event=None):
        """Check all items (complete the list)."""
        for item in self.items():
            item.setCheckState(2)
        self.updateUI()

    def checkNone(self, event=None):
        """Uncheck all items (reset the list)."""
        for item in self.items():
            item.setCheckState(0)

    def checkInvert(self, event=None):
        """Check all unchecked items, uncheck all checked items."""
        for item in self.items():
            if item.checkState() == 2:
                item.setCheckState(0)
            else:
                item.setCheckState(2)
        self.updateUI()

    # UI functions and helpers
    def updateBoldAction(self):
        """Set the bold action check status."""
        s = False
        for i in self.tasklist.selectedItems():
            s = i.font().bold()

        self.actionBold.setChecked(s)

    def updateItalicAction(self):
        """Set the italic action check status."""
        s = False
        for i in self.tasklist.selectedItems():
            s = i.font().italic()

        self.actionItalic.setChecked(s)

    def updateDisabledButtons(self):
        """Disable buttons if the list is empty."""
        if self.tasklist.count() == 0:
            self.actionDelete.setEnabled(False)
            self.actionBold.setEnabled(False)
            self.actionBold.setChecked(False)
            self.actionItalic.setEnabled(False)
            self.actionItalic.setChecked(False)
            self.progressBar.setEnabled(False)
        else:
            self.actionDelete.setEnabled(True)
            self.actionBold.setEnabled(True)
            self.actionItalic.setEnabled(True)
            self.progressBar.setEnabled(True)

    def updateUI(self):
        """Update all UI."""
        self.updateProgressBar()
        self.updateBoldAction()
        self.updateItalicAction()
        self.updateDisabledButtons()

    def selectionHandler(self):
        """Update actions when the selection changes."""
        self.updateBoldAction()
        self.updateItalicAction()
