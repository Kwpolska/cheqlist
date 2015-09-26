#!/usr/bin/env python
# -*- encoding: utf-8 -*-
import io
from setuptools import setup

setup(name='cheqlist',
      version='0.1.4',
      description='A simple Qt checklist.',
      keywords='cheqlist',
      author='Chris Warrick',
      author_email='chris@chriswarrick.com',
      url='https://github.com/Kwpolska/cheqlist',
      license='3-clause BSD',
      long_description=io.open('./docs/README.rst', 'r', encoding='utf-8').read(),
      platforms='any',
      zip_safe=False,
      include_package_data=True,
      # http://pypi.python.org/pypi?%3Aaction=list_classifiers
      classifiers=['Development Status :: 3 - Alpha',
                   'Environment :: X11 Applications :: Qt',
                   'License :: OSI Approved :: BSD License',
                   'Topic :: Office/Business :: Scheduling',
                   'Programming Language :: Python',
                   'Programming Language :: Python :: 2',
                   'Programming Language :: Python :: 2.7',
                   'Programming Language :: Python :: 3',
                   'Programming Language :: Python :: 3.3',
                   'Programming Language :: Python :: 3.4',
                   'Programming Language :: Python :: 3.5'],
      packages=['cheqlist'],
      data_files=[('share/applications', ['freedesktop/cheqlist.desktop']),
                  ('share/mime/packages', ['freedesktop/cheqlist.xml']),],
      entry_points={
          'gui_scripts': [
              'cheqlist = cheqlist.__main__:main',
          ]
      },
      )
