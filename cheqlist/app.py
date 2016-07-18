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

import os
import sys
import io
import time
import cheqlist
from cheqlist import utils, undocommands
from cheqlist.undowidget import UndoWidget
from cheqlist.pastewindow import PasteWindow
from PyQt5 import QtCore, QtGui, QtWidgets

__all__ = ('Main',)


class Main(QtWidgets.QMainWindow):
    """The main window of the app."""

    def __init__(self, app):
        """Create the GUI."""
        super(Main, self).__init__()
        self.app = app
        self.filename = None
        self.filebasename = None
        self.lastText = {}
        self.lastState = {}
        self.ignoreStruckOut = cheqlist.config.getboolean(
            'settings', 'ignore_struck_out')
        self.undoStack = QtWidgets.QUndoStack(self)

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
        self.toolBar.setFloatable(False)
        self.toolBar.setAllowedAreas(QtCore.Qt.TopToolBarArea)
        self.addToolBar(QtCore.Qt.TopToolBarArea, self.toolBar)
        self.editToolBar = QtWidgets.QToolBar("Edit", self)
        self.editToolBar.setIconSize(QtCore.QSize(16, 16))
        self.editToolBar.setFloatable(False)
        self.editToolBar.setAllowedAreas(QtCore.Qt.TopToolBarArea)
        self.addToolBar(QtCore.Qt.TopToolBarArea, self.editToolBar)
        self.insertToolBarBreak(self.editToolBar)
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

        self.actionUnderline = QtWidgets.QAction(
            QtGui.QIcon.fromTheme("format-text-underline"), "&Underline", self,
            shortcut='Ctrl+U', toolTip="Underline", checkable=True,
            triggered=self.underlineItemHandler)

        self.actionStrikeOut = QtWidgets.QAction(
            QtGui.QIcon.fromTheme("format-text-strikethrough"), "&Strike Out",
            self, shortcut='Ctrl+Alt+S', toolTip="Strike Out", checkable=True,
            triggered=self.strikeOutItemHandler)

        self.actionOpen = QtWidgets.QAction(
            QtGui.QIcon.fromTheme("document-open"), "&Open…", self,
            shortcut='Ctrl+O', toolTip="Open", triggered=self.openHandler)

        self.actionSave = QtWidgets.QAction(
            QtGui.QIcon.fromTheme("document-save"), "&Save…", self,
            shortcut='Ctrl+S', toolTip="Save", triggered=self.saveHandler)

        self.actionSaveAs = QtWidgets.QAction(
            QtGui.QIcon.fromTheme("document-save-as"), "S&ave as…", self,
            shortcut='Ctrl+Shift+S', toolTip="Save as",
            triggered=self.saveAsHandler)

        self.actionClear = QtWidgets.QAction(
            QtGui.QIcon.fromTheme("edit-clear-list"), "Clea&r", self,
            shortcut='Ctrl+R', toolTip="Clear", triggered=self.clear)

        self.actionPasteItems = QtWidgets.QAction(
            QtGui.QIcon.fromTheme("edit-paste"), "&Paste items…", self,
            shortcut='Ctrl+V', toolTip="Paste items from clipboard",
            triggered=self.pasteItems)

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

        self.actionIgnoreStruckOut = QtWidgets.QAction(
            "I&gnore struck out tasks", self, toolTip="Ignore tasks that are "
            "struck out from counts", triggered=self.ignoreStruckOutHandler,
            checkable=True)

        self.actionUndo = self.undoStack.createUndoAction(self)
        self.actionUndo.setIcon(QtGui.QIcon.fromTheme("edit-undo"))
        self.actionUndo.setShortcut("Ctrl+Z")
        self.actionRedo = self.undoStack.createRedoAction(self)
        self.actionRedo.setIcon(QtGui.QIcon.fromTheme("edit-redo"))
        self.actionRedo.setShortcut("Ctrl+Y")

        self.actionShowUndoWindow = QtWidgets.QAction(
            "Show undo &window", self, toolTip="Show undo window with all "
            "operations performed", triggered=self.showUndoWindowHandler,
            checkable=True)

        self.toolBar.addAction(self.actionAdd)
        self.toolBar.addAction(self.actionDelete)
        self.toolBar.addSeparator()
        self.toolBar.addAction(self.actionOpen)
        self.toolBar.addAction(self.actionSave)
        self.toolBar.addAction(self.actionSaveAs)
        self.toolBar.addAction(self.actionClear)
        self.toolBar.addAction(self.actionQuit)

        self.editToolBar.addAction(self.actionBold)
        self.editToolBar.addAction(self.actionItalic)
        self.editToolBar.addAction(self.actionUnderline)
        self.editToolBar.addAction(self.actionStrikeOut)
        self.editToolBar.addSeparator()
        self.editToolBar.addAction(self.actionUndo)
        self.editToolBar.addAction(self.actionRedo)

        self.fileMenu.addAction(self.actionOpen)
        self.fileMenu.addAction(self.actionSave)
        self.fileMenu.addAction(self.actionSaveAs)
        self.fileMenu.addSeparator()
        self.fileMenu.addAction(self.actionQuit)

        self.editMenu.addAction(self.actionAdd)
        self.editMenu.addAction(self.actionEdit)
        self.editMenu.addAction(self.actionDelete)
        self.editMenu.addAction(self.actionClear)
        self.editMenu.addAction(self.actionPasteItems)
        self.editMenu.addSeparator()
        self.editMenu.addAction(self.actionBold)
        self.editMenu.addAction(self.actionItalic)
        self.editMenu.addAction(self.actionUnderline)
        self.editMenu.addAction(self.actionStrikeOut)
        self.editMenu.addSeparator()
        self.editMenu.addAction(self.actionUndo)
        self.editMenu.addAction(self.actionRedo)
        self.editMenu.addAction(self.actionShowUndoWindow)
        self.editMenu.addSeparator()
        self.editMenu.addAction(self.actionCheckAll)
        self.editMenu.addAction(self.actionCheckNone)
        self.editMenu.addAction(self.actionCheckInvert)
        self.editMenu.addSeparator()
        self.editMenu.addAction(self.actionIgnoreStruckOut)

        self.tasklist.itemChanged.connect(self.itemChangedHandler)
        self.tasklist.itemSelectionChanged.connect(self.selectionHandler)
        self.actionIgnoreStruckOut.setChecked(self.ignoreStruckOut)
        self.tasklist.setContextMenuPolicy(QtCore.Qt.CustomContextMenu)
        self.tasklist.customContextMenuRequested.connect(
            self.tasklistMenuHandler)

        self.undoWidget = UndoWidget(self.undoStack)
        self.undoWidget.setWindowTitle("Operations — Cheqlist")
        self.undoWidget._mw = self

        self.setWindowIcon(QtGui.QIcon.fromTheme("checkbox"))
        self.updateWindowTitle()
        self.resize(250, 1000)
        self.updateUI()

        for a in sys.argv[1:]:
            self.readFile(a, clear=False)

        QtCore.QMetaObject.connectSlotsByName(self)
        self.show()

        cheqlist.log.info("Startup finished in {0:0.2f} s".format(
                          time.time() - cheqlist._starttime))

    # Item handling
    def items(self):
        """Yield items in the task list."""
        for n in range(0, self.tasklist.count()):
            yield self.tasklist.item(n)

    def clear(self, event=None, undoable=True):
        """Clear the task list."""
        if undoable:
            self.undoStack.push(undocommands.CommandClear(self))
        else:
            self.tasklist.clear()
            self.undoStack.clear()
            self.lastText = {}
            self.lastState = {}
        cheqlist.log.info("List cleared")
        self.updateUI()

    def addItem(self, text="New item", edit=False, checked=False, bold=False,
                italic=False, underline=False, strikeOut=False, undoable=True):
        """Add an item to the task list."""
        item = QtWidgets.QListWidgetItem(text, self.tasklist)
        if not edit:
            self.lastText[id(item)] = text
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
        self.lastState[id(item)] = item.checkState()
        f = item.font()
        if bold:
            f.setBold(True)
        if italic:
            f.setItalic(True)
        if underline:
            f.setUnderline(True)
        if strikeOut:
            f.setStrikeOut(True)
        item.setFont(f)
        if edit:
            self.tasklist.addItem(item)
            item.setSelected(True)
            self.tasklist.editItem(item)
        elif undoable:
            self.undoStack.push(undocommands.CommandAdd(item, self))
        else:
            self.tasklist.addItem(item)
        self.updateUI()
        return self.tasklist.row(item)

    # File handling
    def loadFromText(self, items, undoable=False):
        """Load items from a text file."""
        self.updateUI_disable()
        for (item, checked, bold, italic, underline,
             strikeOut) in utils.parse_lines(items):
            self.addItem(item, False, checked, bold, italic, underline,
                         strikeOut, undoable)

        self.updateUI_enable()
        cheqlist.log.info("{0} tasks loaded".format(len(items)))

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
            self.undoStack.push(undocommands.CommandDelete(i, self))
        self.updateUI()

    def updateProgressBar(self):
        """Update progress bar."""
        done = 0
        count = self.tasklist.count()
        if self.ignoreStruckOut:
            for i in self.items():
                if i.font().strikeOut():
                    count -= 1
                elif i.checkState():
                    done += 1
        else:
            for i in self.items():
                if i.checkState():
                    done += 1
        self.progressBar.setMaximum(count)
        self.progressBar.setValue(done)

    def _formatItemHandler(self, attrName, commandName):
        for i in self.tasklist.selectedItems():
            if getattr(i.font(), attrName)():
                className = 'CommandUn' + commandName
            else:
                className = 'Command' + commandName
            self.undoStack.push(getattr(undocommands, className)(i, self))

    def boldItemHandler(self, event):
        """Toggle bold on an item."""
        self._formatItemHandler('bold', 'Bold')

    def italicItemHandler(self, event):
        """Toggle italic on an item."""
        self._formatItemHandler('italic', 'Italic')

    def underlineItemHandler(self, event):
        """Toggle underline on an item."""
        self._formatItemHandler('underline', 'Underline')

    def strikeOutItemHandler(self, event):
        """Toggle strike out on an item."""
        self._formatItemHandler('strikeOut', 'StrikeOut')

    def openHandler(self, event):
        """Open a file."""
        # Ask for unsaved changes first
        if not self.unsavedChanges():
            return

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
        if newpath != lastdir:
            cheqlist.config.set('directories', 'lastdir', newpath)
            cheqlist.config_write()

        self.readFile(fname)

    def readFile(self, fname, clear=True):
        """Read a file and load it."""
        cheqlist.log.info("Opening file " + fname)
        if clear:
            self.clear(undoable=False)
        with io.open(fname, 'r', encoding='utf-8') as fh:
            self.loadFromText(fh.readlines())
        self.filename = fname
        self.filebasename = os.path.basename(self.filename)
        self.updateWindowTitle()

    def saveHandler(self, event):
        """Save a file."""
        if self.filename:
            self.writeFile(self.filename)
        else:
            self.saveAsHandler(event)

    def saveAsHandler(self, event):
        """Save as a new file."""
        openmode = cheqlist.config.get('directories', 'open_from')
        lastdir = cheqlist.config.get('directories', 'lastdir')
        path = os.path.expanduser(cheqlist.config.get('directories', openmode))
        fname, _ = QtWidgets.QFileDialog.getSaveFileName(
            self, "Save", path,
            "Markdown checklist files (*.cheqlist *.checklist *.md "
            "*.mdown *.markdown)")

        if not fname:
            return

        newpath = os.path.dirname(fname)
        if newpath != lastdir:
            cheqlist.config.set('directories', 'lastdir', newpath)
            cheqlist.config_write()

        self.writeFile(fname)

    def writeFile(self, fname):
        """Serialize and write into a file."""
        cheqlist.log.info("Saving to file " + fname)
        with io.open(fname, 'w', encoding='utf-8') as fh:
            fh.writelines(utils.serialize_qt(self.items()))
        self.filename = fname
        self.filebasename = os.path.basename(fname)
        self.undoStack.clear()
        self.updateUI()

    def showUndoWindowHandler(self, event=None):
        """Show/hide the Undo window."""
        self.undoWidget.setVisible(not self.undoWidget.isVisible())

    def quit(self, event=None):
        """Display a message on quit via Ctrl+Q."""
        if self.unsavedChanges():
            cheqlist.log.info("*** Goodbye!")
            QtWidgets.qApp.quit()
        else:
            cheqlist.log.info("Aborted quit")

    def closeEvent(self, event=None):
        """Display a message on quit via the X button."""
        if self.unsavedChanges():
            cheqlist.log.info("*** Goodbye!")
            # super(Main, self).closeEvent(event)
            self.undoWidget.hide()
            event.accept()
            QtWidgets.qApp.quit()
        else:
            cheqlist.log.info("Aborted quit")
            event.ignore()

    def unsavedChanges(self):
        """If there are unsaved changes, ask the user if they want to save."""
        if not self.undoStack.isClean():
            if self.filename:
                msg = "List \"{0}\" has been modified.".format(
                    self.filebasename)
            else:
                msg = "The list has been modified."
            msgBox = QtWidgets.QMessageBox(self)
            msgBox.setWindowTitle("Cheqlist")
            msgBox.setText(msg)
            msgBox.setInformativeText("Do you want to save your changes?")
            msgBox.setIcon(QtWidgets.QMessageBox.Question)
            msgBox.setStandardButtons(QtWidgets.QMessageBox.Save |
                                      QtWidgets.QMessageBox.Discard |
                                      QtWidgets.QMessageBox.Cancel)
            msgBox.setDefaultButton(QtWidgets.QMessageBox.Save)
            ret = msgBox.exec()
            if ret == QtWidgets.QMessageBox.Save:
                self.saveHandler(None)
                return True
            elif ret == QtWidgets.QMessageBox.Discard:
                return True
            elif ret == QtWidgets.QMessageBox.Cancel:
                return False
        else:
            return True

    def checkAll(self, event=None):
        """Check all items (complete the list)."""
        self.undoStack.push(undocommands.CommandCheckAll(self))

    def checkNone(self, event=None):
        """Uncheck all items (reset the list)."""
        self.undoStack.push(undocommands.CommandCheckNone(self))

    def checkInvert(self, event=None):
        """Check all unchecked items, uncheck all checked items."""
        self.undoStack.push(undocommands.CommandCheckInvert(self))

    def ignoreStruckOutHandler(self, event=None):
        """Toggle the setting that ignores struck out events."""
        self.ignoreStruckOut = self.actionIgnoreStruckOut.isChecked()
        cheqlist.config.set("settings", "ignore_struck_out",
                            utils.config_bool(self.ignoreStruckOut))
        cheqlist.config_write()
        self.updateProgressBar()

    def pasteItems(self, event=None):
        """Open the paste items dialog box."""
        pw = PasteWindow(self)
        if pw.exec():
            self.loadFromText(pw.textBox.toPlainText().splitlines())

    # UI functions and helpers
    def tasklistMenuHandler(self, point):
        """Show the right-click menu of a task list."""
        pos = self.tasklist.mapToGlobal(point)
        m = QtWidgets.QMenu()
        if self.tasklist.count() == 0:
            m.addAction(self.actionAdd)
        else:
            m.addAction(self.actionEdit)
            m.addAction(self.actionDelete)
            m.addAction(self.actionBold)
            m.addAction(self.actionItalic)
            m.addAction(self.actionUnderline)
            m.addAction(self.actionStrikeOut)
        m.exec(pos)

    def cleanChanged(self, clean):
        """Update the window title to reflect that the window is dirty."""
        self.updateWindowTitle()

    def updateWindowTitle(self):
        """Set the appropriate window title (file name, dirty status)."""
        if self.filename and self.undoStack.isClean():
            self.setWindowTitle("{0} — Cheqlist".format(self.filebasename))
        elif self.filename:
            self.setWindowTitle("{0} * — Cheqlist".format(self.filebasename))
        else:
            self.setWindowTitle("Cheqlist")

    def itemChangedHandler(self, item):
        """Handle item changes."""
        try:
            lt = self.lastText[id(item)]
            it = item.text()
            if lt is None and it:
                # Text added
                self.undoStack.push(undocommands.CommandAdd(item, self))
            elif lt is not None and it != lt:
                # Item text changed, let’s make this an edit action
                self.undoStack.push(undocommands.CommandEdit(
                    item, self, lt, it))
        except KeyError:
            self.lastText[id(item)] = None

        cs = item.checkState()
        try:
            ls = self.lastState[id(item)]
            if ls != cs and cs == QtCore.Qt.Checked:
                self.undoStack.push(undocommands.CommandCheck(item, self))
            elif ls != cs and cs == QtCore.Qt.Unchecked:
                self.undoStack.push(undocommands.CommandUnCheck(item, self))
        except KeyError:
            # lastState is set only after checkState is set
            pass
        self.updateUI()

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

    def updateUnderlineAction(self):
        """Set the underline action check status."""
        s = False
        for i in self.tasklist.selectedItems():
            s = i.font().underline()

        self.actionUnderline.setChecked(s)

    def updateStrikeOutAction(self):
        """Set the strike out action check status."""
        s = False
        for i in self.tasklist.selectedItems():
            s = i.font().strikeOut()

        self.actionStrikeOut.setChecked(s)

    def updateDisabledButtons(self):
        """Disable buttons if the list is empty."""
        if self.tasklist.count() == 0:
            self.actionDelete.setEnabled(False)
            self.actionBold.setEnabled(False)
            self.actionBold.setChecked(False)
            self.actionItalic.setEnabled(False)
            self.actionItalic.setChecked(False)
            self.actionUnderline.setEnabled(False)
            self.actionUnderline.setChecked(False)
            self.actionStrikeOut.setEnabled(False)
            self.actionStrikeOut.setChecked(False)
            self.progressBar.setEnabled(False)
        else:
            self.actionDelete.setEnabled(True)
            self.actionBold.setEnabled(True)
            self.actionItalic.setEnabled(True)
            self.actionUnderline.setEnabled(True)
            self.actionStrikeOut.setEnabled(True)
            self.progressBar.setEnabled(True)

    def updateUI(self):
        """Update all UI."""
        self.updateProgressBar()
        self.selectionHandler()
        self.updateDisabledButtons()
        self.updateWindowTitle()

    def _updateUI_disabled(self):
        """Do nothing."""
        pass

    _updateUI_enabled = updateUI

    def updateUI_disable(self):
        """Disable the updateUI function for long running operations."""
        self.progressBar.setMaximum(0)
        self.progressBar.setValue(0)
        self.updateUI = self._updateUI_disabled

    def updateUI_enable(self):
        """Enable the updateUI function after long running operations."""
        self.updateUI = self._updateUI_enabled
        self.updateUI()

    def selectionHandler(self):
        """Update actions when the selection changes."""
        self.updateBoldAction()
        self.updateItalicAction()
        self.updateUnderlineAction()
        self.updateStrikeOutAction()
