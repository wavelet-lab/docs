@osmoweb/nestjs-microservice
============================

NestJS integration layer for OsmoWeb.

This package wires ``@osmoweb/backend-core`` into NestJS primitives:

-  A ready-to-import ``OsmoModule``
-  WebSocket gateways for Osmocom bridge flows (``control``, ``media``, ``abis_oml``, ``abis_rsl``)
-  A small REST controller for per-user BTS config (``/api/v1/osmo/bts``)
-  Optional background stats polling with writers for InfluxDB / Prometheus Pushgateway

It is designed to run in **Node.js**.

Install
-------

.. code:: bash

   npm install @osmoweb/nestjs-microservice

Imports (entrypoints)
---------------------

Subpath exports:

-  ``@osmoweb/nestjs-microservice`` — re-exports ``osmo``, and re-exports ``auth``/``users`` from ``@websdr/nestjs-microservice``
-  ``@osmoweb/nestjs-microservice/osmo`` — OsmoWeb module (``OsmoModule``) and tokens
-  ``@osmoweb/nestjs-microservice/auth`` — re-exported from ``@websdr/nestjs-microservice/auth``
-  ``@osmoweb/nestjs-microservice/users`` — re-exported from ``@websdr/nestjs-microservice/users``

Quick start
-----------

In your application module:

.. code:: ts

   import { Module } from '@nestjs/common';
   import { ConfigModule } from '@nestjs/config';
   import { OsmoModule } from '@osmoweb/nestjs-microservice/osmo';

   @Module({
     imports: [
       ConfigModule.forRoot({ isGlobal: true }),
       OsmoModule,
     ],
   })
   export class AppModule {}

Configuration (env vars)
------------------------

``OsmoModule`` provides an ``OSMO_PARAMS`` token (type ``OsmoParams``) built from ``@nestjs/config``.

Osmocom service addresses
~~~~~~~~~~~~~~~~~~~~~~~~~

These keys override defaults from ``@osmoweb/backend-core``:

-  ``OSMO_SERVER_PORT``

Per-service host/port pairs:

-  ``OSMO_UDP_MEDIA_URI``, ``OSMO_UDP_MEDIA_PORT``
-  ``OSMO_TCP_ABIS_OML_URI``, ``OSMO_TCP_ABIS_OML_PORT``
-  ``OSMO_TCP_ABIS_RSL_URI``, ``OSMO_TCP_ABIS_RSL_PORT``
-  ``OSMO_TCP_HLR_URI``, ``OSMO_TCP_HLR_PORT``
-  ``OSMO_TCP_BSC_URI``, ``OSMO_TCP_BSC_PORT``

WebSocket endpoints
~~~~~~~~~~~~~~~~~~~

Gateways are currently registered with fixed endpoints:

-  ``/wsdr/osmo/control``
-  ``/wsdr/osmo/media``
-  ``/wsdr/osmo/abis_oml``
-  ``/wsdr/osmo/abis_rsl``

Note: ``OSMO_CONTROL_URI``, ``OSMO_MEDIA_URI``, ``OSMO_ABIS_OML_URI``, ``OSMO_ABIS_RSL_URI`` are also read into ``OSMO_PARAMS``, but the gateway decorators currently use the hardcoded endpoints above.

Worker pool
~~~~~~~~~~~

-  ``OSMO_WORKER_POOL_SIZE``

REST API
--------

``GET /api/v1/osmo/bts``
~~~~~~~~~~~~~~~~~~~~~~~~

Returns the BTS config/info assigned to the authenticated user.

``PUT /api/v1/osmo/bts``
~~~~~~~~~~~~~~~~~~~~~~~~

Allocates a BTS for the authenticated user (if needed) and updates its config in the BSC via VTY.

Payload is validated using ``class-validator`` (see ``UpdateBtsDto``).

Authentication: this controller uses ``AuthGuard('jwt')``. Your application must register a Passport JWT strategy (e.g. by using the auth module from ``@websdr/nestjs-microservice``).

WebSocket bridge
----------------

The gateways delegate to ``@osmoweb/backend-core`` router controllers.

Important: some flows use a BTS pool loaded from a ``bts-config.json`` file in the **current working directory** (see ``@osmoweb/backend-core`` BtsPool).

Stats polling
-------------

``StatsModule`` can periodically poll VTY controllers and write metrics.

Enable/disable and interval:

-  ``STATS_ENABLED`` (default: true)
-  ``STATS_INTERVAL_MS`` (default: 10000)

Writers are enabled only when their env vars are provided:

InfluxDB:

-  ``INFLUXDB_URL``
-  ``INFLUXDB_ORG``
-  ``INFLUXDB_TOKEN``
-  ``INFLUXDB_BUCKET``

Prometheus Pushgateway:

-  ``PROMETHEUS_PUSH_URL``

Compatibility notes
-------------------

-  **TypeScript:** ships ``*.d.ts`` typings.

Development (monorepo)
----------------------

From the repository root:

.. code:: bash

   npm install
   npm run build
   npm test --workspace=packages/nestjs-microservice

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

-  Entry point: https://github.com/wavelet-lab/osmoweb/blob/main/packages/nestjs-microservice/src/index.ts
-  Osmo modules exports: https://github.com/wavelet-lab/osmoweb/blob/main/packages/nestjs-microservice/src/osmo/index.ts

Package folder (GitHub):
https://github.com/wavelet-lab/osmoweb/tree/main/packages/nestjs-microservice

License
-------

OsmoWeb is `MIT licensed <https://github.com/wavelet-lab/osmoweb/blob/main/LICENSE>`__
