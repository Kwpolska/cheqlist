=================================
Cheqlist.  A simple Qt checklist.
=================================
:Info: This is the README file for Cheqlist.
:Author: Chris Warrick <chris@chriswarrick.com>
:Copyright: © 2015-2016, Chris Warrick.
:Date: 2016-11-20
:Version: 0.3.1

PURPOSE
-------

This is a simple checklist application, written in PyQt5.

SCREENSHOT
----------

.. image:: https://github.com/Kwpolska/cheqlist/raw/master/screenshot.png
   :alt: Cheqlist
   :align: center

INSTALLATION
------------

::

    pip install cheqlist

Make sure you have PyQt5 installed.  AUR package also available.

If you are on Linux, run::

    sudo update-mime-database /usr/share/mime

FILE FORMAT
-----------

GitHub Flavored Markdown is the usual file format::

    - [ ] unchecked
    - [x] checked


However, the parser is quite liberal when it comes to reading files.
It also supports Markdown-style formatting for ``**bold**, *italic*,
<u>underline</u>, ~~strikeout~~``.

READ MORE
---------

See the `Cheqlist User’s Guide <https://cheqlist.readthedocs.io/en/latest/users-guide.html>`_ for more details.

COPYRIGHT
---------
Copyright © 2015-2016, Chris Warrick.
All rights reserved.

Redistribution and use in source and binary forms, with or without
modification, are permitted provided that the following conditions are
met:

1. Redistributions of source code must retain the above copyright
   notice, this list of conditions, and the following disclaimer.

2. Redistributions in binary form must reproduce the above copyright
   notice, this list of conditions, and the following disclaimer in the
   documentation and/or other materials provided with the distribution.

3. Neither the name of the author of this software nor the names of
   contributors to this software may be used to endorse or promote
   products derived from this software without specific prior written
   consent.

THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS
"AS IS" AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT
LIMITED TO, THE IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR
A PARTICULAR PURPOSE ARE DISCLAIMED.  IN NO EVENT SHALL THE COPYRIGHT
OWNER OR CONTRIBUTORS BE LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL,
SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT
LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES; LOSS OF USE,
DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND ON ANY
THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT
(INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE
OF THIS SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.
