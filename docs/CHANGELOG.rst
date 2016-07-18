=====================
Appendix C. Changelog
=====================
:Info: This is the changelog for Cheqlist.
:Author: Chris Warrick <chris@chriswarrick.com>
:Copyright: © 2015-2016, Chris Warrick.
:License: BSD (see /LICENSE or :doc:`Appendix B <LICENSE>`.)
:Date: 2016-07-18
:Version: 0.3.0

.. index:: CHANGELOG

GitHub holds releases, too
==========================

More information can be found on GitHub in the `releases section
<https://github.com/Kwpolska/cheqlist/releases>`_.

Version History
===============

0.3.0
    * More resilient, regex-based input parser
    * Full file support (remembers file names, save on quit if changes made etc.)
    * Undo/redo capability for all operations
    * Better performance of large lists (patterns, opening)
    * Ability to paste tasks/insert from text (Ctrl+V)

0.2.0
    * Display exceptions in message boxes
    * More formatting: underline and strikeout
    * Remove sample items
    * Split into two toolbars (Main and Edit)
    * Make it possible to ignore struck-out tasks
    * Add right-click menus

0.1.6
    * Fix updating last used directory

0.1.5
    * Fix task counting in logs (prevents crash on write)

0.1.4
    * Support opening files (requires MIME database update)

0.1.3
    * Remember last location used
    * Add config file support
    * Add logging
    * Select newly added items (Ctrl+B/Ctrl+I will work, but will also clear the
      text while editing)

0.1.2
    * Add menu bar
    * Add Quit action (Ctrl+Q)
    * Add Edit action (Ctrl+E)
    * Add actions to (un)check all and invert checks

0.1.1
    * .cheqlist extension
    * minor fixes
    * demo files

0.1.0
    Initial release.
