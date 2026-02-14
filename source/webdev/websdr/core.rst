@websdr/core
============

Core TypeScript utilities for the WebSDR ecosystem: shared types/constants, small runtime helpers, and fast sample format conversions.

**What’s inside**

-  **Common:** shared types + size/format constants.
-  **Utils:** circular buffer, timing helpers, logging, promise helper, string helpers, journal types.
-  **Transform:** PCM buffer converters used by DSP pipelines.

Install
-------

.. code:: bash

   npm install @websdr/core

.. code:: bash

   pnpm add @websdr/core

.. code:: bash

   yarn add @websdr/core

Importing
---------

This package is published as ESM (see ``type: module``). Most users should import from the package root:

.. code:: ts

   import { CircularBuffer, SimpleLogger, bufferF32ToI16 } from '@websdr/core';

Subpath exports are also available (often better for clarity / tree-shaking):

.. code:: ts

   import { CircularBuffer } from '@websdr/core/utils';
   import { bufferI16ToF32 } from '@websdr/core/transform';
   import { CHUNK_SIZE, DataType } from '@websdr/core/common';

Examples
--------

CircularBuffer
~~~~~~~~~~~~~~

.. code:: ts

   import { CircularBuffer } from '@websdr/core/utils';

   const buf = new CircularBuffer<number>(4);
   buf.push_back(1);
   buf.push_back(2);

   console.log(buf.size());   // 2
   console.log(buf.front());  // 1
   console.log(buf.back());   // 2

Timing helpers
~~~~~~~~~~~~~~

.. code:: ts

   import { now, sleep, usleep } from '@websdr/core/utils';

   const t0 = now();
   await usleep(10); // ms
   await sleep(0.05); // seconds
   console.log('elapsed', now() - t0);

PCM conversions
~~~~~~~~~~~~~~~

.. code:: ts

   import { bufferF32ToI16, bufferI16ToF32, clipF32Buffer } from '@websdr/core/transform';

   const f32 = new Float32Array([0.0, 0.5, -0.5]);

   // Optional: clip before converting if your pipeline can produce out-of-range values
   clipF32Buffer(f32);

   const i16 = bufferF32ToI16(f32);
   const f32roundtrip = bufferI16ToF32(i16);

If you want to avoid allocations in a hot path, reuse an output buffer:

.. code:: ts

   import { bufferF32ToI16 } from '@websdr/core/transform';

   const out = new Int16Array(8192);

   function onAudioFrame(frame: Float32Array) {
     // Converts up to min(frame.length, out.length)
     bufferF32ToI16(frame, out);
     return out;
   }

Common constants and types
~~~~~~~~~~~~~~~~~~~~~~~~~~

.. code:: ts

   import { CHUNK_SIZE, COMPLEX_FLOAT_SIZE, DataType } from '@websdr/core/common';

   const streamType: DataType = DataType.cf32;
   const bytesPerChunk = CHUNK_SIZE * COMPLEX_FLOAT_SIZE;
   console.log({ streamType, bytesPerChunk });

Logging
~~~~~~~

.. code:: ts

   import { SimpleLogger } from '@websdr/core/utils';

   const logger = new SimpleLogger('websdr');
   logger.log('hello');
   logger.warn('something odd');
   logger.error('something bad');

PromiseHelper (request/response correlation)
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Useful when you send requests that later resolve from an event handler.

.. code:: ts

   import { PromiseHelper } from '@websdr/core/utils';

   const promises = new PromiseHelper();

   function sendRequest(payload: unknown) {
     const [id, promise] = promises.createPromise<{ ok: boolean }>();
     transport.send({ id, payload });
     return promise;
   }

   transport.on('message', (msg: { id: number; result?: unknown; error?: unknown }) => {
     const entry = promises.getPromise(msg.id);
     if (!entry) return;
     promises.deletePromise(msg.id);
     if (msg.error) promises.promiseReject(entry, msg.error);
     else promises.promiseResolve(entry, msg.result);
   });

Filtering helpers
~~~~~~~~~~~~~~~~~

.. code:: ts

   import { containsAnySubstr, stringToBoolean } from '@websdr/core/utils';

   const enabled = stringToBoolean(process.env.DEBUG);
   const allow = containsAnySubstr('usb:device connected', ['usb:', 'webusb'], false);
   console.log({ enabled, allow });

Journal log items
~~~~~~~~~~~~~~~~~

.. code:: ts

   import { JournalLogLevel, timestampToTimeString } from '@websdr/core/utils';
   import type { JournalLogItem } from '@websdr/core/utils';

   const item: JournalLogItem = {
     timestamp: Date.now(),
     subSystem: 'webusb',
     logLevel: JournalLogLevel.INFO,
     message: 'device opened',
   };

   console.log(`[${timestampToTimeString(item.timestamp)}] ${item.subSystem}: ${item.message}`);

Public API (summary)
--------------------

-  **``@websdr/core/common``**: ``DataType``, ``CHUNK_SIZE``, ``FLOAT_SIZE``, ``COMPLEX_FLOAT_SIZE``, ``INT16_SIZE``, ``COMPLEX_INT16_SIZE``.
-  **``@websdr/core/utils``**:

   -  ``CircularBuffer``
   -  ``sleep``, ``usleep``, ``now``, ``timestampToTimeString``
   -  ``PromiseHelper``
   -  ``JournalLogLevel``, ``JournalLogLevelKeys``, ``JournalLogItem``
   -  ``SimpleLogger``, ``LOG_LEVELS``, ``LoggerInterface``, ``LogLevel``
   -  ``stringToBoolean``, ``containsAnySubstr``

-  **``@websdr/core/transform``**: ``bufferF32ToI16``, ``bufferI16ToF32``.
-  **``@websdr/core/transform``**: ``bufferF32ToI16``, ``bufferI16ToF32``, ``clipF32Buffer``.

Compatibility notes
-------------------

-  **TypeScript:** ships ``*.d.ts`` typings.
-  **Runtime:** uses ``performance.now()`` in ``now()``. In browsers this is always available; in Node.js it depends on your Node version / environment.

Development
-----------

From the repository root:

.. code:: bash

   npm install

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

-  Entry point: https://github.com/wavelet-lab/websdr/blob/main/packages/core/src/index.ts
-  Common exports: https://github.com/wavelet-lab/websdr/blob/main/packages/core/src/common/index.ts
-  Utils exports: https://github.com/wavelet-lab/websdr/blob/main/packages/core/src/utils/index.ts
-  Transform exports: https://github.com/wavelet-lab/websdr/blob/main/packages/core/src/transform/index.ts

Package folder (GitHub):
https://github.com/wavelet-lab/websdr/tree/main/packages/core

License
-------

MIT — see `LICENSE <LICENSE>`__
