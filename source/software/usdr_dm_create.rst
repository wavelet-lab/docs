usdr_dm_create tool
===================

.. note::
   | You have to install ``usdr-tools`` package first.
   | Please refer to the :doc:`/software/install` document.


This tool is used to transmit a simple sinus waveform with a given frequency and power and/or
to receive and record a signal into a raw file as well as other testing purposes.

Newbie glossary
---------------

Here you can find the key concepts and terms to understand the options below.
Most options have reasonable default values, but some require a brief explanation.

* Sample - sample is a minimal atomic piece of data you can transmit or receive. Most of the library's internal mechanisms operate on samples rather than bytes or bits. Well, every sample consists of bits, it's true, but the sample is a base definition here. Physical sample size depends on RX/TX data format.
* Data format (``-F`` option) - directly or indirectly designates the data, encapsulated in one sample. Basically it can be specified as ``external_format[@internal(wire)_format]``, where external format is the one you deal with in send/receive library calls, and internal (wire) format is used in the data exchange bus between your sdr device and your computer. The most common data formats for ``usdr_dm_create`` utility are:

  * ``ci16`` - complex pair of 16-bit integers (I-Q data), sample size = 32 bits = 4 bytes;
  * ``cf32`` - complex pair of 32-bit floats (I-Q data), sample size = 64 bits = 8 bytes.

  You can try using more complicated formats like ``cf32@ci12`` (receive only) or even ``cfftlpwri16`` to get the RX data as hardware processed FFT frames in 16-bit integers (recieve only, if your sdr hardware and firmware support this).
* Sample rate (``-r`` option) - measured in samples/sec or Hz, and determines the average number of a waveform samples transmitted per 1 second to/from usdr device via data exchange bus (USB or PCIE). The minimal sample rate it 1MHz, the maximal value depends on your bus - you should not expect >30MHz using USB, but PCIE can handle up to 65-70MHz.
* Data block - a maximal piece of data, measured in samples, processed by one send/recv library call within one processing iteration. RX and TX data block sizes can be set by -S and -O options resp.
* Data blocks count (``-c`` option) - the number of RX/TX iterations usdr_dm_create utility runs before normal exit. You can specify -1 for almoust 'infinite' data processing (can be interrupted by pressing CTRL-C anyway). However, if you 'replay' TX data from file (``-I`` option, see below), the iterations count depends on your file size - the inner loop will be interrupted by EOF. The utility will always play all the file data, even if it's size is less than/not multiple to one data block size - except you use ``-c`` option explicitly and specify the number of blocks smaller than your file contains (this is a way to partially transfer data from a file). You can not play a file that contains less than one data sample.
* Input file for TX stream (option ``-I``) - if this option is specified and the name/path is correct, the utility opens the file and 'replays' it's content in TX RF stream. Data blocks are read in series according to the data format and data block size, specified by ``-F`` and ``-O`` options. It's not a problem if the last portion of the file data has it's size less than the TX data block size - the file will always be processed completely (within a sample size).


  For example, you have ``ci16`` format and the data block size is 4096 samples. The physical block size (in bytes) will be = 2*2*4096 = 16384 bytes. If your file size is 100 000 bytes, the utility will transmit 4 blocks of 16384 bytes (4096 samples each) and 1 reduced block of 1696 bytes (424 samples).

  Now imagine that your file size is 99 999 bytes, so the last chunk of data is 1695 bytes. One sample is ci16, that means it's physical size is 2*2 = 4 bytes. So the last block would contain 423 samples = 1692 bytes, and the last 3 bytes will be ignored. To avoid such situations, it is best to match the data size to the physical size of a single sample.

  If the ``-I`` option is omitted and you specify ``-t`` or ``-T`` (TX or TX+RX), the TX data will be generated as a simple sine wave. The sine wave generator only supports ci16 and cf32 formats.
* TX from file in a cycle (``-o`` option) - that's a way to 'infinitely' loop you file transmission (CTRL-C always works). It other words, your file is played up to EOF and then rewinded to the beginning, and so on. All the considerations given in paragraph above (option ``-I``) apply here too. This option has no effect if ``-I`` is omitted (the sine generator is always looped) or you are using the RX-only mode (no ``-t``/``-T`` option).
* Channels mask (option ``-C``) - is useful if you sdr device has more than one RF channel. This option allows you to turn some channels on or off as you wish according to the bit mask you specify.

  For example, you have an xSDR device with 3 channels on board. You can specify ``0b01(1)`` mask to enable ``channel#0`` and disable ``channel#1``, ``0b10(2)`` to enable ``channel#1`` and disable ``channel#0``, or ``0b11(3)`` to enable both. The ``-C`` option affects both TX and RX.
* External Reference Clock:

  * Reference Clock Path (option -a) - allows you to use a reference signal from external source for clocking you device. You can specify "external" for external clock use, or "internal" (by default) for device self-clocking. All the other values are invalid. Of course you should physically wire your sdr device to the clock source to use the "external" option.
  * Reference clock frequency (-x option) - specifies the external clock signal frequency (in Hz).

Available options
-----------------

* ``[-D device]`` - Path to the device
* ``[-f RX_filename [./out.data]]`` - Output file for RX data recording
* ``[-I TX_filename ]`` - Input file for TX stream
* ``[-o <flag: cycle TX from file>]`` - Transmit from file in a loop
* ``[-c count [128]]`` - Number of data blocks to transmit/receive.
* ``[-r samplerate [50e6]]`` - Sample rate in Hz, for both TX and RX
* ``[-F format [ci16] | cf32]`` - Data format, both TX and RX
* ``[-C chmsk [0x1]]``
* ``[-S TX samples_per_blk [4096]]`` - Number of samples per one data block for TX
* ``[-O RX samples_per_blk [4096]]`` - Number of samples per one data block for RX
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
* ``[-a Reference clock path []]``
* ``[-x Reference clock frequency [0(not set)]]``
* ``[-B Calibration freq [0]]``
* ``[-s Sync type [all]]``
* ``[-Q <flag: Discover and exit>]`` - Discover devices and exit
* ``[-R RX_LML_MODE [0]]``
* ``[-A Antenna configuration [0]]``
* ``[-X <flag: Skip initialization>]``
* ``[-z <flag: Continue on error>]``
* ``[-l loglevel [3(INFO)]]`` - Set log level
* ``[-h <flag: This help>]`` - Print help


Examples
--------

Receiving RF (signal recording)
-------------------------------

The following command will record 100000 blocks of 4096 samples each of a RF signal into
a raw file with center frequency of 1200Mhz a sample rate of 4MHz:

.. code-block:: bash

   usdr_dm_create -r4e6 -c100000 -l3 -e1200e6 -f output.raw

The output file will have ``int16`` I-Q complex pairs and can be visualized using ``nympy`` and ``matplotlib``.

Estimated file size is 100000 * 4096 * 2 * 2 = 1 600 000 Kb (be careful, otherwise your HDD may get clogged up!:)

Transmission RF (from a recorded file)
--------------------------------------

The following command will transmit a signal from a raw file with a sample rate of 1MHz and a center frequency of 1700MHz, using sample rate = 1M and TX packet size = 16 Ksamples:

.. code-block:: bash

   usdr_dm_create -t -r1e6 -e1701e6 -E1700e6 -I ~/signal.ci16 -O 16384

Suggesting signal.ci16 size = 20M (for example):

* The file will be transferred completely and the utility should exit when the file is read to EOF
* Sample size (ci16) = 4 bytes, the whole file contains 5 Msamples
* Estimated TX send iteration count = 5 * 1024 / 16 = 320 sends
* Estimated TX time = 5 / 1 = 5s

Transmission RF (just a part of a recorded file)
------------------------------------------------

Same as above, but we explicitly limit the number of TX data packets to 100 (option -c):

.. code-block:: bash

   usdr_dm_create -t -r1e6 -e1701e6 -E1700e6 -I ~/signal.ci16 -O 16384 -c100

In this case:

* Only 1638400 of 5Msamples will be transmitted
* Estimated TX time = 1638400 / 1M = 1.64s
* The utility should exit when 100 data packets are read and transmitted

Transmission RF (from a recorded file in a loop)
------------------------------------------------

The following command works the same as above, but rewinds to the beginning of the file after EOF (option -o does the job):

.. code-block:: bash

   usdr_dm_create -t -r1e6 -e1701e6 -E1700e6 -I ~/signal.ci16 -O 16384 -o

In this case the transmission will last for a long time (say 'infinitely'), until it's interrupted by CTRL-C hit.

Transmission RF (signal generation)
-----------------------------------

The following commands will generate a simple sinus waveform with a given frequency.

* Limited by 10000 blocks of 4096 samples each of 800MHz and sample rate of 7MHz:

.. code-block:: bash

   usdr_dm_create -t -r7e6 -c10000 -l3 -E800e6

* Unlimited transmission(hit Ctrl+C to stop) on 900MHz and sample rate of 3MHz:

.. code-block:: bash

   usdr_dm_create -t -r3e6 -c-1 -l3 -E900e6

List of available devices
-------------------------

.. code-block:: bash

   usdr_dm_create -Q

API to enable the external clocking
-----------------------------------

.. code-block:: bash

   res = usdr_dme_set_string(dev, "/dm/sdr/refclk/path", refclkpath);

* pdm_dev_t dev is your SDR connection handle, obtained previously by usdr_dmd_create_string() call;
* const char* refclkpath: "external" or "internal" to enable/disable the external clocking resp.
* int res == 0 on success, or errno on error.

Set the external clock frequency:

.. code-block:: bash

   res = usdr_dme_set_uint(dev, "/dm/sdr/refclk/frequency", fref);

* pdm_dev_t dev is your SDR connection handle, obtained previously by usdr_dmd_create_string() call;
* uint64_t fref - your external clock frequency value, in Hz;
* int res == 0 on success, or errno on error.

Also, you can get the actual extclock value (in Hz):

.. code-block:: bash

   res = usdr_dme_get_uint(dev, "/dm/sdr/refclk/frequency", pfref);

where ``uint64_t *pfref`` is a pointer to your local var.
