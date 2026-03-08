@osmoweb/backend-core
=====================

Backend building blocks for OsmoWeb.

This package provides:

-  **VTY-based controllers** (BSC/HLR/MSC/MGW/STP) for reading stats and performing common operations.
-  **WebSocket → Osmocom bridges** (ABIS OML/RSL, Media, Control) via a small router/controller layer.
-  **Small utilities** for BTS assignment and stats collection.

It is designed to run in **Node.js** (it uses TCP/UDP sockets and ``ws``).

Install
-------

.. code:: bash

   npm install @osmoweb/backend-core

Imports (entrypoints)
---------------------

This package is published with subpath exports:

-  ``@osmoweb/backend-core`` — re-exports everything from ``osmo``, ``osmoctrl``, ``osmorouter``
-  ``@osmoweb/backend-core/osmo`` — BTS management helpers
-  ``@osmoweb/backend-core/osmoctrl`` — VTY controllers + stats collector utilities
-  ``@osmoweb/backend-core/osmorouter`` — WebSocket routing + TCP/UDP bridge controllers

Example:

.. code:: ts

   import { BscController, HlrController } from '@osmoweb/backend-core/osmoctrl';
   import { Router, osmoDefaultParams } from '@osmoweb/backend-core/osmorouter';
   import { BtsManager } from '@osmoweb/backend-core/osmo';

Compatibility notes
-------------------

-  **Runtime:** Node.js (uses ``net``, ``dgram``, and ``ws``).
-  **Module format:** ESM (``"type": "module"``).
-  **Network access:** most controllers require reachability to Osmocom services.

osmoctrl (VTY controllers)
--------------------------

The ``osmoctrl`` module talks to Osmocom daemons via their **VTY (telnet) interface**.

Controllers
~~~~~~~~~~~

Controllers connect to a host/port (defaults are provided) and expose typed helpers.

.. code:: ts

   import { BscController, HlrController, MscController } from '@osmoweb/backend-core/osmoctrl';

   const bsc = new BscController('localhost', 4242);
   const hlr = new HlrController('localhost', 4258);
   const msc = new MscController('localhost', 4254);

   const [bscStats, hlrStats, mscStats] = await Promise.all([
     bsc.getStats(),
     hlr.getStats(),
     msc.getStats(),
   ]);

   bsc.disconnect();
   hlr.disconnect();
   msc.disconnect();

Examples of controller-specific operations:

.. code:: ts

   import { BscController, HlrController } from '@osmoweb/backend-core/osmoctrl';

   const bsc = new BscController();
   const btsList = await bsc.getAllBts();

   const hlr = new HlrController();
   const subs = await hlr.getSubscribers();
   // await hlr.addSubscriber({ imsi: '001010000000001', msisdn: '1001', algorithm: 'comp128v1', ki: '001122...' })

   bsc.disconnect();
   hlr.disconnect();

Stats collection
~~~~~~~~~~~~~~~~

``StatsCollector`` can poll multiple controllers and return a unified list.

.. code:: ts

   import { StatsCollector, forEachOsmoService } from '@osmoweb/backend-core/osmoctrl';
   import { BscController, HlrController } from '@osmoweb/backend-core/osmoctrl';

   const collector = new StatsCollector();
   collector.addController('bsc', new BscController('localhost', 4242));
   collector.addController('hlr', new HlrController('localhost', 4258));

   const stats = await collector.collect();

   forEachOsmoService(stats, (service, items) => {
     console.log(service, items[0]?.stats);
   });

Note: ``StatsCollector`` accepts a ``LoggerInterface`` (from ``@websdr/core/utils``). If not provided, it uses ``new SimpleLogger(StatsCollector.name)``.

osmorouter (WebSocket bridge)
-----------------------------

The ``osmorouter`` module contains a small router that resolves a controller from the WebSocket URL.

Configuration (``OsmoParams``)
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Defaults are exported as ``osmoDefaultParams``.

.. code:: ts

   import { osmoDefaultParams } from '@osmoweb/backend-core/osmorouter';

   // You can override service addresses/ports if needed
   const params = {
     ...osmoDefaultParams,
     // e.g. change websocket base port
     port: 8800,
   };

Minimal WebSocket server example
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

This is intentionally minimal and meant as a starting point (production apps usually wrap this into a framework).

.. code:: ts

   import http from 'node:http';
   import { WebSocketServer } from 'ws';
   import { Router, osmoDefaultParams } from '@osmoweb/backend-core/osmorouter';

   const server = http.createServer();
   const wss = new WebSocketServer({ server });

   const router = new Router();
   router.init(osmoDefaultParams);

   wss.on('connection', async (ws, req) => {
     const url = req.url ?? '/';
     const ctrl = router.to(url, 0);
     await ctrl.handle(ws, req);
   });

   server.listen(osmoDefaultParams.port);

.. _bts-pool-configuration-bts-configjson:

BTS pool configuration (``bts-config.json``)
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Some controllers (e.g. the Control/Media flows) use a BTS pool loaded from a JSON file in the **current working directory**.

Expected shape:

.. code:: json

   {
     "bts": [
       {
         "id": 0,
         "band": "DCS1800",
         "ip.access": "127.0.0.1",
         "arfcn": 871,
         "cell_identity": 6969,
         "osmux_port": 10000
       }
     ]
   }

osmo (BTS assignment)
---------------------

``BtsManager`` is a small helper to allocate and reuse BTS ids for client sessions.

.. code:: ts

   import { BtsManager } from '@osmoweb/backend-core/osmo';

   const mgr = new BtsManager();

   const a = mgr.allocate('user-uuid-1', '10.0.0.2');
   // -> { id, uuid, ip, connected, createdAt, lastSeen }

   mgr.markDisconnected('user-uuid-1');
   // later:
   mgr.releaseByUuid('user-uuid-1');

API overview
------------

From ``@osmoweb/backend-core/osmo``:

-  ``BtsManager``
-  Types: ``BtsAssignment``

From ``@osmoweb/backend-core/osmoctrl``:

-  Controllers: ``BscController``, ``HlrController``, ``MgwController``, ``MscController``, ``StpController``
-  Types: ``BscBtsConfig``, ``BscBtsTrxConfig``, ``BscBtsInfo``, ``BscTimeslotStats``, ``BscStats``, ``HlrSubscriber``, ``HlrStats``, ``MgwStats``, ``MscStats``, ``StpStats``, ``CollectedStat``, ``CollectedStats``, ``StatsWriter``
-  Stats helpers: ``StatsCollector``, ``forEachOsmoService()``, ``forEachCollectedStat()``
-  Control protocol types: ``CtrlCommand``, ``CtrlResponse``, ``CtrlTrapEvent``, ``OsmoComponent``, ``OSMO_COMPONENTS``

From ``@osmoweb/backend-core/osmorouter``:

-  ``Router``
-  Controllers: ``AbisOmlController``, ``AbisRslController``, ``ControlController``, ``MediaController``
-  Config: ``OsmoServices``, ``osmoServiceAddrMap``, ``osmoDefaultParams``
-  Types: ``OsmoParams``

.. _compatibility-notes-1:

Compatibility notes
-------------------

-  **TypeScript:** ships ``*.d.ts`` typings.

Development (monorepo)
----------------------

From the repository root:

.. code:: bash

   npm install
   npm run build
   npm test --workspace=packages/backend-core

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

-  Entry point: https://github.com/wavelet-lab/osmoweb/blob/main/packages/backend-core/src/index.ts
-  Osmo helpers exports: https://github.com/wavelet-lab/osmoweb/blob/main/packages/backend-core/src/osmo/index.ts
-  Osmo VTY controllers exports: https://github.com/wavelet-lab/osmoweb/blob/main/packages/backend-core/src/osmoctrl/index.ts
-  Osmo router exports: https://github.com/wavelet-lab/osmoweb/blob/main/packages/backend-core/src/osmorouter/index.ts

Package folder (GitHub):
https://github.com/wavelet-lab/osmoweb/tree/main/packages/backend-core

License
-------

OsmoWeb is `MIT licensed <https://github.com/wavelet-lab/osmoweb/blob/main/LICENSE>`__
