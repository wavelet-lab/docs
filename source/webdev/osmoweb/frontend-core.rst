@osmoweb/frontend-core
======================

Front-end helpers for OsmoWeb applications.

This package is intentionally small: it provides thin, typed wrappers around OsmoWeb HTTP APIs (via ``apiFetch`` from ``@websdr/frontend-core``).

Install
-------

.. code:: bash

   npm install @osmoweb/frontend-core

Imports (entrypoints)
---------------------

-  ``@osmoweb/frontend-core`` — re-exports everything from ``./services``
-  ``@osmoweb/frontend-core/services`` — API client helpers

.. code:: ts

   import { getBts, updateBts } from '@osmoweb/frontend-core/services';

Services
--------

BTS service
~~~~~~~~~~~

Endpoints:

-  ``GET /api/v1/osmo/bts`` → ``getBts()``
-  ``PUT /api/v1/osmo/bts`` → ``updateBts(cfg?)``

.. code:: ts

   import { getBts, updateBts } from '@osmoweb/frontend-core/services';
   import { GSMBand } from '@osmoweb/core';
   import type { BscBtsConfig } from '@osmoweb/backend-core';

   // Read BTS info for the current user/session
   const bts = await getBts();

   // Update BTS config
   const cfg: BscBtsConfig = {
     type: 'osmo-bts',
     band: GSMBand.GSM_900,
     description: 'Demo BTS',
     trx: [{ id: 0, arfcn: 0 }],
   };

   await updateBts(cfg);

   // Reset / send empty payload
   await updateBts();

Notes
-----

-  These helpers assume an OsmoWeb backend that exposes ``/api/v1/osmo/*`` routes.
-  Request mechanics (base URL, auth headers/cookies, error handling) are delegated to ``apiFetch`` from ``@websdr/frontend-core``.

API overview
------------

From ``@osmoweb/frontend-core/services``:

-  ``getBts(): Promise<BscBtsInfo>``
-  ``updateBts(cfg?: BscBtsConfig): Promise<any>``

Compatibility notes
-------------------

-  **TypeScript:** ships ``*.d.ts`` typings.

Development (monorepo)
----------------------

From the repository root:

.. code:: bash

   npm install
   npm run build
   npm test --workspace=packages/frontend-core

From this package folder:

Build
~~~~~

.. code:: bash

   npm run build

Test
~~~~

.. code:: bash

   npm test

Source links
------------

This package publishes ``dist/`` to npm. Source is available in the GitHub repository:

-  Entry point: https://github.com/wavelet-lab/osmoweb/blob/main/packages/frontend-core/src/index.ts
-  Osmo services exports: https://github.com/wavelet-lab/osmoweb/blob/main/packages/frontend-core/src/services/index.ts

Package folder (GitHub):
https://github.com/wavelet-lab/osmoweb/tree/main/packages/frontend-core

License
-------

OsmoWeb is `MIT licensed <https://github.com/wavelet-lab/osmoweb/blob/main/LICENSE>`__
