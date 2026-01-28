=================================
Front End (FE) and Breakout Board
=================================

A modular adapter board for sSDR and dSDR modules with an integrated high-performance RF front-end.

Overview
========

.. image:: ../_static/fe/fe_front.png
   :alt: fe sdr


.. image:: ../_static/fe/fe_back.png
   :alt: fe sdr

The Front End (FE) is a modular, high-performance adapter board featuring **4 RX and 4 TX channels** which can be synchronized.
In addition, the board includes fast TX/RX switches for each channel, making it usable for **TDD** applications.

The board can be used with our **dSDR** or **sSDR** transceiver modules.

Breakout board
--------------

The **Breakout board** is the light version of the FE board without the RF front-end components.
It is intended for users who want to design their own RF front-end or use the board in a lab environment.

.. image:: ../_static/fe/fe_breakout_front.png
   :alt: fe breakout sdr

General Specifications
----------------------

**Clock Synchronization**
  - LMK1C1104

**Module slot**
  - M.2 Key M socket for sSDR or dSDR module

**Form Factor**
  - PCIe x4

RF Specifications
-----------------

.. note::
   | The full specification of sSDR module :doc:`/hardware/ssdr`.

.. note::
   | The full specification of dSDR module :doc:`/hardware/dsdr`.

Integrated high-performance RF front-end with low-noise amplifiers, power amplifiers, filters, and switches.

**RF frontend frequency range**
  - 400 MHz to 12 GHz

**RFIC**
  - with sSDR module:
     - LMS7002M + LMS8001
     - 2 RX / 2 TX channels
  - with dSDR module:
     - AFE7900/AFE7901/AFE7950
     - 6 RX / 4 TX channels

**Frequency Range**
  - with sSDR module:
     - 30 MHz to 11 GHz
  - with dSDR module:
     - Model XXXX: 10 MHz to 12 GHz (See the dSDR module page for reference)

**Sample Rate**
  - with sSDR module:
     - 4 MSps - 100 MSps
  - with dSDR module
     - 0.1 MSps - 500 MSps

**Channel Bandwidth**
  - with sSDR module:
     - 0.5 MHz - 90 MHz
  - with dSDR module:
     - 0.5 MHz - 500 MHz

Bifurcation Modes
-----------------

- **4×4 MIMO systems**
- **2 independent 2×2 MIMO systems**

Target Applications
-------------------

**Cellular Communication**
  - Enables next-generation **4G/5G wireless networks** with high-order **massive MIMO** and **TDD**
  - Fully compatible with **Amarisoft** and **srsRAN**

**Directional Finding**
  - Determines the **direction of arrival (DoA)** of incoming radio signals, enabling **precise localization** of transmitters

**Beamforming**
  - Focuses on signal transmission and reception in specific directions
  - Enhances range, improves signal quality, and reduces interference in multi-user environments

Connections
===========

.. note::
   | USB-C is intended solely for use in manufacturing test facilities.
   | It is not used during normal operation.

Front side
----------

The front side of the board contains the M.2 socket for the sSDR or sSDR module and 4 MHF7 connectors for RX signals.

Back side
---------

The front side of the board contains 4 MHF7 connectors for TX signals.


PCI bracket panel
-----------------

The bracket panel of the FE has 8 external SMA connectors for TX/RX/TRX signals.


Clocks and synchronization
==========================

There are two clock domains on the FE board:

* **REFCLK**: Reference clock used for phase synchronization and RF frequency calibration.
* **SYSREF**: Event synchronization: start, stop, and other control signals.

The FE board can use different clock sources:

* On-board crystal oscillator.
* GPS synchronization using the on-board GPS module.


sSDR wiring
-----------

* ``REF+`` to ``SYSREF+``.
* ``REF-`` to ``SYSREF-``.
* ``1PPS_OUT`` to ``1PPS_SYN``.

The following diagram shows the clock and synchronization wiring when using the sSDR module.

.. image:: ../_static/fe/fe_sync_ssdr.png
   :alt: fe ssdr clocks and synchronization block diagram



dSDR wiring
-----------

* ``REF+`` to ``REFCLK_SE``.
* ``1PPS_OUT`` to ``1PPS_SYN``.

The following diagram shows the clock and synchronization wiring when using the dSDR module.

.. image:: ../_static/fe/fe_sync_dsdr.png
   :alt: fe dsdr clocks and synchronization block diagram


RF distribution
===============

.. image:: ../_static/fe/fe_rf.png
   :alt: fe sdr rf distribution block diagram

.. note::
   | The diagram above shows the RF distribution for one pair of RX/TX channels.
   | The rest of the channels are connected in the same way.


sSDR module
-----------


.. image:: ../_static/fe/ssdr_fe_wiring.png
   :alt: fe ssdr rf connection diagram


For sSDR, the RF distribution should be connected as follows:

* ``RXA`` to ``sSDR RX A``.
* ``RXB`` to ``sSDR RX B``.
* ``TXA`` to ``sSDR TX A``.
* ``TXB`` to ``sSDR TX B``.


.. note::
   | sSDR only has 2 RX and 2 TX channels, so only the first two pairs are used.


dSDR module
-----------


.. image:: ../_static/fe/dsdr_fe_wiring.png
   :alt: fe dsdr rf connection diagram


For dSDR, the RF distribution should be connected as follows:

* ``RXA`` to ``dSDR RX A``.
* ``RXB`` to ``dSDR RX B``.
* ``RXC`` to ``dSDR RX C``.
* ``RXD`` to ``dSDR RX D``.
* ``TXA`` to ``dSDR TX A``.
* ``TXB`` to ``dSDR TX B``.
* ``TXC`` to ``dSDR TX C``.
* ``TXD`` to ``dSDR TX D``.


Calibration
-----------

The loopback mode is possible for each TX/RX pair for calibration purposes.


RF frontend control
===================


.. note::
   | In order to control the frontend from software, you need to use the ``usdr_registers`` tool.
   | Please refer to the :doc:`/software/usdr_registers`.


exfe10_4ch_usr
--------------

This section describes the main register map for controlling the FE front-end.
Using controls on this page, you can switch filters, set attenuators, select antenna paths, and enable/disable channels.


.. image:: ../_static/fe/fe_control_usr.png
   :alt: fe control registers


* - ``RX_FILTER_BANK``/``A`` - RX filter bank selector for channel A
  - ``/debug/hw/exfe10_4ch_usr/0/reg/0x50/A``
  - Options:

        - FILT_400_1000M - RX filter 400-1000 MHz
        - FILT_1000_2000M - RX filter 1000-2000 MHz
        - FILT_2000_3500M - RX filter 2000-3500 MHz
        - FILT_2500_5000M - RX filter 2500-5000 MHz
        - FILT_3500_7100M - RX filter 3500-7100 MHz
        - AUTO_400_1000M - **======================TODO**
        - AUTO_1000_2000M - **======================TODO**
        - AUTO_2000_3500M - **======================TODO**
        - AUTO_2500_5000M - **======================TODO**
        - AUTO_3500_7100M - **======================TODO**

* - ``RX_FILTER_BANK``/``B`` - RX filter bank selector for channel B
  - ``/debug/hw/exfe10_4ch_usr/0/reg/0x50/B``
  - Options: same as channel A

* - ``RX_FILTER_BANK``/``C`` - RX filter bank selector for channel C
  - ``/debug/hw/exfe10_4ch_usr/0/reg/0x50/C``
  - Options: same as channel A

* - ``RX_FILTER_BANK``/``D`` - RX filter bank selector for channel D
  - ``/debug/hw/exfe10_4ch_usr/0/reg/0x50/D``
  - Options: same as channel A

* - ``RX_ATTN``/``A`` - RX attenuator setting (dB) for channel A
  - ``/debug/hw/exfe10_4ch_usr/0/reg/0x51/A``

* - ``RX_ATTN``/``B`` - RX attenuator setting (dB) for channel B
  - ``/debug/hw/exfe10_4ch_usr/0/reg/0x51/B``

* - ``RX_ATTN``/``C`` - RX attenuator setting (dB) for channel C
  - ``/debug/hw/exfe10_4ch_usr/0/reg/0x51/C``

* - ``RX_ATTN``/``D`` - RX attenuator setting (dB) for channel D
  - ``/debug/hw/exfe10_4ch_usr/0/reg/0x51/D``

* - ``ANT_SEL``/``A`` - Antenna path selector for channel A
  - ``/debug/hw/exfe10_4ch_usr/0/reg/0x52/A``
  - Options:

        - RX_TO_RX_AND_TX_TO_TRX - RX to RX path and TX to TRX path
        - RX_TO_TRX_AND_TX_TERM - RX to TRX path and TX terminated
        - RX_TO_RX_AND_TX_TERM - RX to RX path and TX terminated
        - RX_TX_LOOPBACK - RX to TX loopback
        - TDD_DRIVEN_AUTO - **======================TODO**

* - ``ANT_SEL``/``B`` - Antenna path selector for channel B
  - ``/debug/hw/exfe10_4ch_usr/0/reg/0x52/B``
  - Options: same as channel A

* - ``ANT_SEL``/``C`` - Antenna path selector for channel C
  - ``/debug/hw/exfe10_4ch_usr/0/reg/0x52/C``
  - Options: same as channel A

* - ``ANT_SEL``/``D`` - Antenna path selector for channel D
  - ``/debug/hw/exfe10_4ch_usr/0/reg/0x52/D``
  - Options: same as channel A

* - ``RX_CHEN``/``A`` - Enable RX channel A
  - ``/debug/hw/exfe10_4ch_usr/0/reg/0x53/A``

* - ``RX_CHEN``/``B`` - Enable RX channel B
  - ``/debug/hw/exfe10_4ch_usr/0/reg/0x53/B``

* - ``RX_CHEN``/``C`` - Enable RX channel C
  - ``/debug/hw/exfe10_4ch_usr/0/reg/0x53/C``

* - ``RX_CHEN``/``D`` - Enable RX channel D
  - ``/debug/hw/exfe10_4ch_usr/0/reg/0x53/D``

* - ``TX_CHEN``/``A`` - Enable TX channel A
  - ``/debug/hw/exfe10_4ch_usr/0/reg/0x54/A``

* - ``TX_CHEN``/``B`` - Enable TX channel B
  - ``/debug/hw/exfe10_4ch_usr/0/reg/0x54/B``

* - ``TX_CHEN``/``C`` - Enable TX channel C
  - ``/debug/hw/exfe10_4ch_usr/0/reg/0x54/C``

* - ``TX_CHEN``/``D`` - Enable TX channel D
  - ``/debug/hw/exfe10_4ch_usr/0/reg/0x54/D``

* - ``TX_2STAGE``/``A`` - Enable TX 2nd stage for channel A
  - ``/debug/hw/exfe10_4ch_usr/0/reg/0x55/A``

* - ``TX_2STAGE``/``B`` - Enable TX 2nd stage for channel B
  - ``/debug/hw/exfe10_4ch_usr/0/reg/0x55/B``

* - ``TX_2STAGE``/``C`` - Enable TX 2nd stage for channel C
  - ``/debug/hw/exfe10_4ch_usr/0/reg/0x55/C``

* - ``TX_2STAGE``/``D`` - Enable TX 2nd stage for channel D
  - ``/debug/hw/exfe10_4ch_usr/0/reg/0x55/D``



exfe10_4ch_exp
--------------

This section describes the low level control register map for the FE front-end.
Using this page, you can control each hardware component directly.

.. warning::
   | The page exposes the low-level hardware controls.
   | Improper use may lead to unexpected behavior or damage to your hardware.

.. image:: ../_static/fe/fe_control_exp.png
   :alt: fe control lowlevel registers


* - ``SW_RX_FILTER``/``IN_CHA`` - RX IN filters switch for Channel A
  - ``/debug/hw/exfe10_4ch_exp/0/reg/0x30/IN_CHA``
  - Options:

        - MUTE0 - **======================TODO**
        - 400_1000M - Input filter bank switch to filter 400-1000 MHz
        - 1000_2000M - Input filter bank switch to filter 1000-2000 MHz
        - 2000_3500M - Input filter bank switch to filter 2000-3500 MHz
        - 2500_5000M - Input filter bank switch to filter 2500-5000 MHz
        - 3500_7100M - Input filter bank switch to filter 3500-7100 MHz
        - MUTE1 - **======================TODO**
        - MUTE2 - **======================TODO**

* - ``SW_RX_FILTER``/``OUT_CHA`` - RX OUT filters switch for Channel A
  - ``/debug/hw/exfe10_4ch_exp/0/reg/0x30/OUT_CHA``
  - Options:

        - MUTE0 - **======================TODO**
        - 400_1000M - Output filter bank switch to filter 400-1000 MHz
        - 1000_2000M - Output filter bank switch to filter 1000-2000 MHz
        - 2000_3500M - Output filter bank switch to filter 2000-3500 MHz
        - 2500_5000M - Output filter bank switch to filter 2500-5000 MHz
        - 3500_7100M - Output filter bank switch to filter 3500-7100 MHz
        - MUTE1 - **======================TODO**
        - MUTE2 - **======================TODO**

* - ``SW_RX_FILTER``/``IN_CHB`` - RX IN filters switch for Channel B
  - ``/debug/hw/exfe10_4ch_exp/0/reg/0x30/IN_CHB``
  - Options: same as Channel A

* - ``SW_RX_FILTER``/``OUT_CHB`` - RX OUT filters switch for Channel B
  - ``/debug/hw/exfe10_4ch_exp/0/reg/0x30/OUT_CHB``
  - Options: same as Channel A

* - ``SW_RX_FILTER``/``IN_CHC`` - RX IN filters switch for Channel C
  - ``/debug/hw/exfe10_4ch_exp/0/reg/0x30/IN_CHC``
  - Options: same as Channel A

* - ``SW_RX_FILTER``/``OUT_CHC`` - RX OUT filters switch for Channel C
  - ``/debug/hw/exfe10_4ch_exp/0/reg/0x30/OUT_CHC``
  - Options: same as Channel A

* - ``SW_RX_FILTER``/``IN_CHD`` - RX IN filters switch for Channel D
  - ``/debug/hw/exfe10_4ch_exp/0/reg/0x30/IN_CHD``
  - Options: same as Channel A

* - ``SW_RX_FILTER``/``OUT_CHD`` - RX OUT filters switch for Channel D
  - ``/debug/hw/exfe10_4ch_exp/0/reg/0x30/OUT_CHD``
  - Options: same as Channel A

* - ``ENABLE``/``IF_VBYP`` - IF bypass control
  - ``/debug/hw/exfe10_4ch_exp/0/reg/0x31/IF_VBYP``

* - ``ENABLE``/``REF_GPS`` - Enable GPS module
  - ``/debug/hw/exfe10_4ch_exp/0/reg/0x31/REF_GPS``

* - ``ENABLE``/``P8V_TX`` - Enable +8V power supply for TX amps
  - ``/debug/hw/exfe10_4ch_exp/0/reg/0x31/P8V_TX``

* - ``ENABLE``/``P6V_RX`` - Enable +6V power supply for RX amps
  - ``/debug/hw/exfe10_4ch_exp/0/reg/0x31/P6V_RX``

* - ``ENABLE``/``PA_BYPASS_CHD`` - Stage-2 PA bypass, channel D
  - ``/debug/hw/exfe10_4ch_exp/0/reg/0x31/PA_BYPASS_CHD``

* - ``ENABLE``/``PA_BYPASS_CHC`` - Stage-2 PA bypass, channel C
  - ``/debug/hw/exfe10_4ch_exp/0/reg/0x31/PA_BYPASS_CHC``

* - ``ENABLE``/``PA_BYPASS_CHB`` - Stage-2 PA bypass, channel B
  - ``/debug/hw/exfe10_4ch_exp/0/reg/0x31/PA_BYPASS_CHB``

* - ``ENABLE``/``PA_BYPASS_CHA`` - Stage-2 PA bypass, channel A
  - ``/debug/hw/exfe10_4ch_exp/0/reg/0x31/PA_BYPASS_CHA``

* - ``LED_TRX_CTRL``/``LED_CHA`` - LED TX/RX control for Channel A
  - ``/debug/hw/exfe10_4ch_exp/0/reg/0x32/LED_CHA``

* - ``LED_TRX_CTRL``/``LED_CHB`` - LED TX/RX control for Channel B
  - ``/debug/hw/exfe10_4ch_exp/0/reg/0x32/LED_CHB``

* - ``LED_TRX_CTRL``/``LED_CHC`` - LED TX/RX control for Channel C
  - ``/debug/hw/exfe10_4ch_exp/0/reg/0x32/LED_CHC``

* - ``LED_TRX_CTRL``/``LED_CHD`` - LED TX/RX control for Channel D
  - ``/debug/hw/exfe10_4ch_exp/0/reg/0x32/LED_CHD``

* - ``LEDRX_CH_CTRL``/``EN_CHA`` - Enable LED CHA
  - ``/debug/hw/exfe10_4ch_exp/0/reg/0x33/EN_CHA``

* - ``LEDRX_CH_CTRL``/``EN_CHB`` - Enable LED CHB
  - ``/debug/hw/exfe10_4ch_exp/0/reg/0x33/EN_CHB``

* - ``LEDRX_CH_CTRL``/``EN_CHC`` - Enable LED CHC
  - ``/debug/hw/exfe10_4ch_exp/0/reg/0x33/EN_CHC``

* - ``LEDRX_CH_CTRL``/``EN_CHD`` - Enable LED CHD
  - ``/debug/hw/exfe10_4ch_exp/0/reg/0x33/EN_CHD``

* - ``LEDRX_CH_CTRL``/``LED_CHA`` - LED CHA indicator
  - ``/debug/hw/exfe10_4ch_exp/0/reg/0x33/LED_CHA``

* - ``LEDRX_CH_CTRL``/``LED_CHB`` - LED CHB indicator
  - ``/debug/hw/exfe10_4ch_exp/0/reg/0x33/LED_CHB``

* - ``LEDRX_CH_CTRL``/``LED_CHC`` - LED CHC indicator
  - ``/debug/hw/exfe10_4ch_exp/0/reg/0x33/LED_CHC``

* - ``LEDRX_CH_CTRL``/``LED_CHD`` - LED CHD indicator
  - ``/debug/hw/exfe10_4ch_exp/0/reg/0x33/LED_CHD``

* - ``P_A_EN_AB``/``B`` - Enable CHB (PA enable AB)
  - ``/debug/hw/exfe10_4ch_exp/0/reg/0x34/B``

* - ``P_A_EN_AB``/``A`` - Enable CHA (PA enable AB)
  - ``/debug/hw/exfe10_4ch_exp/0/reg/0x34/A``

* - ``ATTN_RX_CH_AB``/``B`` - Attenuator CHB
  - ``/debug/hw/exfe10_4ch_exp/0/reg/0x35/B``

* - ``ATTN_RX_CH_AB``/``A`` - Attenuator CHA
  - ``/debug/hw/exfe10_4ch_exp/0/reg/0x35/A``

* - ``SW_AB``/``TDDFDD_A`` - TDD/FDD control bits (A)
  - ``/debug/hw/exfe10_4ch_exp/0/reg/0x36/TDDFDD_A``

* - ``SW_AB``/``TDDFDD_B`` - TDD/FDD control bits (B)
  - ``/debug/hw/exfe10_4ch_exp/0/reg/0x36/TDDFDD_B``

* - ``SW_AB``/``PA_ON_A`` - PA on control for A
  - ``/debug/hw/exfe10_4ch_exp/0/reg/0x36/PA_ON_A``

* - ``SW_AB``/``PA_ON_B`` - PA on control for B
  - ``/debug/hw/exfe10_4ch_exp/0/reg/0x36/PA_ON_B``

* - ``SW_AB``/``RXTX_A`` - RX/TX switch control for A
  - ``/debug/hw/exfe10_4ch_exp/0/reg/0x36/RXTX_A``

* - ``SW_AB``/``RXTX_B`` - RX/TX switch control for B
  - ``/debug/hw/exfe10_4ch_exp/0/reg/0x36/RXTX_B``

* - ``P_A_EN_CD``/``D`` - Enable CHD (PA enable CD)
  - ``/debug/hw/exfe10_4ch_exp/0/reg/0x37/D``

* - ``P_A_EN_CD``/``C`` - Enable CHC (PA enable CD)
  - ``/debug/hw/exfe10_4ch_exp/0/reg/0x37/C``

* - ``ATTN_RX_CH_CD``/``D`` - Attenuator CHD
  - ``/debug/hw/exfe10_4ch_exp/0/reg/0x38/D``

* - ``ATTN_RX_CH_CD``/``C`` - Attenuator CHC
  - ``/debug/hw/exfe10_4ch_exp/0/reg/0x38/C``

* - ``SW_CD``/``TDDFDD_C`` - TDD/FDD control bits (C)
  - ``/debug/hw/exfe10_4ch_exp/0/reg/0x39/TDDFDD_C``

* - ``SW_CD``/``TDDFDD_D`` - TDD/FDD control bits (D)
  - ``/debug/hw/exfe10_4ch_exp/0/reg/0x39/TDDFDD_D``

* - ``SW_CD``/``PA_ON_C`` - PA on control for C
  - ``/debug/hw/exfe10_4ch_exp/0/reg/0x39/PA_ON_C``

* - ``SW_CD``/``PA_ON_D`` - PA on control for D
  - ``/debug/hw/exfe10_4ch_exp/0/reg/0x39/PA_ON_D``

* - ``SW_CD``/``RXTX_C`` - RX/TX switch control for C
  - ``/debug/hw/exfe10_4ch_exp/0/reg/0x39/RXTX_C``

* - ``SW_CD``/``RXTX_D`` - RX/TX switch control for D
  - ``/debug/hw/exfe10_4ch_exp/0/reg/0x39/RXTX_D``

Software
========

.. note::
   | You must install the required software and driver packages first.
   | Please refer to the :doc:`/software/install`.

In order to use FE, you can use the **usdr_dm_create** utility to receive or transmit data.

The following example creates a raw IQ data file with a sample rate of 10 MSamples per second per channel, a center frequency of 1700 MHz, using all 4 RX channels:

.. code-block:: bash

   usdr_dm_create -D -r10e6 -l3 -e1700e6 -c -1 -f output.raw

The software stack supports the **SoapySDR** interface, so you can use any compatible application.
