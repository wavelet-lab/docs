@osmoweb/vue3-components
========================

Vue 3 UI components used by OsmoWeb.

This package currently exports BTS configuration components:

-  ``BtsInput`` — input-like dropdown wrapper
-  ``BtsConfig`` — configuration form

Installation
------------

.. code:: bash

   npm install @osmoweb/vue3-components

Imports
-------

.. code:: ts

   import { BtsInput, BtsConfig } from '@osmoweb/vue3-components';
   // or
   import { BtsInput, BtsConfig } from '@osmoweb/vue3-components/components';

Components
----------

BtsInput
~~~~~~~~

An input-like component that shows the current BTS config and opens a dropdown with ``BtsConfig``.

.. code:: vue

   <template>
     <BtsInput
       :bts="bts"
       :supported-technologies="supportedTechnologies"
       :bts-state="btsState"
       placeholder="Click to configure BTS"
       :disabled="disabled"
       :searchable="true"
       @update="onUpdate"
       @cancel="onCancel"
     />
   </template>

   <script setup lang="ts">
   import { ref } from 'vue';
   import { BtsInput, RadioTechnology } from '@osmoweb/vue3-components';
   import type { BtsParams, BtsState } from '@osmoweb/vue3-components';

   const bts = ref<BtsParams>({
     technology: RadioTechnology.GSM,
     band: 'GSM_900',
     arfcn: 100,
   });

   const supportedTechnologies = [RadioTechnology.GSM, RadioTechnology.LTE];

   const btsState = ref<BtsState>('configured');
   const disabled = ref(false);

   function onUpdate(config: BtsParams) {
     bts.value = config;
   }

   function onCancel() {
     // dropdown was closed via cancel
   }
   </script>

**Props**

-  ``bts?: BtsParams``
-  ``supportedTechnologies?: Array<RadioTechnology>``
-  ``placeholder?: string``
-  ``size?: 'small' | 'medium' | 'large'`` (re-exported as ``SizeType``)
-  ``btsState?: 'not-configured' | 'configured' | 'connected' | 'disconnected'``
-  ``disabled?: boolean``
-  ``searchable?: boolean``

**Events**

-  ``update(config: BtsParams)``
-  ``cancel()``

BtsConfig
~~~~~~~~~

Configuration form for technology/band/ARFCN with frequency preview (uses ``@osmoweb/core/radio``).

.. code:: vue

   <template>
     <BtsConfig
       :bts="bts"
       :supported-technologies="supportedTechnologies"
       :searchable="true"
       @submit="onSubmit"
       @cancel="onCancel"
     />
   </template>

   <script setup lang="ts">
   import { ref } from 'vue';
   import { BtsConfig, RadioTechnology } from '@osmoweb/vue3-components';
   import type { BtsParams } from '@osmoweb/vue3-components';

   const bts = ref<BtsParams>({
     technology: RadioTechnology.GSM,
     band: 'GSM_900',
     arfcn: 100,
   });

   const supportedTechnologies = [RadioTechnology.GSM, RadioTechnology.LTE, RadioTechnology.NR];

   function onSubmit(config: BtsParams) {
     bts.value = config;
   }

   function onCancel() {
     // close parent UI
   }
   </script>

**Props**

-  ``bts?: BtsParams``
-  ``supportedTechnologies?: Array<RadioTechnology>`` (defaults to ``[RadioTechnology.GSM]``)
-  ``searchable?: boolean``

**Events**

-  ``submit(config: BtsParams)``
-  ``cancel()``

Styles
------

Styles are published as compiled CSS and exported via the ``./styles/*`` subpath.

.. code:: ts

   import '@osmoweb/vue3-components/styles/variables.css';
   import '@osmoweb/vue3-components/styles/index.css';
   // or import only what you need:
   // import '@osmoweb/vue3-components/styles/bts-input.css';
   // import '@osmoweb/vue3-components/styles/bts-config.css';

To theme components, override the CSS custom properties defined in ``variables.css`` in your app’s global CSS.

Corporate Branding
~~~~~~~~~~~~~~~~~~

.. code:: scss

   :root {
     /* Corporate colors */
     --primary-color: #1e40af;        /* Corporate blue */
     --primary-hover: #1e3a8a;
     --success-color: #059669;        /* Corporate green */
     --warning-color: #d97706;        /* Corporate orange */
     --danger-color: #dc2626;         /* Corporate red */
     
     /* Corporate typography */
     --input-font-size: 15px;
     --button-font-weight: 700;
     
     /* Corporate spacing */
     --input-padding: 16px;
     --button-padding: 16px 32px;
     --input-border-radius: 8px;
     --button-border-radius: 8px;
     
     /* Corporate shadows */
     --shadow-md: 0 4px 6px -1px rgba(0, 0, 0, 0.1), 0 2px 4px -1px rgba(0, 0, 0, 0.06);
   }

Minimal/Flat Design
~~~~~~~~~~~~~~~~~~~

.. code:: scss

   :root {
     /* Remove shadows and borders for flat design */
     --shadow-sm: none;
     --shadow-md: none;
     --shadow-lg: none;
     --input-border: 1px solid transparent;
     --input-focus-shadow: none;
     --dropdown-shadow: none;
     
     /* Flat colors */
     --input-focus-border: var(--primary-color);
     --dropdown-border: 1px solid var(--border-light);
     
     /* Sharp corners */
     --input-border-radius: 0;
     --button-border-radius: 0;
     --dropdown-border-radius: 0;
   }

Component-Level Overrides
~~~~~~~~~~~~~~~~~~~~~~~~~

You can also override styles at the component level:

.. code:: vue

   <template>
     <div class="custom-log-area">
       <LogArea :logs="logs" />
     </div>
   </template>

   <style scoped>
   .custom-log-area {
     /* Override only for this instance */
     --log-error-color: #e74c3c;
     --log-warning-color: #f39c12;
     --logarea-item-font-size: 12px;
   }
   </style>

CSS Class Overrides
~~~~~~~~~~~~~~~~~~~

For complete control, you can also override CSS classes:

.. code:: scss

   /* Global overrides */
   .log-area {
     border: 2px solid var(--primary-color);
     
     .filter {
       background: var(--primary-color);
       color: white;
     }
     
     .log-area-item {
       &:hover {
         background-color: var(--light);
       }
     }
   }

   .dropdown-trigger {
     border: 2px solid var(--border);
     
     &:focus {
       border-color: var(--primary-color);
       outline: 2px solid var(--primary-color);
       outline-offset: 2px;
     }
   }

This approach ensures that your components integrate seamlessly with any design system while maintaining consistent behavior and accessibility.

Compatibility notes
-------------------

-  **TypeScript:** ships ``*.d.ts`` typings.

Development (monorepo)
----------------------

From the repository root:

.. code:: bash

   npm install
   npm run build
   npm test --workspace=packages/vue3-components

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

-  Entry point: https://github.com/wavelet-lab/osmoweb/blob/main/packages/vue3-components/src/index.ts
-  Osmo components exports: https://github.com/wavelet-lab/osmoweb/blob/main/packages/vue3-components/src/components/index.ts
-  Common utils exports: https://github.com/wavelet-lab/osmoweb/blob/main/packages/vue3-components/src/utils/index.ts
-  Styles exports: https://github.com/wavelet-lab/osmoweb/blob/main/packages/vue3-components/src/styles/index.scss

Package folder (GitHub):
https://github.com/wavelet-lab/osmoweb/tree/main/packages/vue3-components

License
-------

OsmoWeb is `MIT licensed <https://github.com/wavelet-lab/osmoweb/blob/main/LICENSE>`__
