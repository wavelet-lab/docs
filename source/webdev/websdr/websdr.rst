WebSDR
======

`WebSDR <https://github.com/wavelet-lab/websdr>`__ is an open-source TypeScript monorepo that provides libraries and tools for building web applications that work with Software Defined Radios (SDR) using WebUSB and related browser/node tooling.

⚠️ This project is under active development. Some features are experimental and APIs may change.

Supported SDR hardware
----------------------

Currently supported SDR devices:

1. `Wavelet uSDR <https://docs.wsdr.io/hardware/usdr.html>`__ — can be connected via the `Development Board <https://docs.wsdr.io/hardware/devboard.html>`__ or the `USB adapter <https://docs.wsdr.io/hardware/usbadapter.html>`__.
2. `Wavelet xSDR <https://docs.wsdr.io/hardware/xsdr.html>`__ — can be connected via the `Development Board <https://docs.wsdr.io/hardware/devboard.html>`__ or the `USB adapter <https://docs.wsdr.io/hardware/usbadapter.html>`__.
3. `LimeSDR Mini v2 <https://limesdr-mini.myriadrf.org/v2.2/>`__ — tested with v2.2; should also work with v2.3 and v2.4.
4. `SSDR <https://www.crowdsupply.com/wavelet-lab/ssdr>`__
5. `XTRX <https://www.crowdsupply.com/fairwaves/xtrx>`__
6. RTLSDR - support is in progress

What is WebSDR?
---------------

WebSDR contains utilities, UI components, backend modules, and small test apps to make it easier to build browser-based SDR applications and tooling. The primary goal is to enable interaction with SDR devices connected over USB from web applications (via WebUSB), and to provide supporting building blocks for dashboards, demos, and server-side microservices.

Core capabilities include:

-  `WebUSB device management <https://github.com/wavelet-lab/websdr/tree/main/docs/webusb/README.md>`__ (requesting devices, selecting devices in UI components).
-  A small Vue 3 component library for dashboards and controls (dropdowns, lists, inputs, log viewers).
-  NestJS modules for microservices (authentication, API scaffolding) useful for backend parts of an SDR web platform.
-  Utility modules: circular buffers, data conversion helpers, string utilities, time helpers and promise helpers used across frontend and backend.

Documentation
-------------

-  Docs index: `https://github.com/wavelet-lab/websdr/tree/main/docs/README.md <https://github.com/wavelet-lab/websdr/tree/main/docs/README.md>`__
-  WebUSB / SDR interaction subsystem: `https://github.com/wavelet-lab/websdr/tree/main/docs/webusb/README.md <https://github.com/wavelet-lab/websdr/tree/main/docs/webusb/README.md>`__

Repository layout
-----------------

Top-level structure (important folders):

::

   packages/
   ├─ core/                # Shared domain types, utilities, constants
   ├─ frontend-core/       # Front-end utilities and WebUSB adapters
   ├─ vue3-components/     # Reusable Vue 3 UI components and styles
   ├─ nestjs-microservice/ # NestJS modules (auth, API helpers, microservice wiring)
   https://github.com/wavelet-lab/websdr/tree/main/docs/                   # Architecture and subsystem documentation
   test-apps/              # Small example/test applications and scripts

Brief package descriptions:

-  ``packages/core`` — Core shared library with domain types, utilities, constants and radio-related helpers.
-  ``packages/frontend-core`` — Front-end core utilities, WebUSB adapters, and services used by client apps.
-  ``packages/vue3-components`` — Vue 3 component library (examples: ``SdrInput``, ``Dropdown``, ``List``, ``LogArea``). Built with Vite; ships TypeScript types and styles.
-  ``packages/nestjs-microservice`` — NestJS integration and helper modules; main entry is ``WebSDRModule`` (configurable via environment variables such as ``WEBSDR_*``).
-  ``test-apps`` — Small scripts and demo pages used to test low-level functionality (e.g., ``usb-test.ts``).

Published npm packages
----------------------

This monorepo publishes several packages under the ``@websdr/*`` scope. If you only want to consume the libraries (not develop inside the monorepo), install them from npm.

-  ``@websdr/core`` — shared types/constants and small utilities.

   -  Docs: `core.rst <core.rst>`__
   -  Install: ``npm install @websdr/core``

-  ``@websdr/frontend-core`` — frontend utilities (API helpers, WebUSB abstraction).

   -  Docs: `frontend-core.rst <frontend-core.rst>`__
   -  Install: ``npm install @websdr/frontend-core``

-  ``@websdr/vue3-components`` — Vue 3 UI components + styles.

   -  Docs: `vue3-components.rst <vue3-components.rst>`__
   -  Install: ``npm install @websdr/vue3-components``

-  ``@websdr/nestjs-microservice`` — reusable NestJS modules (auth/users/logging).

   -  Docs: `nestjs-microservice.rst <nestjs-microservice.rst>`__
   -  Install: ``npm install @websdr/nestjs-microservice``

Quick setup
-----------

Install dependencies for the workspace:

.. code:: bash

   npm install

If you only want to use the libraries as dependencies, see **Published npm packages** above.

Build the packages:

.. code:: bash

   npm run build

Run tests (runs workspace tests):

.. code:: bash

   npm run test

Run all tests

.. code:: bash

   npm run test:all

Run all tests and watch for changes

.. code:: bash

   npm run test:watch

Run coverage check

.. code:: bash

   npm run test:coverage

Running test applications
-------------------------

Example test apps live in ``test-apps``. To run them:

.. code:: bash

   cd test-apps
   npm install
   npm run test:usb   # runs the USB test script (requires appropriate permissions/flags)

Note: WebUSB requires HTTPS or localhost and browser support. Running tests that access USB devices may require additional browser flags or permissions.

.. _environment--configuration:

Environment / Configuration
---------------------------

-  ``packages/nestjs-microservice`` reads configuration from environment variables (prefixed with ``WEBSDR_`` in places). See the module entry and code for exact variable names.

License
-------

WebSDR is `MIT licensed <https://github.com/wavelet-lab/websdr/blob/main/LICENSE>`__
