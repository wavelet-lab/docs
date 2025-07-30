=========
srsRAN 4G
=========

.. note::

   This application needs a SoapySDR plugin. Please refer to :doc:`/software/install`.

Overview
--------

**srsRAN_4G** is a popular open-source implementation of the LTE network with both implementations of UE (mobile phone),
and eNB (base station) and EPC (core network). We’ll be focusing on running simple eNB+EPC configuration.

Building
--------

srsRAN provides ready-to-use Ubuntu packages, however, these only work with usrp hardware.
So we’ll need to build from sources.

.. note::

   This will fail on Ubuntu 24.04, so you need to use gcc-11 instead of the default compiler.
   More details are available in `this GitHub issue <https://github.com/srsran/srsRAN_4G/issues/1339>`_.

.. code-block:: bash

   sudo apt-get install build-essential cmake libfftw3-dev libmbedtls-dev libboost-program-options-dev libconfig++-dev libsctp-dev
   # Only for ubuntu 24.04
   sudo apt-get install gcc-11 g++-11

   git clone https://github.com/srsran/srsRAN_4G.git
   git checkout release_22_10

   # Only for ubuntu 24.04
   export CC=$(which gcc-11)
   export CXX=$(which g++-11)

   mkdir build
   cd build
   cmake ..
   make -j$(nproc)
   sudo make install

SIM Cards
---------

To operate even a test network, you need dedicated SIM cards.
The easiest way is to buy preprogrammed SIM cards for test/private networks.

We recommend using `sysmoISIM-S17 <https://shop.sysmocom.de/sysmoISIM-SJA5-S17-SIM-USIM-ISIM-Card-10-pack-with-ADM-keys-S17-chip-for-SUCI-in-USIM/sysmoISIM-SJA5-S17-10p-adm>`_. cards.
You’ll get the secret key via email.

Alternatively, you can use programmable SIM cards and create a profile by yourself.
Here’s are `detailed instructions <https://www.quantulum.co.uk/blog/private-lte-with-limesdr-and-srsran-part-3-sim-cards/>`_.

Both ways work fine, so you can use whichever is more convenient.

Configuring EPC
---------------

We’ll need to configure EPC to run with SIM card network codes. Edit ``epc.conf`` and change mcc and mnc accordingly.
Then, you need to append SIM secrets to ``user_db.csv`` file. E.g., in our case it’s

.. code-block:: text

   ue0,mil,901704356421622,aae018af78cb0fc5276138ef1254d7f0,opc,b0414d943ea6f14889ae04dae16c67e0,8000,00000000239b,7,dynamic

`Detailed instructions <https://docs.srsran.com/projects/4g/en/latest/usermanuals/source/srsenb/source/2_enb_getstarted.html>`_.

Frequency bands
---------------

LTE band is defined by EARFCN code, which is a combination of frequency and bandwidth.
In big cities, it’s hard to find a free band, so, you can use our :doc:`web platform </intro/getting_started>` to observe the spectrum and find a free band.

Better to use bands with both downlink and uplink frequencies are not used by any operator in your area, but you can also try bands with only downlink frequency free.

Please refer to `this table <https://www.sqimway.com/lte_band.php>`_ for the list of EARFCN codes and their corresponding frequencies.

Configuring eNB
---------------

For ``eNB``, besides ``EARFCN``/``MCC``/``MNC`` codes, we also need to specify ``f.device_name`` and ``rf.device_args`` parameters.
The latest depends on actual LTE bandwidth (``n_prb``).
Without this parameter, eNB will work but less efficiently which may lead to more CPU usage and buffer overruns.

Due to limited USB2 bus bandwidth, only 1.4/3 Mhz/5 Mhz options are suitable.
The 5 Mhz band has been supported since version 0.9.8 using 12-bit I/Q format.
To enable it, you need to add ``rx12bit=1`` parameter to ``rf.device_args`` as in example below.
PCIe connectivity works well in any configuration.

.. note::
   1.4/3Mhz may not work with all LTE phones.

1.4 Mhz
'''''''

.. code-block:: bash

   sudo srsenb --rf.device_name soapy --rf.device_args driver=usdr,desired_rx_pkt=1920 --enb.n_prb 6 --enb.mcc 901 --enb.mnc 70 --rf.rx_gain 35 --rf.tx_gain 20

3 Mhz
'''''

.. code-block:: bash

   sudo srsenb --rf.device_name soapy --rf.device_args driver=usdr,desired_rx_pkt=3840 --enb.n_prb 15 --enb.mcc 901 --enb.mnc 70 --rf.rx_gain 35 --rf.tx_gain 20

5 Mhz
'''''

.. code-block:: bash

   sudo srsenb --rf.device_name soapy --rf.device_args driver=usdr,desired_rx_pkt=5760 --enb.n_prb 25 --enb.mcc 901 --enb.mnc 70 --rf.rx_gain 35 --rf.tx_gain 20

5 Mhz (USB2)
''''''''''''

.. code-block:: bash

   sudo srsenb --rf.device_name soapy --rf.device_args driver=usdr,desired_rx_pkt=5760,rx12bit=1 --enb.n_prb 25 --enb.mcc 901 --enb.mnc 70 --rf.rx_gain 35 --rf.tx_gain 20

10 Mhz
''''''

.. code-block:: bash

   sudo srsenb --rf.device_name soapy --rf.device_args driver=usdr,desired_rx_pkt=11520 --enb.n_prb 50 --enb.mcc 901 --enb.mnc 70 --rf.rx_gain 35 --rf.tx_gain 20

20 Mhz
''''''

.. code-block:: bash

   sudo srsenb --rf.device_name soapy --rf.device_args driver=usdr,desired_rx_pkt=23040 --enb.n_prb 100 --enb.mcc 901 --enb.mnc 70 --rf.rx_gain 35 --rf.tx_gain 20

.. note::

   You can add these parameters to ``enb.conf`` and ``rr.conf`` instead.


Running Networks
----------------

Enable NAT
''''''''''

Before running the network, you need to enable NAT for your internet network device.
This can be done by running a simple script:

.. code-block:: bash

   sudo srsepc_if_masq.sh {name_of_your_internet_device}

Run EPC
'''''''

.. code-block:: bash

   sudo srsepc epc.conf

Run eNB
'''''''

``srsenb`` either with config file or all parameters in CLI.

.. code-block:: bash

   sudo srsenb ...


Using the network
-----------------

If the SIM card was set up correctly you’ll see UE Authentication Accepted in EPC log.

.. code-block:: bash

   ID Response -- IMSI: 901704356421622
   Downlink NAS: Sent Authentication Request
   UL NAS: Received Authentication Response
   Authentication Response -- IMSI 901704356421622
   UE Authentication Accepted.

If you have properly configured APN on your mobile, you’ll see an allocation of IP address to your equipment right after authentication.

.. code-block:: bash

   ESM Info: APN srsapn
   Getting subscription information -- QCI 7
   Sending Create Session Request.
   Creating Session Response -- IMSI: 901704356421622
   Creating Session Response -- MME control TEID: 1
   Received GTP-C PDU. Message type: GTPC_MSG_TYPE_CREATE_SESSION_REQUEST
   SPGW: Allocated Ctrl TEID 1
   SPGW: Allocated User TEID 1
   SPGW: Allocate UE IP 172.16.0.2

If you don’t see it, please check the internet APN setting on your phone.

Using Development Board
-----------------------

Running a private LTE network or even a test LTE network is subject to local regulation.
In some counties, it’s not hard to get a low-power license. The other part is RF compliant emissions.

Most inexpensive SDRs don’t have any selectivity filtering or transmission harmonic reduction.
This is crucial to run not just commercial but also test networks.
uSDR is a tiny form factor board and fitting proper filtering is physically impossible.
That’s why we developed the uSDR development board.
It has a power amplifier, low-noise amplifier, a bank of filters, and a bank of LTE duplexers.
LNA and PA increase coverage for uplink and downlink.
Duplexers significantly reduce out of band emissions on the TX path, on the RX path they improve selectivity (any strong signal may saturate receiving path, thus reducing coverage).

We strongly advise using the development board for doing experiments with LTE networks wherever possible.
To use duplexers, you need to connect u.FL cables from uSDR to the development board (``RX->J20``, ``TX->J19``).

.. note::

   :doc:`Additional information about Development Board </hardware/devboard>`.

A single antenna should be connected to ``J17``.

The uSDR dev board has a duplexer bank in bands 2,3,5,7,8.

+------+---------+-------------------+-------------------+-----------------------+
| Band | F (MHz) | Uplink (MHz)      | Downlink (MHz)    | Channels              |
+======+=========+===================+===================+=======================+
| 2    | 1900    | 1850 - 1910       | 1930 - 1990       | 1.4, 3, 5, 10, 15, 20 |
+------+---------+-------------------+-------------------+-----------------------+
| 3    | 1800    | 1710 - 1785       | 1805 - 1880       | 1.4, 3, 5, 10, 15, 20 |
+------+---------+-------------------+-------------------+-----------------------+
| 5    | 850     | 824 - 849         | 869 - 894         | 1.4, 3, 5, 10         |
+------+---------+-------------------+-------------------+-----------------------+
| 7    | 2600    | 2500 - 2570       | 2620 - 2690       | 5, 10, 15, 20         |
+------+---------+-------------------+-------------------+-----------------------+
| 8    | 900     | 880 - 915         | 869 - 894         | 1.4, 3, 5, 10         |
+------+---------+-------------------+-------------------+-----------------------+

To enable using the duplexer path, you’ll need to add ``fe=pciefev1:path_band7:pa_on:lna_on`` to the ``--rf.device_args`` parameter using a comma,
and where ``path_band7`` reflects using the duplexer for Band Seven. E.g., here’s the full configuration string for 20 MHz bandwidth:

.. code-block:: bash

   sudo srsenb --rf.device_name soapy --rf.device_args driver=usdr,desired_rx_pkt=23040,fe=pciefev1:path_band7:pa_on:lna_on --rf.rx_gain 35 --rf.tx_gain 20  --enb.mcc 901 --enb.mnc 70  --enb.n_prb 100

References
----------

* `srsRAN Project <https://www.srsran.com>`_
* `srsRAN 4G Repository <https://github.com/srsran/srsRAN_4G>`_
* `srsRAN 4G Documentation <https://docs.srsran.com/projects/4g/en/latest/>`_
