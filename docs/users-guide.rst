=====================
Cheqlist User’s Guide
=====================

.. contents::

Installing
==========

To install and use Cheqlist, you must first install Qt, Python (Python 3
recommended) and PyQt5.

Cheqlist fully supports Linux and should work on Windows and macOS, but some
things might not work properly or natively.

Arch Linux users can use the ``cheqlist`` package from the AUR. Users of other
Linux distributions need to install it themselves; PyQt5 packages should be
available in OS repositories. macOS users can install ``python3`` from
Homebrew, ``pip`` for that Python manually and ``pyqt5`` from pip (in a
virtualenv, or with ``pip install --user``) to satisfy all dependencies.
Windows users can use installers provided by Python, Qt and PyQt5.

Main Window
===========

Cheqlist opens with an empty task list, but a file may be provided on the
command line. There are three menus (*File*, *Edit*, *Help*) and two toolbars that
allow access to common commands.

Tasks can be added by pressing :kbd:`Ctrl+T` on the keyboard or by clicking the
*Add* button in the toolbar/in the menu. Tasks can be edited with :kbd:`Ctrl+E`
or double clicking. Tasks can be deleted by pressing :kbd:`Delete` or clicking
the *Delete* button in the toolbar/in the menu. Tasks also offer right-click
menus with *Add/Edit/Delete* and formatting.

The entire list can be cleared with :kbd:`Ctrl+R` or the *Clear* button. There
is no confirmation, but it can be undone (:kbd:`Ctrl+Z`).

Files (`*.cheqlist`) may be opened or saved, see `File format`_ for details of what input is
taken and what is saved to files. Opening or saving a file links Cheqlist to
that file (further *Save* operations won’t ask for a file name). Closing
Cheqlist with unsaved changes will prompt to save them.

Mac users: Replace Ctrl with ⌘ Command and Alt with ⌥ Option.

Formatting
----------

There are four formatting options available: bold (:kbd:`Ctrl+B`), italic
(:kbd:`Ctrl+I`), underline (:kbd:`Ctrl+U`), and strike out (:kbd:`Ctrl+Alt+S`).
Bold, italic, and underline have no meaning to the application (they are for
decoration only). Strike out has no meaning unless *Ignore struck out tasks* is
enabled from the *Edit* menu (saved in configuration between sessions).

Pressing :kbd:`Ctrl+Up` and :kbd:`Ctrl+Down` moves items up and down on the list.

Undo, Redo, Undo Window
-----------------------

All operations can be undone. Saving a file clears the undo list. To see all
operations, you can use the *Show undo window* option from the *Edit* menu.

Pasting items
-------------

The *Paste items…* option in the edit menu (:kbd:`Ctrl+V` when *not* editing a
task) allows users to add tasks from the clipboard. It can also be used to add
multiple tasks without having to press :kbd:`Ctrl+T` after every task (i.e.
Collection Mode/Bulk Add) Input is parsed the same way as files — check the
`File format`_ section for details.

Bulk operations
---------------

There are three bulk operations in the *Edit* menu. *Check All* marks all tasks
as done (sets completion to 100%).  *Check None* marks all tasks as undone
(sets completion to 0%). *Invert Selection* marks all done tasks as undone, and
all undone tasks as done (completion = 100% - previous completion)

File format
===========

Cheqlist uses a very liberal parser for files, loosely based on GitHub Flavored
Markdown’s list syntax. The following rules apply:

* If a line starts with asterisks or dashes followed by spaces, those are removed. (bulleted list syntax)
* If a line starts with ``[ ]`` (after removing asterisks/dashes), those are removed and the task is marked as incomplete.
* If a line starts with ``[x]`` or ``[X]`` or ``[*]``, those are removed and the task is marked as complete.
* If text is wrapped in single asterisks or underscores (``*italic*``, ``_italic_``), it is interprted as italic text.
* If text is wrapped in double asterisks underscores (``**bold**``, ``__bold__``), it is interprted as italic text.
* If text is wrapped in ``<u>`` HTML tags (``<u>underline</u>``), it is interpreted as underlined text.
* If text is wrapped in double tildes (``~~strikeout~~``), it is interpreted as struck out text.
* A zero-width-non-joiner character (U+200C) on both sides of a line may be used to preserve raw asterisks, underscores, tildes or <u> tags at start/end of lines.
* Text formatting options may be mixed, eg. ``<u>~~***all formattings***~~</u>``
* Cheqlist itself starts lines with dashes and ``[ ]`` or ``[x]`` in saved files.

The source distribution has some example files that show available formats, alongside a file generator
(that often produces garbled output to test the parser).

Configuration
=============

Configuration is stored in ``~/.config/kwpolska/cheqlist/cheqlist.ini``.
The current configuration values are:

* ``[directories]``
    * ``lastdir`` — last directory used when opening files
    * ``homedir`` — home directory for lists (used only if ``open_from`` is set
      to ``homedir``)
    * ``open_from`` — place to open from (``lastdir`` or ``homedir``)
* ``[settings]``
    * ``ignore_struck_out`` (true/false) — whether or not to ignore tasks that
      are struck out

Logs are stored in ``~/.config/kwpolska/cheqlist/cheqlist.log``.
