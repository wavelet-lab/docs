@osmoweb/core
=============

Shared, dependency-light utilities and domain types used across the OsmoWeb monorepo.

Today, the package focuses on:

-  **Radio helpers**: ARFCN ⇄ frequency conversions and band detection for **GSM / LTE / NR**.
-  **Osmo helpers**: small utilities that adapt Osmocom concepts to the rest of the stack (e.g., log level mapping).

Install
-------

.. code:: bash

   npm install @osmoweb/core

Imports (entrypoints)
---------------------

This package is published with subpath exports:

-  ``@osmoweb/core`` — re-exports everything from ``radio`` and ``osmo``
-  ``@osmoweb/core/radio`` — radio band/ARFCN/frequency helpers
-  ``@osmoweb/core/osmo`` — Osmocom-related helpers

In most apps you’ll want the more specific entrypoints to keep imports explicit:

.. code:: ts

   import { configureARFCN, RadioTechnology, LTEBand } from '@osmoweb/core/radio';
   import { getJournalLogLevelFromOsmoLogLevel } from '@osmoweb/core/osmo';

Units
-----

All frequencies in this package are expressed in **kHz**.

Radio
-----

``configureARFCN()``
~~~~~~~~~~~~~~~~~~~~

A universal helper that takes either an **ARFCN** or a **frequency** (kHz) and returns a complete configuration:

-  detects ``technology`` and ``band`` when possible
-  computes ``uplinkFrequency`` and ``downlinkFrequency`` (kHz)
-  ``frequency`` can be either uplink or downlink; the helper will normalize it by recomputing both sides

.. code:: ts

   import {
     configureARFCN,
     RadioTechnology,
     LTEBand,
   } from '@osmoweb/core/radio';

   // 1) Provide ARFCN (highest priority)
   const cfg1 = configureARFCN({
     technology: RadioTechnology.LTE,
     band: LTEBand.B3,
     arfcn: 1300,
   });

   // cfg1.uplinkFrequency / cfg1.downlinkFrequency are in kHz

   // 2) Provide frequency (kHz) and let band auto-detect
   const cfg2 = configureARFCN({
     technology: RadioTechnology.GSM,
     frequency: 935_200, // kHz
   });

   // cfg2.arfcn is computed and frequencies are normalized

Low-level conversions
~~~~~~~~~~~~~~~~~~~~~

If you already know the technology and band, you can call the specific helpers.

.. code:: ts

   import {
     GSMBand,
     LTEBand,
     NRBand,
     gsmArfcnToFrequency,
     gsmFrequencyToArfcn,
     lteArfcnToFrequency,
     nrFrequencyToArfcn,
   } from '@osmoweb/core/radio';

   const gsm = gsmArfcnToFrequency(0, GSMBand.GSM_900);
   // -> { uplink: number, downlink: number } (kHz)

   const arfcn = gsmFrequencyToArfcn(935_200, GSMBand.GSM_900);

   const lte = lteArfcnToFrequency(1200, LTEBand.B3);

   const nrArfcn = nrFrequencyToArfcn(3_500_000, NRBand.N78);

.. _detection--ranges:

Detection & ranges
~~~~~~~~~~~~~~~~~~

.. code:: ts

   import {
     RadioTechnology,
     getSupportedBands,
     getBandArfcnRange,
     getBandFrequencyRange,
     detectGSMBandFromFrequency,
   } from '@osmoweb/core/radio';

   const lteBands = getSupportedBands(RadioTechnology.LTE);

   const gsm900Candidates = detectGSMBandFromFrequency(935_200);

   const range = getBandArfcnRange(RadioTechnology.GSM, gsm900Candidates[0]);
   const freqs = getBandFrequencyRange(RadioTechnology.GSM, gsm900Candidates[0]);

Osmo
----

``getJournalLogLevelFromOsmoLogLevel()``
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Maps Osmocom log levels (numeric) to ``JournalLogLevel`` from ``@websdr/core/utils``.

.. code:: ts

   import { getJournalLogLevelFromOsmoLogLevel } from '@osmoweb/core/osmo';

   const level = getJournalLogLevelFromOsmoLogLevel(7);
   // 7 (LOGL_ERROR) -> JournalLogLevel.ERROR

API overview
------------

Everything below is exported from ``@osmoweb/core/radio``:

-  Enums: ``RadioTechnology``, ``GSMBand``, ``LTEBand``, ``NRBand``
-  Types: ``MobileBand``, ``ARFCNConfigInput``, ``ARFCNConfig``, ``FrequencyResult``
-  Universal: ``configureARFCN()``, ``getSupportedBands()``, ``getBandArfcnRange()``, ``getBandFrequencyRange()``
-  GSM: ``gsmArfcnToFrequency()``, ``gsmFrequencyToArfcn()``, ``detectGSMBandFromFrequency()``, ``detectGSMBandFromArfcn()``, ``getGSMBandArfcnRange()``, ``getGSMBandFrequencyRange()``, ``getAllGSMBands()``
-  LTE: ``lteArfcnToFrequency()``, ``lteFrequencyToArfcn()``, ``detectLTEBandFromFrequency()``, ``detectLTEBandFromArfcn()``, ``getLTEBandArfcnRange()``, ``getLTEBandFrequencyRange()``, ``getAllLTEBands()``
-  NR: ``nrArfcnToFrequency()``, ``nrFrequencyToArfcn()``, ``detectNRBandFromFrequency()``, ``detectNRBandFromArfcn()``, ``getNRBandArfcnRange()``, ``getNRBandFrequencyRange()``, ``getAllNRBands()``

Everything below is exported from ``@osmoweb/core/osmo``:

-  ``getJournalLogLevelFromOsmoLogLevel()``

Compatibility notes
-------------------

-  **TypeScript:** ships ``*.d.ts`` typings.

Development (monorepo)
----------------------

From the repository root:

.. code:: bash

   npm install
   npm run build
   npm test --workspace=packages/core

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

-  Entry point: https://github.com/wavelet-lab/osmoweb/blob/main/packages/core/src/index.ts
-  Osmo utils exports: https://github.com/wavelet-lab/osmoweb/blob/main/packages/core/src/osmo/index.ts
-  Radio utils exports: https://github.com/wavelet-lab/osmoweb/blob/main/packages/core/src/radio/index.ts

Package folder (GitHub):
https://github.com/wavelet-lab/osmoweb/tree/main/packages/core

License
-------

OsmoWeb is `MIT licensed <https://github.com/wavelet-lab/osmoweb/blob/main/LICENSE>`__
