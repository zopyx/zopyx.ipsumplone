zopyx.ipsumplone
================

This package provides some browser view for creating demo content and demo
images without reinventing functionality for every new project.

Installation
============

Add ``zopyx.ipsumplone`` to the eggs options of your buildout configuration, re-run
buildout and restart your Plone instance.

Usage
=====

- ``@@new-site`` called in the context of the Zope root object or a Zope folder will
  create a new Plone site with a unique id.

- ``@@demo-content`` called in the context of the a Plone site will create
  a set of folder for images, news items, events, files and documents.

The main purpose of the package to call the views above inside the setuphandler
or profile setup step to generate example content on request.  Please check the
``browser/setup.py`` implementation to figure out API methods like
``createDocument()``, ``createImage()`` or ``createNewsitem()``. Subclassing
the ``Setup`` view is obviously a good start for own customizations.

Requirements
============

* tested with Plone 5.0 and Dexterity content (use ``zopyx.ipsumplone`` 0.2.X
  for Archetypes-based content under Plone 4.X)

Sources
=======

See https://github.com/zopyx/zopyx.ipsumplone

Issue tracker
=============

See https://github.com/zopyx/zopyx.ipsumplone/issues


Licence
=======
``zopyx.ipsumplone`` is published under the GNU Public Licence Version 2

Author
======

| ZOPYX/Andreas Jung
| Hundskapfklinge 33
| D-72070 Tübingen, Germany
| www.zopyx.com
| info@zopyx.com

