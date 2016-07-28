=========
typejudge
=========

Judgement as a Service.

Typejudge will automatically check for `semver <http://semver.org/>`_
compliance based on type hints.  If the type signature for a function changes,
it will judge this to be an API change and recommend a major version bump.

This is largely inspired by Elm's package manager, which also enforces semver.


Installation
============

Note: typejudge only works on python 3.5 and higher.

Install with pip::

    $ pip install typejudge


Usage
=====

.. code-block::

    $ typejudge --help
    usage: typejudge [-h] [-o OUT] [-f FILE] MODULE [VERSION]

    judge your types

    positional arguments:
      MODULE                module to import and check
      VERSION               current version of the package

    optional arguments:
      -h, --help            show this help message and exit
      -o OUT, --out OUT     save current type definitions to this file
      -f FILE, --file FILE  load type definitions from this file

Example usage
-------------

Suppose we've got a module that contains some type annotations on the publicly
exported API, testmodule.py:

.. code-block:: python

    def greeting(name: str) -> str:
        return 'Hello ' + name

Save the types somewhere:

.. code-block:: bash

    $ typejudge -o testmodule.json testmodule

Make some small change to ``testmodule.py``, add a new function:

.. code-block:: python

    def greeting2(name: str, name2: str) -> str:
        return 'Hello ' + name + ' and ' name2

Typejudge will recommend this is a minor release:

.. code-block::

    $ typejudge -f testmodule.json testmodule
    minor

The same, but with a known current version number:

.. code-block:: bash

    $ typejudge -f testmodule.json testmodule 0.3.2
    0.4.0

Make a change to existing type signatures:

.. code-block:: python

    from typing import List

    def greeting(names: List[str]) -> str:
        return 'Hello ' + ' '.join(names)

Typejudge will now recommend this is a major release:

.. code-block:: bash

    $ typejudge -f testmodule.json testmodule
    major
