usdr_dm_create tool
===================

.. note::
   | You have to install ``usdr-tools`` package first.
   | Please refer to the :doc:`/software/install` document.


This tool is used to transmit a simple sinus waveform with a given frequency and power and/or
to receive and record a signal into a raw file as well as other testing purposes.

Transmission RF (signal generation)
-----------------------------------

The following commands will generate a simple sinus waveform with a given frequency.

* Limited by 10000 blocks of 4096 samples each of 800MHz and sample rate of 7MHz:

.. code-block:: bash

   usdr_dm_create -t -r7e6 -c10000 -l3 -E800e6

* Unlimited transmission(hit Ctrl+C to stop) on 900MHz and sample rate of 3MHz:

.. code-block:: bash

   usdr_dm_create -t -r3e6 -c-1 -l3 -E900e6

Receiving RF (signal recording)
-------------------------------

The following command will record 100000 blocks of 4096 samples each of a signal into
a raw file with center frequency of 1200Mhz a sample rate of 4MHz:

.. code-block:: bash

   usdr_dm_create -r4e6 -c100000 -l3 -e1200e6 -f output.raw

The output file will have ``int16`` complex pairs and can be visualized using ``nympy`` and ``matplotlib``.

Transmission RF (from a recorded file)
--------------------------------------

The following command will transmit a signal from a raw file with a sample rate of 1MHz and a center frequency of 1700MHz:

.. code-block:: bash

   usdr_dm_create -t -r1e6 -e1701e6 -E1700e6 -I ~/signal.ci16 -O 16384


List of available devices
-------------------------

.. code-block:: bash

   usdr_dm_create -Q

Available options
-----------------

* ``[-D device]`` - Path to the device
* ``[-f RX_filename [./out.data]]`` - Output file
* ``[-I TX_filename ]`` - Input file
* ``[-o <flag: cycle TX from file>]`` - Transmit from file in a loop
* ``[-c count [128]]`` - Number of blocks to transmit/receive
* ``[-r samplerate [50e6]]`` - Sample rate in Hz, for both TX and RX
* ``[-F format [ci16] | cf32]`` - Data format
* ``[-C chmsk [0x1]]``
* ``[-S TX samples_per_blk [4096]]`` - Number of samples per block for transmission
* ``[-O RX samples_per_blk [4096]]`` - Number of samples per block for receiving
* ``[-t <flag: TX only mode>]`` - Transmit only mode
* ``[-T <flag: TX+RX mode>]`` - Transmit and receive mode
* ``[-N <flag: No TX timestamps>]``
* ``[-q TDD_FREQ [910e6]]``
* ``[-e RX_FREQ [900e6]]`` - Center frequency in Hz for receiving
* ``[-E TX_FREQ [920e6]]`` - Center frequency in Hz for transmission
* ``[-w RX_BANDWIDTH [1e6]]`` - Bandwidth in Hz for receiving
* ``[-W TX_BANDWIDTH [1e6]]`` - Bandwidth in Hz for transmission
* ``[-y RX_GAIN_LNA [15]]`` - LNA gain
* ``[-Y TX_GAIN [0]]`` - TX gain
* ``[-p RX_PATH ([rx_auto]|rxl|rxw|rxh|adc|rxl_lb|rxw_lb|rxh_lb)]``
* ``[-P TX_PATH ([tx_auto]|txb1|txb2|txw|txh)]``
* ``[-u RX_GAIN_PGA [15]]`` - PGA gain
* ``[-U RX_GAIN_VGA [15]]`` - VGA gain
* ``[-a Reference clock path) []]``
* ``[-B Calibration freq [0]]``
* ``[-s Sync type [all]]``
* ``[-Q <flag: Discover and exit>]`` - Discover devices and exit
* ``[-i Resync iter [1]]``
* ``[-R RX_LML_MODE [0]]``
* ``[-A Antenna configuration [0]]``
* ``[-X <flag: Skip initialization>]``
* ``[-z <flag: Continue on error>]``
* ``[-l loglevel [3(INFO)]]`` - Set log level
* ``[-h <flag: This help>]`` - Print help
