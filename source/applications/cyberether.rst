==========
CyberEther
==========

Installation
------------

.. note::

   This application needs SoapySDR plugin. Please refer to :doc:`/software/install`.

You have to build CyberEther from source with SoapySDR support.

Usage
-----

* Create a new floatgraph.
* Place ``Soapy`` block to the graph and select USDR from the device list.
* Place ``Scectroscope`` block to the graph. Set the Range Min parameter to -100.
* Connect the blocks together.

.. image:: ../_static/applications/cyberether_1.jpg
   :alt: CyberEther example of signal processing

* You should see the spectrum of the signal.

References
----------

* `CyberEther github <https://github.com/luigifcruz/CyberEther>`_
