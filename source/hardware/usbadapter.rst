===========
USB Adapter
===========

The USB adapter is a small board made easy to connect the uSDR via USB
as well as some additional features:

* Six GPIOs exposed to an FPC cable, along with 1.8 V
* TX harmonic-reduction filter for 2.3 - 3.7 GHz
* RX LPF at 3.5 GHz
* A connector for an external reference clock
* Exposed JTAG pads for a JTAG-HS2 adapter
* Mounting holes for a heatsink or enclosure

.. image:: ../_static/hw_usbadapter_1.jpg
   :alt: USB Adapter

Connections
-----------

* J7 - Harmonic Filter(2.3 - 3.7 GHz) - TX SMA
* J6 - Low Pass Filter(3.5 GHz) - RX SMA
* Central connector - direct to SMA: Usable to connect uSDR HF RX
