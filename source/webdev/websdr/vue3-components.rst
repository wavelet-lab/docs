@websdr/vue3-components
=======================

Vue 3 UI components for the WebSDR ecosystem (Dropdown, virtualized List, LogArea, SdrInput) with customizable styling via CSS variables.

Install
-------

.. code:: bash

   npm install @websdr/vue3-components

.. code:: bash

   pnpm add @websdr/vue3-components

.. code:: bash

   yarn add @websdr/vue3-components

Importing
---------

Import from the root:

.. code:: ts

   import { Dropdown, DropdownOption, List, LogArea, SdrInput } from '@websdr/vue3-components';

Or from subpaths:

.. code:: ts

   import { Dropdown, List } from '@websdr/vue3-components/components';
   import { calculateDisplayItems } from '@websdr/vue3-components/utils';

Styles
------

Import the compiled CSS (recommended):

.. code:: ts

   import '@websdr/vue3-components/styles/index.css';

You can also import per-component CSS:

.. code:: ts

   import '@websdr/vue3-components/styles/dropdown.css';
   import '@websdr/vue3-components/styles/list.css';

Styling is based on CSS custom properties (variables). Override them in your app’s CSS to match your design system.

Components
----------

Dropdown
~~~~~~~~

**Usage:**

.. code:: vue

   <template>
       <div>
           <!-- Dropdown -->
           <Dropdown
               v-model="selectedValue"
               placeholder="Choose option"
               :clearable="true"
           >
               <template #content="{ close, updateSelection }">
                   <DropdownOption
                       v-for="option in options"
                       :key="option.value"
                       :value="option.value"
                       :label="option.label"
                       :selected="selectedValue === option.value"
                       @select="(value) => { updateSelection(value); close(); }"
                   />
               </template>
           </Dropdown>

           <!-- Dropdown with search -->
           <Dropdown
               v-model="searchableValue"
               :searchable="true"
               size="large"
               variant="outlined"
           >
               <template #content="{ close, searchQuery, updateSelection }">
                   <DropdownOption
                       v-for="option in filteredOptions(searchQuery)"
                       :key="option.value"
                       :value="option.value"
                       :label="option.label"
                       :description="option.description"
                       :selected="searchableValue === option.value"
                       @select="(value) => { updateSelection(value); close(); }"
                   />
               </template>
           </Dropdown>

           <!-- Multiple selection -->
           <Dropdown
               v-model="multipleValues"
               :multiple="true"
               :clearable="true"
           >
               <template #content="{ updateSelection, selectedValues }">
                   <DropdownOption
                       v-for="option in options"
                       :key="option.value"
                       :value="option.value"
                       :label="option.label"
                       :selected="selectedValues.includes(option.value)"
                       @select="(value) => {
                           const newValues = selectedValues.includes(value)
                               ? selectedValues.filter(v => v !== value)
                               : [...selectedValues, value];
                           updateSelection(newValues);
                       }"
                   />
               </template>
           </Dropdown>
       </div>
   </template>

List
~~~~

A performant, virtualized list component with optional auto-scroll behavior. ``List`` renders only visible rows into the DOM and uses a spacer + translated window to provide a full scrollable experience even for very large datasets.

Key features:

-  Supports both in-memory arrays (``items``) and on-demand access via ``getItem`` + ``totalCount`` for very large lists.
-  Optional fixed ``itemHeight`` or automatic measurement when ``itemHeight`` is ``0`` (uses ``ResizeObserver`` and averages several visible rows).
-  Virtual buffer above/below the viewport to reduce popping during scrolls.
-  Optional ``autoScroll`` that keeps the view pinned to the bottom (useful for logs/chat) and pauses when the user scrolls away.
-  Simple slot-based rendering: the default slot receives ``{ item, index }`` for each visible row.

**Usage (in-memory items):**

.. code:: vue

   <template>
     <List :items="items" :itemHeight="40" :autoScroll="false" maxHeight="300px">
       <template #default="{ item, index }">
         <div class="my-row">{{ index }} — {{ item.text }}</div>
       </template>
     </List>
   </template>

   <script setup>
   import { ref } from 'vue'
   import { List } from '@websdr/vue3-components'

   const items = ref(Array.from({ length: 1000 }, (_, i) => ({ text: `Item ${i}` })))
   </script>

**Usage (on-demand getter for huge lists):**

.. code:: vue

   <template>
     <List :totalCount="total" :getItem="getItem" :itemHeight="24" maxHeight="400px">
       <template #default="{ item, index }">
         <div class="my-row">{{ index }} — {{ item }}</div>
       </template>
     </List>
   </template>

   <script setup lang="ts">
   import { ref } from 'vue'
   import { List } from '@websdr/vue3-components'

   const total = 1_000_000
   function getItem(i: number) {
     // return item on-demand (synchronous getter expected by the component)
     return `Row #${i}`
   }
   </script>

**Props:**

-  ``items?: Array<T>`` — optional full array source (when present ``getItem`` / ``totalCount`` are ignored).
-  ``totalCount?: number`` — optional total count when using ``getItem`` (required for on-demand access).
-  ``getItem?: (index: number) => T`` — optional synchronous getter used to access items on-demand.
-  ``itemHeight?: number`` — height in px of each row. ``0`` means auto-measure (component will measure rendered items). If unset or ``0``, fallback/initial estimate is 25px until measured.
-  ``virtualBuffer?: number`` — rows above/below viewport to render as buffer (default: 5).
-  ``maxHeight?: string`` — maximum height for the list (e.g. ``"200px"`` or ``"50%"``) (default: ``"100%"``).
-  ``class?: string`` — additional class for the root container.
-  ``style?: Record<string, any>`` — additional inline styles for the root container.
-  ``autoScroll?: boolean`` — when ``true``, the list will auto-scroll to the bottom when new items are appended (default: ``false``). Auto-scroll pauses while the user scrolls away from the bottom, and resumes when scrolled back.

**Slot:**

-  Default slot receives ``{ item, index }`` for each visible row. Use this to render each item.

**Behavior / Notes:**

-  The component places a transparent spacer element with the full ``totalHeight`` so native scrolling works as if all rows are rendered.
-  Visible rows are rendered inside an absolutely-positioned window translated by ``translateY(offset)``.
-  If ``itemHeight`` is ``0`` (auto-measure), ``ResizeObserver`` measures several visible children (up to 8) and uses the average as the measured row height.
-  When using ``getItem``, provide a correct ``totalCount`` and a synchronous ``getItem`` function — the component expects immediate values, not promises.
-  ``autoScroll`` will only scroll programmatically when new items increase ``totalCount``, and it respects a small bottom threshold to avoid jumps.
-  There are no custom events emitted by the component; interaction is done via props/slot and standard DOM scroll behavior.

LogArea
~~~~~~~

A log viewer component with filtering capabilities, virtual scrolling, and real-time updates.

**Features:**

-  Virtual scrolling for performance with large datasets
-  Filter by log level (fatal, error, warning, info, debug)
-  Filter by subsystem
-  Search functionality
-  Clear logs action
-  Dark theme support

**Usage:**

.. code:: vue

   <template>
     <LogArea
       :logs="logs"
       :subsystems="subsystems"
       @clear-logs="handleClearLogs"
     />
   </template>

   <script setup>
   import { LogArea } from '@websdr/vue3-components'

   const logs = ref([
     {
       id: 1,
       timestamp: '2025-09-14T10:30:00Z',
       level: 'info',
       subsystem: 'core',
       message: 'Application started'
     }
   ])

   const subsystems = ref(['core', 'network', 'ui'])

   function handleClearLogs() {
     logs.value = []
   }
   </script>

**Props:**

-  ``logs`` (Array): Array of log objects with ``id``, ``timestamp``, ``level``, ``subsystem``, ``message``
-  ``subsystems`` (Array): Available subsystems for filtering
-  ``itemHeight`` (Number): Height of each log item in pixels (default: 24)
-  ``bufferSize`` (Number): Number of items to render outside visible area (default: 10)

**Events:**

-  ``clear-logs``: Emitted when clear button is clicked

SdrInput
~~~~~~~~

A lightweight SDR (Software Defined Radio) selector with an input-like appearance. The component wraps a ``Dropdown`` trigger and uses the WebUSB manager to request/select SDR devices.

Key points:

-  Shows the currently selected device name (or a placeholder when none is selected).
-  Opens the WebUSB device picker when the dropdown is opened.
-  Emits an update event with the selected device info so the parent can react.

**Usage:**

.. code:: vue

   <template>
     <SdrInput
       v-model:device="sdrDevice"
       mode="single"
       placeholder="Click to select SDR"
       :disabled="isProcessing"
       size="medium"
     />
   </template>

   <script setup lang="ts">
   import { ref } from 'vue'
   import { SdrInput, type RequestDeviceInfo } from '@websdr/vue3-components'

   const sdrDevice = ref<RequestDeviceInfo | undefined>(undefined)
   const isProcessing = ref(false)

   // sdrDevice will be updated when the user selects a device in the picker
   </script>

**Props:**

-  ``device`` (RequestDeviceInfo \| undefined) — Currently selected SDR device. Shape: ``{ devName: string, vendorId: number, productId: number }``.
-  ``mode?: 'single' | 'worker'`` — WebUsb manager mode. Defaults to ``'single'``.
-  ``placeholder?: string`` — Placeholder text when no device is selected. Defaults to ``'Click to select SDR'``.
-  ``size?: DropdownProps['size']`` — Visual size of the input (passes through to ``Dropdown``). Defaults to ``'medium'``.
-  ``disabled?: boolean`` — When true the input is disabled. Defaults to ``false``.

**Emits:**

-  ``update:device`` (RequestDeviceInfo) — Standard Vue event for ``v-model:device``.

**Behavior / Notes:**

-  When opened the component calls the WebUSB manager (``getWebUsbManagerInstance``) to request a device.
-  If a device is returned it becomes the selected device and ``update:device`` is emitted with the ``RequestDeviceInfo``.
-  If the picker is cancelled the component emits an empty device object (fields set to empty/0) to indicate no selection.
-  The visual status (error/success) is derived from whether a device name is present.

**Defaults**

-  ``mode``: ``'single'``
-  ``placeholder``: ``'Click to select SDR'``
-  ``disabled``: ``false``
-  ``size``: ``'medium'``

Styling
-------

All components are designed for maximum customization using CSS custom properties (variables). This allows you to easily integrate them with your existing design system or CSS framework.

Quick Start
~~~~~~~~~~~

Import the compiled CSS entry (recommended for npm consumers):

.. code:: ts

   import '@websdr/vue3-components/styles/index.css';

If you need to customize via CSS variables, define overrides in your application stylesheet (no Sass required). The sections below list the available variables.

Component Customization
~~~~~~~~~~~~~~~~~~~~~~~

Each component exposes specific CSS variables for granular control:

LogArea Component Variables
^^^^^^^^^^^^^^^^^^^^^^^^^^^

.. code:: scss

   :root {
     /* Log level colors (customizable) */
     --log-fatal-color: darkred;
     --log-error-color: red; 
     --log-warning-color: rgb(190, 124, 0);
     --log-info-color: black;
     --log-debug-color: blue;

     /* Layout variables (customizable) */
     --logarea-filter-bg: var(--light, #f8f9fa);
     --logarea-filter-padding: var(--input-padding, 12px);
     --logarea-filter-gap: 1rem;
     --logarea-item-padding: 0.5rem;

     /* Typography variables (customizable) */
     --logarea-item-font-family: ui-monospace, SFMono-Regular, Monaco, 'Courier New', monospace;
     --logarea-item-font-size: var(--input-font-size, 14px);
     --logarea-item-line-height: 1rem;
   }

Dropdown Component Variables
^^^^^^^^^^^^^^^^^^^^^^^^^^^^

.. code:: scss

   :root {
     /* Container variables (customizable) */
     --dropdown-bg: var(--white, #ffffff);
     --dropdown-border: var(--input-border, 1px solid #d1d5db);
     --dropdown-border-radius: var(--input-border-radius, 6px);
     --dropdown-shadow: var(--shadow, 0 10px 15px -3px rgba(0, 0, 0, 0.1));
     --dropdown-padding: var(--input-padding, 8px 12px);

     /* State variables (customizable) */
     --dropdown-focus-border: var(--input-focus-border, #3b82f6);
     --dropdown-focus-shadow: var(--input-focus-shadow, 0 0 0 3px rgba(59, 130, 246, 0.1));
     
     /* Option variables (customizable) */
     --dropdown-item-hover-bg: var(--light, #f3f4f6);
     --dropdown-item-active-bg: var(--primary-color, #3b82f6);
     --dropdown-option-selected-bg: var(--primary-light, #eff6ff);
     --dropdown-option-selected-text: var(--primary-color, #3b82f6);
   }

SdrInput Component Variables
^^^^^^^^^^^^^^^^^^^^^^^^^^^^

.. code:: scss

   :root {
     /* Uses base variables from variables.scss */
     /* Status indicator colors */
     --success-color: #28a745;  /* Connected state */
     --danger-color: #dc3545;   /* Disconnected state */
     --primary-color: #007bff;  /* Configured state */
     --muted: #6c757d;          /* Empty state text */
   }

Base Variables
~~~~~~~~~~~~~~

Core design tokens available for all components:

.. code:: scss

   :root {
     /* === PRIMARY COLOR PALETTE === */
     --primary-color: #007bff;
     --primary-hover: #0056b3;
     --primary-light: #cce7ff;
     --secondary-color: #6c757d;
     --secondary-hover: #545b62;
     --success-color: #28a745;
     --success-hover: #218838;
     --warning-color: #ffc107;
     --warning-hover: #e0a800;
     --danger-color: #dc3545;
     --danger-hover: #c82333;
     --info-color: #17a2b8;

     /* === NEUTRAL COLORS === */
     --white: #ffffff;
     --light: #f8f9fa;
     --dark: #495057;
     --muted: #6c757d;
     --border: #ced4da;
     --border-light: #dee2e6;
     --border-dark: #495057;
     --disabled-bg: #e9ecef;
     --text-muted: #6c757d;
     --text-light: #9ca3af;

     /* === FORM ELEMENT VARIABLES === */
     --input-padding: 12px;
     --input-border-radius: 6px;
     --input-font-size: 14px;
     --input-border: 1px solid var(--border);
     --input-focus-border: #80bdff;
     --input-focus-shadow: 0 0 0 0.2rem rgba(0, 123, 255, 0.25);
     --input-transition: border-color 0.15s ease-in-out, box-shadow 0.15s ease-in-out;

     /* === BUTTON VARIABLES === */
     --button-padding: 12px 24px;
     --button-border-radius: 6px;
     --button-font-size: 14px;
     --button-font-weight: 600;
     --button-transition: background-color 0.15s ease-in-out;

     /* === SHADOW VARIABLES === */
     --shadow-sm: 0 2px 4px rgba(0, 0, 0, 0.1);
     --shadow-md: 0 2px 10px rgba(0, 0, 0, 0.1);
     --shadow-lg: 0 10px 30px rgba(0, 0, 0, 0.3);
     --shadow: var(--shadow-md);

     /* === Z-INDEX LEVELS === */
     --z-dropdown: 1000;
     --z-modal: 1050;

     /* === RESPONSIVE BREAKPOINTS === */
     --mobile-breakpoint: 768px;

     /* === ANIMATION TIMING === */
     --transition-fast: 0.15s ease-in-out;
     --transition-normal: 0.2s ease;
     --transition-slow: 0.3s ease;
   }

Dark Theme Support
~~~~~~~~~~~~~~~~~~

Enable dark theme by adding ``data-theme="dark"`` attribute or ``theme-dark`` class:

.. code:: html

   <div data-theme="dark">
     <LogArea :logs="logs" />
     <Dropdown v-model="value" />
   </div>

Dark theme automatically overrides variables:

.. code:: scss

   [data-theme="dark"],
   .theme-dark {
     --white: #1f232b;
     --light: #2a2f3a;
     --dark: #f8f9fa;
     --muted: #9aa4b2;
     --border: #3a4149;
     --border-light: #2a2f3a;
     
     /* Component-specific dark theme overrides */
     --log-fatal-color: rgb(201, 0, 0);
     --log-error-color: rgb(255, 78, 78);
     --log-warning-color: rgb(238, 155, 0);
     --log-info-color: lightgray;
     --log-debug-color: rgb(0, 191, 255);
     
     --dropdown-shadow: 0 10px 15px -3px rgba(0, 0, 0, 0.5);
   }

Framework Integration Examples
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Integration with Bulma CSS
^^^^^^^^^^^^^^^^^^^^^^^^^^

.. code:: scss

   :root {
     /* Use Bulma's color system */
     --primary-color: hsl(171, 100%, 41%);
     --primary-hover: hsl(171, 100%, 35%);
     --danger-color: hsl(348, 86%, 61%);
     --success-color: hsl(141, 53%, 53%);
     --warning-color: hsl(48, 100%, 67%);
     
     /* Use Bulma's sizing */
     --input-font-size: 1rem;
     --button-font-size: 1rem;
     --input-border-radius: 4px;
   }

Integration with Tailwind CSS
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

.. code:: scss

   :root {
     /* Use Tailwind color palette */
     --primary-color: theme('colors.blue.500');
     --primary-hover: theme('colors.blue.600');
     --success-color: theme('colors.green.500');
     --warning-color: theme('colors.yellow.500');
     --danger-color: theme('colors.red.500');
     
     /* Use Tailwind spacing and border radius */
     --input-padding: theme('spacing.3');
     --button-padding: theme('spacing.2') theme('spacing.4');
     --input-border-radius: theme('borderRadius.md');
   }

Advanced Customization Examples
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Custom Log Colors and Typography
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

.. code:: scss

   :root {
     /* Custom monospace font for logs */
     --logarea-item-font-family: 'Fira Code', 'JetBrains Mono', monospace;
     --logarea-item-font-size: 13px;
     
     /* Custom log level colors */
     --log-fatal-color: #ff0000;
     --log-error-color: #ff6b6b;
     --log-warning-color: #feca57;
     --log-info-color: #48dbfb;
     --log-debug-color: #ff9ff3;
     
     /* Custom filter background */
     --logarea-filter-bg: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
   }

Corporate Branding
^^^^^^^^^^^^^^^^^^

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
^^^^^^^^^^^^^^^^^^^

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

-  Entry point: https://github.com/wavelet-lab/websdr/blob/main/packages/vue3-components/src/index.ts
-  Components exports: https://github.com/wavelet-lab/websdr/blob/main/packages/vue3-components/src/components/index.ts
-  Styles entry (SCSS): https://github.com/wavelet-lab/websdr/blob/main/packages/vue3-components/src/styles/index.scss
-  Utils exports: https://github.com/wavelet-lab/websdr/blob/main/packages/vue3-components/src/utils/index.ts

Package folder (GitHub):
https://github.com/wavelet-lab/websdr/tree/main/packages/vue3-components

License
-------

WebSDR is `MIT licensed <https://github.com/wavelet-lab/websdr/blob/main/LICENSE>`__
