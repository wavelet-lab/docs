Test apps
=========

This folder contains **manual / hardware-in-the-loop test scripts** for the WebSDR monorepo.

Currently the main entry is `usb-test.ts <usb-test.ts#L1>`__ — a WebUSB smoke test that opens a device, runs RX streaming, then TX streaming.

Prerequisites
-------------

-  **Node.js + npm** installed.
-  A supported SDR device connected via USB.
-  **Permissions to access USB devices** on your OS.

   -  On Linux you might need udev rules (recommended) or to run with elevated privileges depending on your setup.

.. _usb-smoke-test-rx--tx:

USB smoke test (RX + TX)
------------------------

The script roughly does:

1. Ensure a WebUSB implementation exists (``ensureWebUsb()``).
2. Initialize control module (``initControl()``).
3. Request/select a USB device (``requestDevice()``).
4. Open the device and the control interface.
5. Run an RX streaming loop and print stats.
6. Run a TX streaming loop.
7. Close everything.

Run
~~~

From the repository root:

.. code:: bash

   cd test-apps
   npm install
   npm run test:usb

What you should see
~~~~~~~~~~~~~~~~~~~

-  Logs about selecting/opening the device.
-  ``RX stream started`` → packet stats → ``RX stream stopped``.
-  ``TX stream started`` → packet stats → ``TX stream stopped``.
-  Final ``USB test completed``.

Configuration
~~~~~~~~~~~~~

You can tune parameters by editing constants near the top of `usb-test.ts <usb-test.ts#L1>`__, for example:

-  ``packetSize``
-  ``rxConfig`` / ``txConfig`` (frequency, bandwidth, samplerate, gain)

Troubleshooting
~~~~~~~~~~~~~~~

-  **Permission denied / libusb errors**

   -  Ensure your user has access to the USB device.
   -  On Linux this typically means udev rules.

-  **Timeout waiting for packets**

   -  The RX test uses a finite safety timeout while waiting for in-flight packets.
   -  Check USB stability, device firmware, and that streaming is supported.

-  **No WebUSB implementation found**

   -  The underlying WebUSB layer attempts to use ``usb`` (preferred) or fall back to ``webusb``.
   -  Verify dependencies are installed and compatible with your platform.

.. _safety--regulatory-note-tx:

Safety / regulatory note (TX)
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

The TX part may cause RF transmission depending on your device and setup.
Only run TX tests if you understand your hardware chain and comply with local regulations (use appropriate shielding / dummy load where applicable).
