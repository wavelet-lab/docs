=========
xMASS SDR
=========

A modular, high-performance **8×8 MIMO transceiver** designed for **4G/5G applications** and other use cases.

.. image:: ../_static/xmass-front-lg.png
   :alt: xmass sdr

Overview
========

The xMASS SDR is a modular, high-performance **MIMO transceiver** featuring **8 RX and 8 TX channels** which can be synchronized. Its modular design allows for easy maintenance and enables the construction of high-order MIMO systems using the same building blocks.

.. image:: ../_static/xmass-iso-open-lg.png
   :alt: xmass sdr

General Specifications
----------------------

**FPGA**  
  - 4× AMD XC7A35T  

**Clock Synchronization**  
  - LMK05318  

**Module Host Interface**  
  - PCIe 3.0 x2 connection  

**Form Factor**  
  - PCIe x4 (2 PCIe lanes used)  

**Power Consumption**  
  - 20W Typical

**Extended Power Supply Range**  
  - 2.85 - 5.5 V  

RF Specifications
-----------------

**RFIC**  
  - 4× LMS7002  

**Frequency Range**  
  - 30 MHz to 3.8 GHz  

**Sample Rate**  
  - 0.1 MSps - 100 MSps  

**Channel Bandwidth**  
  - 0.5 MHz - 90 MHz  

Bifurcation Modes
-----------------

- **Full 8×8 MIMO**  
- **2 independent 4×4 MIMO systems**  
- **4 independent 2×2 MIMO systems**  

Target Applications
-------------------

**Spectrum Monitoring**  
  - **4× M.2 2230 Key A+E xSDR** for comprehensive frequency analysis and monitoring  

**Cellular Communication**  
  - Enables next-generation **4G/5G wireless networks** with high-order **massive MIMO**  
  - Fully compatible with **Amarisoft** and **srsRAN**  

**Directional Finding**  
  - Determines the **direction of arrival (DoA)** of incoming radio signals, enabling **precise localization** of transmitters  

**Beamforming**  
  - Focuses signal transmission and reception in specific directions  
  - Enhances range, improves signal quality, and reduces interference in multi-user environments

Connections
===========

.. image:: ../_static/xmass_fron_open.png
   :alt: xmass sdr

Front side
----------

.. note::
   | USB-C is connected to the xSDR A and is intended solely for use in manufacturing test facilities.
   | It is not used during normal operation.

The xMASS SDR has 4 slots for M.2 xSDR modules. Slot A is the master module and is required for the xMASS to control the AF part of the board.

.. image:: ../_static/xmass/xmass_wiring.png
   :alt: xmass sdr

The MHF4 connector of each xSDR module should be connected as shown in the picture above. Please note that the cables should be connected crosswise.

Back side
---------

.. image:: ../_static/xmass_back_zoom_light.jpg
   :alt: xmass sdr

PCI bracket panel
-----------------

The bracket panel of the xMASS SDR has 16 external MMCX connectors for RF signals. The top 8 connectors are RX channels, and the bottom 8 connectors are TX channels.


Clocks and synchronization
==========================

.. image:: ../_static/xmass/xmass_sync.png
   :alt: xmass sdr clocks and synchronization block diagram

There are two clock domains on the xMASS SDR:

* **REFCLK**: Reference clock used for phase synchronization and RF frequency calibration.
* **SYSREF**: Event synchronization: start, stop, and other control signals.

The **LMK05318B** serves as the central clocking IC on the xMASS SDR and can use different clock sources:

* On-board crystal oscillator.
* External reference clock input (10 MHz typical; range: 10 MHz to 40 MHz).
* GPS synchronization using the on-board GPS module.

The IC produces the following output signals:

* Reference clock output to all xSDR modules.
* SYSREF output to all xSDR modules.
* Calibrated reference clock output for the RF calibration loop.

Standalone mode
---------------

Standalone mode is used when only one xMASS SDR is present. In this mode most distribution schemes can be avoided, and synchronization buses should be connected as follows:

* ``REF_OUT_A`` to ``REF_IN``.
* ``SYSREF_OUT`` to ``SYSREF_IN``.

.. note::
   | Bold blue dotted lines in the picture above show the connections for standalone mode.

Multiboard mode
---------------

If you need to use multiple xMASS SDR boards synchronized together, you can use the following connection scheme:

* ``OUT_REF_B0`` to ``REF_IN`` on the same (master) board.
* ``OUT_REF_B1``, ``OUT_REF_B2`` and ``OUT_REF_B3`` to ``REF_IN`` on each additional (slave) board, respectively.
* ``SYSREF_OUT`` to ``SYSREF_B_IN`` on the same (master) board.
* ``SYSREF_B_0`` to ``SYSREF_IN`` on the same (master) board.
* ``SYSREF_B_1``, ``SYSREF_B_2`` and ``SYSREF_B_3`` to ``SYSREF_IN`` on each additional (slave) board, respectively.

.. note::
   | Bold green dotted lines in the picture above show the connections for multiboard mode.

RF distribution
===============

.. image:: ../_static/xmass/xmass_rf.png
   :alt: xmass sdr rf distribution block diagram

.. note::
   | The diagram above shows the RF distribution for one pair of RX/TX channels.
   | The rest of the channels are connected in the same way.

In standalone mode, the RF distribution should be connected as follows:

* ``RF_CAL_OUT`` to ``RF_CAL_IN``.

In multiboard mode, the RF distribution should be connected as follows:

* ``RF_CAL_OUT`` to ``RF_B_IN`` on the same (master) board.
* ``RF_0`` to ``RF_CAL_IN`` on the same (master) board.
* ``RF_1``, ``RF_2`` and ``RF_3`` to ``RF_CAL_IN`` on each additional (slave) board, respectively.

.. note::
   | Bold blue dotted lines in the picture above show connections for standalone mode.
   | Bold green dotted lines in the picture above show connections for multiboard mode.


Calibration network
-------------------

The board includes a NOISE source that can be used for calibration and testing.
In addition, the **LMK05318B** can provide a calibrated reference signal for the RF calibration loop.

Calibration signals can be routed to each channel using series software-controlled switches.

The possible RF paths are:

* Normal RX/TX path: TX from MMCX to xSDR module and RX from xSDR module to MMCX.
* Calibration path: NOISE or CAL signal to xSDR module for RX calibration.
* Loopback path: TX from xSDR module to RX of the same channel for loopback testing.

In addition, the NOISE/CAL signal can be routed to the first channel(LNAL_A) of each xSDR module directly through the M.2 socket.
This avoids using the RF frontend, resulting in more accurate calibration.


Frontend control
================

.. note::
   | In order to control the frontend from software, you need to use the ``usdr_registers`` tool.
   | Please refer to the :doc:`/software/usdr_registers`.


Frontend control registers map
==============================


GENERAL
-------

.. list-table::
   :header-rows: 1

   * - Register
     - Type
     - Values/Range
     - Unit
     - Description
   * - /dm/sdr/0/usbclk
     - TODO
     - TODO
     - TODO
     - USB/PHY clock setting
   * - /dm/sdr/0/calibrate
     - bool/command
     - TODO
     - TODO
     - calibration trigger
   * - /dm/sdr/0/vio
     - TODO
     - TODO
     - TODO
     - TODO
   * - /dm/sdr/0/tx/phase_ovr
     - TODO
     - TODO
     - TODO
     - TODO
   * - /dm/sdr/0/tx/phase_ovr_ia
     - TODO
     - TODO
     - TODO
     - TODO
   * - /dm/sdr/0/tx/phase_ovr_rc
     - TODO
     - TODO
     - TODO
     - TODO
   * - /dm/sdr/0/rx/phase_ovr
     - TODO
     - TODO
     - TODO
     - TODO
   * - /dm/sdr/0/rx/dccorr
     - TODO
     - TODO
     - TODO
     - RX DC correction (I/Q offsets)
   * - /dm/sdr/0/tx/dccorr
     - TODO
     - TODO
     - TODO
     - TX DC correction (I/Q offsets)
   * - /dm/sdr/0/rx/phgaincorr
     - TODO
     - TODO
     - TODO
     - TODO
   * - /dm/sdr/0/tx/phgaincorr
     - TODO
     - TODO
     - TODO
     - TODO
   * - /dm/sdr/0/rx/freqency/bb
     - TODO
     - TODO
     - TODO
     - TODO
   * - /dm/sdr/0/tx/freqency/bb
     - TODO
     - TODO
     - TODO
     - TODO
   * - /dm/sdr/0/rx/freqency
     - ==TODO
     - ==TODO
     - ==TODO
     - RX LO frequency
   * - /dm/sdr/0/tx/freqency
     - TODO
     - TODO
     - TODO
     - TX LO frequency
   * - /dm/sdr/0/tx/gain
     - ==TODO
     - ==TODO
     - ==TODO
     - Total TX gain
   * - /dm/sdr/0/tx/gain/lb
     - ==TODO
     - ==TODO
     - ==TODO
     - TX loopback gain
   * - /dm/sdr/0/tx/gain/vga1
     - ==TODO
     - ==TODO
     - ==TODO
     - TX VGA1 gain
   * - /dm/sdr/0/rx/gain
     - ==TODO
     - ==TODO
     - ==TODO
     - Total RX gain
   * - /dm/sdr/0/rx/gain/pga
     - ==TODO
     - ==TODO
     - ==TODO
     - RX PGA gain
   * - /dm/sdr/0/rx/gain/vga
     - ==TODO
     - ==TODO
     - ==TODO
     - RX VGA gain
   * - /dm/sdr/0/rx/gain/lna
     - ==TODO
     - ==TODO
     - ==TODO
     - RX LNA gain
   * - /dm/sdr/0/rx/gain/lb
     - ==TODO
     - ==TODO
     - ==TODO
     - RX loopback gain
   * - /dm/sdr/0/rx/rfic_path
     - TODO
     - TODO
     - TODO
     - TODO
   * - /dm/sdr/0/tx/rfic_path
     - TODO
     - TODO
     - TODO
     - TODO
   * - /dm/sdr/0/rx/path
     - enum
     - - 0 - AUTO
       - 1 - LNAL
       - 2 - LNAW
       - 3 - LNAH
       - 4 - ADC
       - 5 - LNAL_LB
       - 6 - LNAW_LB
       - 7 - LNAH_LB
     -
     - RX path / antenna selection
   * - /dm/sdr/0/tx/path
     - enum
     - - 0 - AUTO
       - 1 - B1: TXH/TXW
       - 2 - B2: TXL
       - 3 - W: 0-2.5G
       - 4 - H: 2.5G-3.9G
     -
     - TX path / antenna selection
   * - /dm/sdr/0/rx/dccorrmode
     - TODO
     - TODO
     - TODO
     - TODO
   * - /dm/sdr/0/rx/bandwidth
     - float
     - TODO
     - Hz
     - RX LPF/BW
   * - /dm/sdr/0/tx/bandwidth
     - float
     - TODO
     - Hz
     - TX LPF/BW
   * - /dm/sdr/0/rxdsp/swapab
     - TODO
     - TODO
     - TODO
     - TODO
   * - /dm/sdr/0/tdd/freqency
     - TODO
     - TODO
     - TODO
     - TODO
   * - /dm/sdr/0/tfe/antcfg
     - TODO
     - TODO
     - TODO
     - TODO
   * - /dm/sdr/0/tfe/generator/enable
     - TODO
     - TODO
     - TODO
     - TODO
   * - /dm/sdr/0/tfe/generator/const
     - TODO
     - TODO
     - TODO
     - TODO
   * - /dm/sdr/0/tfe/generator/tone
     - TODO
     - TODO
     - TODO
     - TODO
   * - /dm/sdr/0/tfe/nco/enable
     - TODO
     - TODO
     - TODO
     - TODO
   * - /dm/sdr/0/tfe/nco/freqency
     - TODO
     - TODO
     - TODO
     - TODO
   * - /dm/sdr/0/rfe/throttle
     - TODO
     - TODO
     - TODO
     - TODO
   * - /dm/sdr/0/rfe/nco/enable
     - TODO
     - TODO
     - TODO
     - TODO
   * - /dm/sdr/0/rfe/nco/freqency
     - TODO
     - TODO
     - TODO
     - TODO
   * - /dm/sdr/0/rfe/prdc
     - TODO
     - TODO
     - TODO
     - TODO
   * - /dm/sdr/0/core/atcrbs/reg
     - TODO
     - TODO
     - TODO
     - TODO
   * - /dm/sdr/0/dac_vctcxo
     - TODO
     - TODO
     - TODO
     - TODO
   * - /dm/sdr/0/phy_rx_dly
     - TODO
     - TODO
     - TODO
     - TODO
   * - /dm/sdr/0/phy_rx_fsr
     - TODO
     - TODO
     - TODO
     - TODO
   * - /dm/sdr/0/phy_tx_fsr
     - TODO
     - TODO
     - TODO
     - TODO
   * - /dm/sdr/0/phy_tx_iqsel
     - TODO
     - TODO
     - TODO
     - TODO
   * - /dm/sdr/0/phyrx/ml
     - TODO
     - TODO
     - TODO
     - TODO
   * - /dm/sdr/0/sync/cal/freq
     - float
     - ??? 1000000.0 -- 499000000.99
     - Hz
     - LO calibration frequency
   * - /dm/sdr/0/sync/cal/path
     - enum
     -  - 0 - Normal operation
        - 1 - LO
        - 2 - NOISE
        - 3 - LO_LNA3
        - 4 - NOISE_LNA3
     -
     - Calibration path selection


xmass_ctrl
----------


TODO: description of the low level controls register map.

.. image:: ../_static/xmass/xmass_control_xmass.png
   :alt: xmass sdr frontend control screenshot

