Test apps
=========

This folder contains small, manual “test applications” for ``@osmoweb/backend-core`` controllers.

They connect to Osmocom daemons over **VTY (telnet)** and run a few basic operations to validate that:

-  the daemon is reachable
-  parsing/commands work
-  basic CRUD flows behave as expected

Prerequisites
-------------

-  Osmocom services must be running and reachable from this machine.
-  Default targets are hard-coded to ``localhost`` VTY ports:

   -  BSC: ``localhost:4242``
   -  MGW: ``localhost:4243``
   -  MSC: ``localhost:4254``
   -  HLR: ``localhost:4258``

If your services run elsewhere, edit the host/port in the corresponding ``*.ts`` file.

Install
-------

From the repository root:

.. code:: bash

   npm install

Run
---

Change into this directory:

.. code:: bash

   cd test-apps

Run the individual test apps:

.. code:: bash

   npm run test:bsc
   npm run test:hlr
   npm run test:msc
   npm run test:mgw

What each test does
-------------------

.. _bsc-bsc-testts:

BSC (``bsc-test.ts``)
~~~~~~~~~~~~~~~~~~~~~

-  Reads BSC stats
-  Lists BTSes
-  Adds a BTS and updates it (delete is present but commented out)

This **changes BSC state**. Run only against a dev/test BSC.

.. _hlr-hlr-testts:

HLR (``hlr-test.ts``)
~~~~~~~~~~~~~~~~~~~~~

-  Reads stats and lists subscribers
-  Adds a test subscriber, reads it, updates it, checks existence
-  Deletes the test subscriber

This **modifies subscriber DB**. Run only against a dev/test HLR.

.. _msc-msc-testts--mgw-mgw-testts:

MSC (``msc-test.ts``) / MGW (``mgw-test.ts``)
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

-  Reads ``getStats()`` and disconnects

Troubleshooting
---------------

-  If you get connection errors, verify that the VTY port is reachable:

   -  ``telnet localhost 4242`` (BSC)
   -  ``telnet localhost 4258`` (HLR)

-  If a test fails mid-way, the script still calls ``.disconnect()`` in ``finally``.
