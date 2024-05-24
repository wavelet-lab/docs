========
GNURadio
========

Installation
------------

.. note::

   This application needs SoapySDR plugin. Please refer :doc:`/software/install` for installation instructions.


.. code-block:: bash

   sudo apt install gnuradio

Usage
-----

In order to use USDR with GNURadio, you have to use "osmocom Source" block with the following Device Arguments.

.. code-block:: text

   "soapy,driver=usdr"

.. image:: ../_static/applications/gnuradio_1.jpg
   :alt: GNURadio source settings

Now you can create a simple FM receiver like shown on the following screenshot.

.. image:: ../_static/applications/gnuradio_2.jpg
   :alt: GNURadio fm receiver

And start listening to the radio.

.. image:: ../_static/applications/gnuradio_3.jpg
   :alt: GNURadio fm receiver in action

You can download the example file :download:`here <../_static/applications/gnuradio_example_1.grc>`.

References
----------

* `GNURadio website <https://www.gnuradio.org>`_
