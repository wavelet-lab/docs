=================
Flashing firmware
=================

.. note::

   You can also update the firmware using web platform.

Instruction
-----------

.. note::
   | You have to install ``usdr-tools`` package first.
   | Please refer to the :doc:`/software/install` document.

* Connect the uSDR module to the computer using a USB adapter or Development board (Both PCIe and USB-C options are supported)
* Download the required firmware file.
* Open a terminal and run the following command:

.. code-block:: bash

   usdr_flash -w <firmware_file>

* Wait for the process to complete.
* **WARNING**: Please do not disconnect the device during the flashing process.
* When flashing is complete, perform a "power cycle" of the device (reconnect it)

Firmwares
---------

You can download the firmware files from the `firmwares <https://github.com/wavelet-lab/firmwares>`_ repository.

Example
-------

.. code-block:: bash

   root@raspberry:~# usdr_flash -w usdr_top_all.bin
   Device was created: `usb@3/1/2`!
   Flash ID id 1f16421f (Adesto SPI/QPI series 32 Mb)!
   Actual firmware in use:      FirmwareID a2b0b731 (20240520112849)
   Golden image: DEVID 0362d093 FirmwareID 29b02372 (20240305021350)
   Master image: DEVID 0362d093 FirmwareID a2b0b731 (20240520112849)
   Writing 1310720 bytes at 001c0000; flash(G/M) = 29b02372/a2b0b731 [1] new = aab135c4 current = a2b0b731 { flash(G/M) = 20240305021350/20240520112849 new = 20240521192304 current = 20240520112849 } !
   Reading 1310720 bytes!
   Write successful!
