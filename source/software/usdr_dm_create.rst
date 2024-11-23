usdr_dm_create tool
===================

.. note::
   | You have to install ``usdr-tools`` package first.
   | Please refer to the :doc:`/software/install`.

This tool allows you to:

* Transmit a simple sinusoidal waveform with a specified frequency and power.
* Receive and record a signal into a raw file.
* Perform other testing and debugging tasks.

Newbie glossary
---------------

Below are key concepts and terms to help you understand the options provided. Most options have reasonable default values, but some require a brief explanation.


**Sample**
    A sample is the smallest unit of data you can transmit or receive. The library operates on samples rather than bytes or bits. While each sample consists of bits, the concept of a sample is fundamental here. The physical size of a sample depends on the RX/TX data format.

**Data Format (-F option)**
    This determines the data encapsulated in one sample. It can be specified as:

    - `external_format[@internal(wire)_format]`

    where:
    - **External format**: The format used in send/receive API calls.
    - **Internal (wire) format**: The format used for data exchange between the SDR device and the computer.

    Common data formats for the ``usdr_dm_create`` utility include:

    - **ci16**: A complex pair of 16-bit integers (I-Q data). Sample size = 32 bits (4 bytes).
    - **cf32**: A complex pair of 32-bit floats (I-Q data). Sample size = 64 bits (8 bytes).

    Advanced formats (if supported by your hardware):
    - **cf32@ci12**: Receive-only.
    - **cfftlpwri16**: Hardware-processed FFT frames in 16-bit integers (receive-only).

**Sample Rate (-r option)**
    The sample rate is measured in samples/sec (Hz) and determines the average number of waveform samples transmitted per second to/from the SDR device.

    - **Minimum**: 1 MHz.
    - **Maximum**: USB supports up to ~30 MHz; PCIe can handle up to 65–70 MHz.

**Data Block**
    The largest unit of data, measured in samples, processed in a single send/receive API call.

    - **RX Block Size (-S option)**
    - **TX Block Size (-O option)**

**Data Block Count (-c option)**
    The number of RX/TX iterations the ``usdr_dm_create`` utility runs before exiting:

    - Use ``-1`` for near-infinite data processing (can be interrupted with CTRL-C).
    - For TX from a file (``-I`` option), iterations are limited by file size or explicitly set with ``-c``. 

The utility will always process all the data in the file, even if the file size is smaller than or not a multiple of the specified data block size. However, if you explicitly use the -c option to limit the number of blocks, only the specified portion of the file will be transferred (allowing partial data transfer). Files smaller than one complete data sample cannot be processed.

**Output File for RX Streams (-f option)**
    Specifies the file path to save received I-Q data in the defined format. For devices with multiple RX channels, a numerical suffix is added to the filename.

**Input File for TX Streams (-I option)**
      Specifies the file path to use for transmitting data. For devices with multiple TX channels:

    - Provide multiple files separated by colons ``:``.
    - If fewer files are provided than channels, a round-robin rotation is applied.

    For example, if you have an xSDR device with two TX channels and set the channel mask to ``3`` (``0b11``) to enable both channels, you can use the ``-I`` option to specify input files:

- If you provide ``file1.dat:file2.dat``, channel 0 will transmit IQ data from ``file1.dat``, and channel 1 will transmit IQ data from ``file2.dat``.
- If you specify only one file (e.g., ``-I file.dat``), the same file will be used for both channel 0 and channel 1.

Data blocks are processed sequentially based on the data format and block size specified by the ``-F`` and ``-O`` options. If the last portion of the file data is smaller than the TX data block size, the utility will process the file completely, up to the nearest sample boundary.

For example:
- Suppose you are using the ``ci16`` format, with a data block size of 4096 samples. The physical size of a block is calculated as ``2 * 2 * 4096 = 16384`` bytes. 
- If your file size is 100,000 bytes, the utility will transmit:
  - Four full blocks of 16,384 bytes each (4096 samples per block).
  - One partial block of 1696 bytes (424 samples).
  
Now consider a file size of 99,999 bytes:
- The last chunk of data would be 1695 bytes. Since a single sample in ``ci16`` format requires 4 bytes (``2 * 2``), the last block will contain 423 samples (1692 bytes), with the remaining 3 bytes ignored.
- To avoid data loss, ensure your file size is a multiple of the sample size.

If the ``-I`` option is not used and you specify ``-t`` or ``-T`` (TX or TX+RX modes), the utility will generate a simple sine wave for TX data. The sine wave generator supports only the ``ci16`` and ``cf32`` formats.

**TX from File in a Cycle (-o option)**
      This option allows you to continuously loop the transmission of a file. When enabled, the file is played to the end (EOF) and then rewound to the beginning, repeating indefinitely. You can interrupt the transmission at any time by pressing ``CTRL-C``.

All considerations mentioned for the ``-I`` option apply here as well. For example:
- If the file size is not a multiple of the sample size, the utility will still process the file completely.
- The looped file is transmitted block by block according to the specified data format and block size.

**Note:**  
- The ``-o`` option has no effect if the ``-I`` option (input file for TX) is omitted.  
- In this case, the sine wave generator is used for TX and loops automatically.  
- This option is also irrelevant in RX-only mode (when ``-t`` or ``-T`` is not specified).

**Channel Mask (-C option)**
      The channel mask is used to control which RF channels of your SDR device are active. This is particularly useful for devices with multiple RF channels, enabling you to turn specific channels on or off as needed.

The mask is specified as a bitmask where each bit corresponds to a channel:
- ``0`` disables the channel.
- ``1`` enables the channel.

**Example:**  
For an xSDR device with three RF channels:
- ``0b01`` (1): Enables channel 0, disables channel 1.
- ``0b10`` (2): Enables channel 1, disables channel 0.
- ``0b11`` (3): Enables both channels 0 and 1.

The ``-C`` option affects both TX and RX operations.


**External Reference Clock**
    - **Reference Clock Path (-a option)**: Specifies the clocking source for the SDR device:
        - ``internal``: Default device clocking.
        - ``external``: Use an external reference clock (requires physical wiring).

    - **Reference Clock Frequency (-x option)**: Defines the external clock frequency in Hz.


See below is an example of configuring the Development Board to provide an external clock source


Available options
-----------------

* ``[-D device_parameters]`` - Device additional options & parameters, comma-separated
* ``[-f RX_filename [./out.data]]`` - Output file for RX data recording
* ``[-I TX_filename(s) (optionally colon-separated list)]`` - Input file(s) for TX stream(s)
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

The following command will record 100000 blocks of 4096 samples each of an RF signal into
a raw file with a center frequency of 1200Mhz and a sample rate of 4MHz:

.. code-block:: bash

   usdr_dm_create -r4e6 -c100000 -l3 -e1200e6 -f output.raw

The output file will have ``int16`` I-Q complex pairs and can be visualized using ``nympy`` and ``matplotlib``.

The estimated file size is 100000 * 4096 * 2 * 2 = 1 600 000 Kb (be careful, otherwise your HDD may get clogged up!:)

Transmission RF (from a recorded file)
--------------------------------------

The following command will transmit a signal from a raw file with a sample rate of 1MHz and a center frequency of 1700MHz, using sample rate = 1M and TX packet size = 16 K samples:

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

In this case, the transmission will last for a long time (say 'infinitely') until it's interrupted by a CTRL-C hit.

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
* const char* refclkpath: "external" or "internal" to enable/disable the external clocking.
* int res == 0 on success, or errno on error.

Set the external clock frequency:

.. code-block:: bash

   res = usdr_dme_set_uint(dev, "/dm/sdr/refclk/frequency", fref);

* pdm_dev_t dev is your SDR connection handle, obtained previously by usdr_dmd_create_string() call;
* uint64_t fref - The external clock frequency, specified in Hz;
* int res == 0 on success, or errno on error.

Also, you can get the actual extclock value (in Hz):

.. code-block:: bash

   res = usdr_dme_get_uint(dev, "/dm/sdr/refclk/frequency", pfref);

where ``uint64_t *pfref`` is a pointer to your local var.

Configuring the utility to obtain an external reference clock from the Development Board
--------------------------------------------------------------------------------------

.. code-block:: bash

   usdr_dm_create -t -r1e6 -c-1 -Y4 -E390e6 -e390e6 -I ./signal_1khz.ci16 -C1 -o -aexternal -Dfe=pciefev1:osc_on -x26e6

Except for the `-a` and `-x` options, you must enable the Development Board’s reference clock generator. This can be done using the `-D` option, with the appropriate value for the `fe` (front-end) parameter.

The `fe` parameter has the following meaning:

* dev board name - ``pciefe`` in this case;
* dev board revision - specify this without any separator, e.g., `v1`;
* parameters separator - use a colon (`:`) to separate parameters;
* colon-delimited list of parameters, where we need only one parameter to control the oscillator. This parameter can vary:


  * ``osc_on`` (or ``osc_en``) - enable oscillator
  * ``osc_off`` - disable oscillator

**Note:** To ensure proper functioning of your SDR device, you must know the exact reference clock frequency, which you specify using the `-x` option.

For more detailed information about the Development Board, refer to :doc:`/hardware/devboard`



Device parameters (option -D)
-----------------------------

As mentioned earlier, the device parameters string is a comma-separated list of `name=value` pairs. Each value (`val`) may contain a sublist of parameters, which are typically separated by a colon ``:``. Therefore, the most general format is:


.. code-block:: bash

   usdr_dm_create -D<name1>=<val1[:subname1[=subval1]:..:subvalN[=subvalN]]>..<nameM>=<valM>

Available device parameters:

* ``bus`` - specifies the device connection bus(es) name(s) and the filtering parameters, maybe a colon-separated list

  * ``bus=usb[@filter]``, where filter is ``<usb_addr>/<usb_port>/<usb_addr>`` (for instance - ``usb@3/1/31``)
  * ``bus=pci[/filter]``
  * ``bus=/dev/[filter]``
* ``fe`` - front-end settings, see :doc:`/hardware/devboard`
* ``cpulimit`` = max CPUs count, the usdr library can use;
* ``loglevel`` = 0(errors only) .. 6+(everything), specifies the verbosity level  of the uSDR library logging;
* xSDR + USB only options:

  * ``bifurcation`` = 1|0, enable/disable channel bifurcation;
  * ``nodec`` (no value) - disable decimation;
* uSDR + USB only options:

  * ``extclk`` = (1 or 'o') : enable external reference clock selector, otherwise - disable. This option has just the same effect as ``-a external``;
  * ``extref`` = external clock frequency, in Hz. This option has just the same effect as ``-x <fref>``;
* PCIE only options:
  
  * ``mmapio`` = (1 or 'o') : enable, otherwise - disable, use mmap() instead of ioctl()

