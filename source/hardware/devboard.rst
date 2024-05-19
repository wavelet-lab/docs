======================
uSDR Development Board
======================

This board was designed for developers and advanced users.
It has USB Type-C connectors and can be plugged into a computer with a PCIe x4 slot.
It provides the following features:

* A very simple radio fronted that allows you to prototype using the 2.4-GHz ISM band
* Duplexer for common cellular bands
* Increased TX power
* Increased RX sensitivity
* Extended automatic gain control (AGC)
* More precise clock synchronization thanks to a GNSS module.
* Mounting holes for a heatsink or enclosure

.. image:: ../_static/hw_devboard_1.jpg
   :alt: The development board

Technical Specifications
------------------------

* GPSDO: GNSS module + 12-bit DAC for VCTCXO
* GPIO: 12 GPIOs in six banks with different voltage levels (1.8 - 5 V)
* USB Type-C: 5 V, 3 A (USB 3.0 lines routed, currently without gateware support)
* RF filters:
    * 3.0 - 3.8 GHz
    * 2.1 - 3.0 GHz (ISM, Wi-Fi, Bluetooth, Zigbee)
    * 0 - 2.1 GHz
    * 0 - 1.2 GHz
* TX filters:
    * 0 - 3.8 GHz
    * 0 - 2.1 GHz
    * 0 - 1.2 GHz
* LNA/PGA: MiniCircuits PGA-103+

.. image:: ../_static/hw_devboard_2.svg
   :alt: The development board: block diagram

Installation
------------

The development board comes with a factory setup after testing.
To use the full potential of the board, some cable re-routing needs to be applied.

* Plug in the uSDR using a thin thermal interface in between.
* Gently unplug the cables from connectors J20 and J19.

.. image:: ../_static/hw_devboard_3.jpg
   :alt: The development board: default wiring

* Use your MHF4 - MHF4 jumpers to connect the uSDR RX/TX to J20 and J19.
* The two available SMA cables can be plugged into the uSDR HF connector and the 1PPS connector (see the picture).

.. image:: ../_static/hw_devboard_4.jpg
   :alt: The development board: uSDR rewiring

* Apply a thicker thermal interface (2.0 mm) and the heatsink as described in the ‘Heatsink Installation’ chapter.
* Here is the final SMA schematic on the panel.

.. image:: ../_static/hw_devboard_5.jpg
   :alt: The development board: final wiring

.. note::

    If you on’t need to use the development board,
    you can route SMA cables directly to the uSDR connectors in the order you want.
