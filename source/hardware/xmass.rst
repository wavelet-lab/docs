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


xmass_ctrl
----------


.. image:: ../_static/xmass/xmass_control_xmass.png
   :alt: xmass sdr frontend control screenshot


.. list-table::
   :header-rows: 1

   * - Parameter
     - Description
   * - BDISTRIB
     - Enable OUT_REF_B and OUT_SYSREF_B for 4 sync boards
   * - BLOCAL
     - Enable local PPS and REF distribution
   * - RF_CAL_DST_SEL
     - 0 - RF_CAL_EXT (general RX port) / 1 - RF_CAL_INT (LNA3 port)
   * - RF_CAL_SRC_SEL
     - 0 - RF_LO_SRC (from LMK) / 1 - RF_NOISE_SRC (from NOISE GEN)
   * - GPS_PWREN
     - Enable GPS module and DC-bias
   * - LMK_SYNCN
     - Set LMK05318B SYNC_N port
   * - SYSREF_1PPS_SEL
     - 0 - LMK_1PPS / 1 - From SDR_A
   * - EN_LMX
     - Enable LMK05318B
   * - RF_EN
     - Enables Power Amplifiers
   * - RF_CAL_SW
     - 0 - Use RF cal source as FB / 1 - Use XSDR TX as FB
   * - RF_LB_SW
     - 0 - Normal operation / 1 - use loopback path to XSDR RX
   * - RF_NOISE_EN
     - Enable 14V generator for Zener noise source
   * - SYSREF_GPSRX_SEL
     - 0 - TX_SYREF_MUX demultiplexing to CLK_SYSREF_OUT / 1 - TX_SYREF_MUX to GPS_RX
   * - RTS
     - Interboard sync logic


lmk05318
---------


.. list-table::
   :header-rows: 1

   * - Register
     - Field
     - Description
   * - DEV_CTL
     - RESET_SW
     - Software Reset ALL functions
   * - DEV_CTL
     - SYNC_SW
     - Output Synchronization (SYNC) Assert bit
   * - DEV_CTL
     - SYNC_AUTO_DPLL
     - Enable Automatic Output SYNC after DPLL lock
   * - DEV_CTL
     - SYNC_AUTO_APLL
     - Enable Automatic Output SYNC after PLL lock
   * - DEV_CTL
     - SYNC_MUTE
     - Determines if the output drivers are muted during a SYNC event, 0x0 = Do not mute any outputs during SYNC, 0x1 = Mute all outputs during SYNC
   * - DEV_CTL
     - PLLSTRTMODE
     - PLL Startup Mode . When using cascade mode, PLL1 is fixed to a center value while PLL2 locks. Then PLL1 performs final lock.
   * - DEV_CTL
     - AUTOSTRT
     - Autostart. If AUTOSTRT is set to 1, the device will automatically initiate the PLL and output start-up sequence after a device reset. A device reset can be triggered by the power-on-reset, PDN pin, or by writing to the RESET_SW bit. If AUTOSTRT is 0, the device will halt after the configuration phase; a subsequent write to set the AUTOSTRT bit will initiate the start-up sequence. In Test mode, the AUTOSTRT bit is ignored after device reset, but start-up can be triggered by a subsequent write to set the AUTOSTART bit.
   * - INT_LIVE0
     - LOS_FDET_XO
     - Loss of source freq detection XO
   * - INT_LIVE0
     - LOL_PLL2
     - Loss of Lock APLL2
   * - INT_LIVE0
     - LOL_PLL1
     - Loss of Lock APLL1
   * - INT_LIVE0
     - LOS_XO
     - Loss of source XO
   * - INT_LIVE1
     - LOPL_DPLL
     - Loss of phase lock DPLL
   * - INT_LIVE1
     - LOFL_DPLL
     - Loss of frequency lock DPLL
   * - INT_LIVE1
     - HIST
     - Tuning word history update DPLL
   * - INT_LIVE1
     - HLDOVR
     - Holdover event DPLL
   * - INT_LIVE1
     - REFSWITCH
     - Reference switchover DPLL
   * - INT_LIVE1
     - LOR_MISSCLK
     - Loss of active reference missing clock DPLL
   * - INT_LIVE1
     - LOR_FREQ
     - Loss of active reference frequency DPLL
   * - INT_LIVE1
     - LOR_AMP
     - Loss of active reference amplitude DPLL
   * - INT_MASK0
     - LOS_FDET_XO_MASK
     - Mask Loss of Source Freq Det XO When set to 1, interrupt output is not triggered.
   * - INT_MASK0
     - LOL_PLL2_MASK
     - Mask Loss of Lock APLL2 When set to 1, interrupt output is not triggered.
   * - INT_MASK0
     - LOL_PLL1_MASK
     - Mask Loss of Lock APLL1 When set to 1, interrupt output is not triggered.
   * - INT_MASK0
     - LOS_XO_MASK
     - Mask Loss of source XO When set to 1, interrupt output is not triggered.
   * - INT_MASK1
     - LOPL_DPLL_MASK
     - Mask Loss of Phase Lock DPLL When set to 1, interrupt output is not triggered.
   * - INT_MASK1
     - LOFL_DPLL_MASK
     - Mask Loss of Freq Lock DPLL When set to 1, interrupt output is not triggered.
   * - INT_MASK1
     - HIST_MASK
     - Mask Tuning word history update DPLL When set to 1, interrupt output is not triggered.
   * - INT_MASK1
     - HLDOVR_MASK
     - Mask Holdover event DPLL When set to 1, interrupt output is not triggered.
   * - INT_MASK1
     - REFSWITCH_MASK
     - Mask Reference switchover DPLL When set to 1, interrupt output is not triggered.
   * - INT_MASK1
     - LOR_MISSCLK_MASK
     - Mask Loss of active reference missing clk DPLL When set to 1, interrupt output is not triggered.
   * - INT_MASK1
     - LOR_FREQ_MASK
     - Mask Loss of active reference freq DPLL When set to 1, interrupt output is not triggered.
   * - INT_MASK1
     - LOR_AMP_MASK
     - Mask Loss of active reference amplitude DPLL When set to 1, interrupt output is not triggered.
   * - INT_FLAG_POL0
     - LOS_FDET_XO_POL
     - LOS_FDET_XO Flag Polarity
   * - INT_FLAG_POL0
     - LOL_PLL2_POL
     - LOL_PLL2 Flag Polarity
   * - INT_FLAG_POL0
     - LOL_PLL1_POL
     - LOL_PLL1 Flag Polarity
   * - INT_FLAG_POL0
     - LOS_XO_POL
     - LOS_XO Flag Polarity
   * - INT_FLAG_POL1
     - LOPL_DPLL_POL
     - LOPL_DPLL Flag Polarity
   * - INT_FLAG_POL1
     - LOFL_DPLL_POL
     - LOFL_DPLL Flag Polarity
   * - INT_FLAG_POL1
     - HIST_POL
     - HIST Flag Polarity
   * - INT_FLAG_POL1
     - HLDOVR_POL
     - HLDOVR Flag Polarity
   * - INT_FLAG_POL1
     - REFSWITCH_POL
     - REFSWITCH Flag Polarity
   * - INT_FLAG_POL1
     - LOR_MISSCLK_POL
     - LOR_MISSCLK Flag Polarity
   * - INT_FLAG_POL1
     - LOR_FREQ_POL
     - LOR_FREQ Flag Polarity
   * - INT_FLAG_POL1
     - LOR_AMP_POL
     - LOR_AMP Flag Polarity
   * - INT_FLAG0
     - LOS_FDET_XO_INTR
     - LOL_FDET_XO Interrupt Bit is set when an edge of the correct polarity is detected on the LOL_FDET_XO interrupt source. The bit is cleared by writing a 0.
   * - INT_FLAG0
     - LOL_PLL2_INTR
     - LOL_PLL2 Interrupt Bit is set when an edge of the correct polarity is detected on the LOL_PLL2 interrupt source. The bit is cleared by writing a 0.
   * - INT_FLAG0
     - LOL_PLL1_INTR
     - LOL_PLL1 Interrupt Bit is set when an edge of the correct polarity is detected on the LOL_PLL1 interrupt source.The bit is cleared by writing a 0.
   * - INT_FLAG0
     - LOS_XO_INTR
     - LOS_XO Interrupt Bit is set when an edge of the correct polarity is detected on the LOS_XO interrupt source. The bit is cleared by writing a 0.
   * - INT_FLAG1
     - LOPL_DPLL_INTR
     - LOPL_DPLL Interrupt Bit is set when an edge of the correct polarity is detected on the LOPL_DPLL interrupt source. The bit is cleared by writing a 0.
   * - INT_FLAG1
     - LOFL_DPLL_INTR
     - LOFL_DPLL Interrupt Bit is set when an edge of the correct polarity is detected on the LOFL_DPLL interrupt source. The bit is cleared by writing a 0.
   * - INT_FLAG1
     - HIST_INTR
     - HIST Interrupt Bit is set when an edge of the correct polarity is detected on the HIST interrupt source. The bit is cleared by writing a 0.
   * - INT_FLAG1
     - HLDOVR_INTR
     - HLDOVR Interrupt Bit is set when an edge of the correct polarity is detected on the HLDOVR interrupt source. The bit is cleared by writing a 0.
   * - INT_FLAG1
     - REFSWITCH_INTR
     - REFSWITCH Interrupt Bit is set when an edge of the correct polarity is detected on the REFSWITCH interrupt source. The bit is cleared by writing a 0.
   * - INT_FLAG1
     - LOR_MISSCLK_INTR
     - LOR_MISSCLK Interrupt Bit is set when an edge of the correct polarity is detected on the LOR_MISSCLK interrupt source. The bit is cleared by writing a 0.
   * - INT_FLAG1
     - LOR_FREQ_INTR
     - LOR_FREQ Interrupt Bit is set when an edge of the correct polarity is detected on the LOR_FREQ interrupt source. The bit is cleared by writing a 0.
   * - INT_FLAG1
     - LOR_AMP_INTR
     - LOR_AMP Interrupt Bit is set when an edge of the correct polarity is detected on the LOR_AMP interrupt source. The bit is cleared by writing a 0.
   * - INTCTL
     - INT_AND_OR
     - Interrupt Logical AND or OR Combination 0x0 = OR Any un-masked interrupt flags can generate an interrupt. 0x1 = AND All un-masked interrupt flags must be active in order to generate an interrupt.
   * - INTCTL
     - INT_EN
     - Interrupt Enable
   * - STAT_POL
     - STAT1_POL
     - STATUS1 Output Polarity Defines the polarity of information presented on the STATUS1 output. If STAT1_POL is set to 1 then STATUS1 is active high, if STAT1_POL is 0then STATUS1 is active low.
   * - STAT_POL
     - STAT0_POL
     - STATUS0 Output Polarity Defines the polarity of information presented on the STATUS0 output. If STAT0_POL is set to 1 then STATUS0 is active high, if STAT0_POL is 0then STATUS0 is active low
   * - MUTELVL1
     - CH3_MUTE_LVL
     - Output 3 Mute Level See CH0_MUTE_LVL for description and bit settings.
   * - MUTELVL1
     - CH2_MUTE_LVL
     - Output 2 Mute Level See CH0_MUTE_LVL for description and bit settings.
   * - MUTELVL1
     - CH1_MUTE_LVL
     - Output 1 Mute Level See CH0_MUTE_LVL for description and bit settings.
   * - MUTELVL1
     - CH0_MUTE_LVL
     - Output 0 Mute Level Determines the configuration of the Output Driver during mute. 0x0 = Bypass Mute (Normal Operation) 0x1 = For DIFF or HCSL mute to differential Vocm. For LVCMOS, P is Bypass Mute and N is Mute Low. 0x2 = For DIFF or HCSL mute to differntial High. For LVCMOS, P is Mute Low and N is Bypass Mute. 0x3 = For DIFF or HCSL mute to differential Low. For LVCMOS, P is Mute Low and N is Mute Low.
   * - MUTELVL2
     - CH7_MUTE_LVL
     - Output 7 Mute Level See CH0_MUTE_LVL for description and bit settings.
   * - MUTELVL2
     - CH6_MUTE_LVL
     - Output 6 Mute Level See CH0_MUTE_LVL for description and bit settings.
   * - MUTELVL2
     - CH5_MUTE_LVL
     - Output 5 Mute Level See CH0_MUTE_LVL for description and bit settings.
   * - MUTELVL2
     - CH4_MUTE_LVL
     - Output 4 Mute Level See CH0_MUTE_LVL for description and bit settings.
   * - OUT_MUTE
     - CH7_MUTE
     - Output 7 Mute Control
   * - OUT_MUTE
     - CH6_MUTE
     - Output 6 Mute Control
   * - OUT_MUTE
     - CH5_MUTE
     - Output 5 Mute Control
   * - OUT_MUTE
     - CH4_MUTE
     - Output 4 Mute Control
   * - OUT_MUTE
     - CH3_MUTE
     - Output 3 Mute Control
   * - OUT_MUTE
     - CH2_MUTE
     - Output 2 Mute Control
   * - OUT_MUTE
     - CH1_MUTE
     - Output 1 Mute Control
   * - OUT_MUTE
     - CH0_MUTE
     - Output 0 Mute Control
   * - DPLL_MUTE
     - MUTE_APLL2_LOCK
     - APLL2 mute enabled during PLL lock
   * - DPLL_MUTE
     - MUTE_DPLL_PHLOCK
     - DPLL mute enabled during phase lock
   * - DPLL_MUTE
     - MUTE_DPLL_FLLOCK
     - DPLL mute enabled during DPLL lock
   * - DPLL_MUTE
     - MUTE_APLL1_LOCK
     - APLL1 mute enabled during PLL lock
   * - GPIO_OUT
     - GPIO_STAT1_OUT
     - STAT1 Driver Type Output; 0x0 = NMOS Open-drain driver; 0x1 = LVCMOS driver
   * - GPIO_OUT
     - GPIO_STAT0_OUT
     - STAT0 Driver Type Output; 0x0 = NMOS Open-drain driver; 0x1 = LVCMOS driver
   * - SPARE_NVMBASE2_BY2
     - GPIO2_OUT
     - GPIO2 Driver Type GPIO2; 0x0 = NMOS Open-drain driver; 0x1 = LVCMOS driver
   * - SPARE_NVMBASE2_BY2
     - APLL1_DEN_MODE
     - Programmable APLL1 denominator mode; 0x0 = APLL1 uses programmable 40-bit numerator (R110, R111, R112, R113, R114) and fixed 40-bit denominator; 0x1 = APLL1 uses programmable 24-bit numberator (R339, R110, R111) and programmable 24-bit denominator (R112, R113, R114)
   * - SPARE_NVMBASE2_BY1
     - SECREF_DC_MODE
     - SECREF DC buffer mode; 0x0 = SECREF is AC coupled internally; 0x1 = SECREF is DC coupled internally
   * - SPARE_NVMBASE2_BY1
     - PRIREF_DC_MODE
     - PRIREF DC buffer mode; 0x0 = PRIREF is AC coupled internally; 0x1 = PRIREF is DC coupled internally
   * - SPARE_NVMBASE2_BY1
     - APLL2_DEN_MODE
     - Programmable APLL2 denominator mode; 0x0 = APLL2 uses fixed 24-bit denominator; 0x1 = APLL2 uses programmable 24-bit denominator (R333, R334, R335)
   * - XO_CLKCTL1
     - OSCIN_DBLR_EN
     - Enable OSCIn doubler
   * - XO_CLKCTL1
     - XO_FDET_BYP
     - XO Frequency Detector Bypass If bypassed, the XO detector status is ignored and the XO input is considered valid by the PLL control state machines
   * - XO_CLKCTL1
     - XO_DETECT_BYP
     - XO Amplitude Detector Bypass. If bypassed, the XO input is considered to be valid by the PLL control state machines. XO_DETECT_BYP bit has no effect on the Interrupt register or status outputs.
   * - XO_CLKCTL1
     - XO_BUFSEL
     - XO Input Buffer Enable
   * - XO_CLKCTL2
     - XO_CLKCTL2_RESERVED7
     - reset=1
   * - XO_CLKCTL2
     - XO_TYPE
     - XO Input Type; 0x0 = DC-Differential (external termination); 0x1 = AC-Differential (external termination); 0x3 = AC-Differential (internal termination 100-Ω); 0x4 = HCSL (internal termination 50-Ω); 0x8 = CMOS; 0xC = Single-ended (internal termination 50-Ω)
   * - XO_CLKCTL2
     - XO_CLKCTL2_RESERVED0
     - reset=0x10
   * - XO_CONFIG
     - OSCIN_RDIV
     - Oscillator Input Divider
   * - REF_CLKCTL1
     - SECREF_CMOS_SLEW
     - SECREF input buffer slew rate; 0x0 = Select Amplitude Detector Mode; 0x1 = Select CMOS Amplitude Detector Mode
   * - REF_CLKCTL1
     - PRIREF_CMOS_SLEW
     - PRIREF input buffer slew rate; 0x0 = Select Amplitude Detector Mode; 0x1 = Select CMOS Amplitude Detector Mode
   * - REF_CLKCTL1
     - SECREF_BUF_MODE
     - SECREF buffer mode. 0x0 - Set AC buffer hysteresis to 50mV or enable DC buffer hysteresis; 0x1 = Set AC buffer hysteresis to 200mV or disable DC buffer hysteresis
   * - REF_CLKCTL1
     - PRIREF_BUF_MODE
     - PRIREF buffer mode. 0x0 - Set AC buffer hysteresis to 50mV or enable DC buffer hysteresis; 0x1 = Set AC buffer hysteresis to 200mV or disable DC buffer hysteresis
   * - REF_CLKCTL2
     - SECREF_TYPE
     - SECREF Input Type See PRIREF_TYPE for input type bit settings.
   * - REF_CLKCTL2
     - PRIREF_TYPE
     - PRIREF Input Type
   * - PLL_CLK_CFG
     - PLL2_RCLK_SEL
     - PLL2 Reference clock selection; 0x0 = VCO1 - Cascaded Mode; 0x1 = XO
   * - PLL_CLK_CFG
     - PLL1_VCO_TO_CNTRS_EN
     - PLL1 VCO to counters enable. Enables VCO1 output drivers to PLL1 N counter, DPLL, digital top, PLL2 R divider. Bit 0 enables VCO1 output for DPLL TDC, reference window detect, DPLL loop filter high speed clock and ppm checker clock. Bit 1 enables VCO1 output to PLL1 N counter Bit 2 enables the PLL1_P1 output to PLL2 R divider for loop-back mode.
   * - STAT0_SEL
     - STAT0_SEL
     - STATUS0 Indicator Signal Select The output pin state of 1 indicates the status condition is true; 0x00 = XO Input Loss of Signal (LOS); 0x01 = Low; 0x03 = PLL1 Digital Lock Detect (DLD); 0x04 = PLL1 VCO Calibration Active; 0x05 = PLL1 N Divider, div-by-2; 0x06 = PLL2 Digital Lock Detect (DLD); 0x07 = PLL2 VCO Calibration Active; 0x08 = PLL2 N Divider, div-by-2; 0x09 = EEPROM Active; 0x0A = Interrupt (INTR); 0x0C = DPLL Phase Lock Detected (LOPL); 0x0D = PRIREF Monitor Divider Output, div-by-2; 0x0E = SECREF Monitor Divider Output, div-by-2; 0x0F = PLL2 R Divider, div-by-2; 0x11 = PRIREF Amplitude Monitor Fault; 0x12 = SECREF Amplitude Monitor Fault; 0x15 = PRIREF Frequency Monitor Fault; 0x16 = SECREF Frequency Monitor Fault; 0x19 = PRIREF Missing or Early Pulse Monitor Fault; 0x1A = SECREF Missing or Early Pulse Monitor Fault; 0x1D = PRIREF Validation Timer Active; 0x1E = SECREF Validation Timer Active; 0x25 = PRIREF Phase Validation Monitor Fault; 0x26 = SECREF Phase Validation Monitor Fault; 0x29 = PLL1 Lock Detected (LOL); 0x2A = PLL2 Lock Detected (LOL); 0x40 = DPLL R Divider, div-by-2; 0x41 = DPLL FB Divider, div-by-2; 0x46 = DPLL PRIREF Selected; 0x47 = DPLL SECREF Selected; 0x4A = DPLL Holdover Active; 0x4B = DPLL Reference Switchover Event; 0x4D = DPLL Tuning History Update; 0x4E = DPLL Fast Lock Active; 0x50 = DPLL Loss of Lock (LOFL)
   * - STAT1_SEL
     - STAT1_SEL
     - STATUS1 Indicator Signal Select See STAT0_SEL for status signal and bit settings
   * - PWDN
     - GPIO_FDEV_EN
     - Enable DCO Frequency When enabled, a rising edge on these pins will update the DCO frequency accordingly.
   * - PWDN
     - CH7_PD
     - Channel 7 Powerdown When CH7_PD is 1 the regulator that supplies the divider and drivers for OUT7 will be disabled.
   * - PWDN
     - CH6_PD
     - Channel 6 Powerdown When CH6_PD is 1 the regulator that supplies the divider and drivers for OUT6 will be disabled.
   * - PWDN
     - CH5_PD
     - Channel 5 Powerdown When CH5_PD is 1 the regulator that supplies the divider and drivers for OUT5 will be disabled.
   * - PWDN
     - CH4_PD
     - Channel 4 Powerdown When CH4_PD is 1 the regulator that supplies the divider and drivers for OUT4 will be disabled.
   * - PWDN
     - CH2_3_PD
     - Channel 2 and 3 Powerdown When CH2_3_PD is 1 the regulator that supplies the divider and drivers for OUT2 and OUT3 will be disabled.
   * - PWDN
     - CH0_1_PD
     - Channel 0 and 1 Powerdown When CH0_1_PD is 1 the regulator that supplies the divider and drivers for OUT0 and OUT1 will be disabled.
   * - OUTCTL_0
     - CH0_1_MUX
     - Channel 0 and 1 Output Mux; Selects frequency source for OUT0 and OUT1; 0x0 = APLL1 P1; 0x1 = APLL1 P1 Inverted; 0x2 = APLL2 P1; 0x3 = APLL2 P2
   * - OUTCTL_0
     - OUT0_FMT
     - OUT0 Clock Format; Values not desplayed below are reserved; 0x00 = Disabled; 0x10 = AC-LVDS; 0x14 = AC-CML; 0x18 = AC-LVPECL; 0x2C = HCSL (external termination 50-Ω); 0x2D = HCSL (internal termination 50-Ω)
   * - OUTCTL_1
     - OUT1_FMT
     - OUT1 Clock Format See OUT0_FMT for bit settings
   * - OUTDIV_0_1
     - OUT0_1_DIV
     - Channel 0 and Channel 1 Output Divider This is an 8-bit divider. The valid values for OUT0_1_DIV range from 1 to 255. Output Divider (ODOUT01) = OUT0_1_DIV + 1 Note 0x00 is disabled
   * - OUTCTL_2
     - CH2_3_MUX
     - Channel 2 and 3 Output Mux Selects frequency source for OUT2 and OUT3. See CH0_1_MUX for bit settings
   * - OUTCTL_2
     - OUT2_FMT
     - OUT2 Clock Format See OUT0_FMT for bit settings.
   * - OUTCTL_3
     - OUT3_FMT
     - OUT3 Clock Format See OUT0_FMT for bit settings.
   * - OUTDIV_2_3
     - OUT2_3_DIV
     - Channel 2 and Channel 3 Output Divider See OUT0_1_DIV for description and bit settings.
   * - OUTCTL_4
     - CH4_MUX
     - Channel 4 Output Mux Selects frequency source for OUT4. See CH0_1_MUX for bit settings.
   * - OUTCTL_4
     - OUT4_FMT
     - OUT4 Clock Format Values not desplayed below are reserved. 0x00 = Disabled; 0x10 = AC-LVDS; 0x14 = AC-CML; 0x18 = AC-LVPECL; 0x2C = HCSL (external termination 50-Ω); 0x2D = HCSL (internal termination 50-Ω); 0x30 = LVCMOS(HiZ/HiZ); 0x32 = LVCMOS(HiZ/-); 0x33 = LVCMOS(HiZ/+); 0x35 = LVCMOS(low/low); 0x38 = LVCMOS(-/HiZ); 0x3A = LVCMOS(-/-); 0x3B = LVCMOS(-/+); 0x3C = LVCMOS(+/HiZ); 0x3E = LVCMOS(+/-); 0x3F = LVCMOS(+/+)
   * - OUTDIV_4
     - OUT4_DIV
     - Channel 4 Output Divider See OUT0_1_DIV for description and bit settings.
   * - OUTCTL_5
     - CH5_MUX
     - Channel 5 Output Mux Selects frequency source for OUT5. See CH0_1_MUX for bit settings.
   * - OUTCTL_5
     - OUT5_FMT
     - OUT5 Clock Format See OUT4_FMT for bit settings.
   * - OUTDIV_5
     - OUT5_DIV
     - Channel 5 Output Divider See OUT0_1_DIV for description and bit settings
   * - OUTCTL_6
     - CH6_MUX
     - Channel 6 Output Mux Selects frequency source for OUT6. See CH0_1_MUX for bit settings.
   * - OUTCTL_6
     - OUT6_FMT
     - OUT6 Clock Format See OUT4_FMT for bit settings
   * - OUTDIV_6
     - OUT6_DIV
     - Channel 6 Output Divider See OUT0_1_DIV for description and bit settings
   * - OUTCTL_7
     - CH7_MUX
     - Channel 7 Output Mux Selects frequency source for OUT7. See CH0_1_MUX for bit settings.
   * - OUTCTL_7
     - OUT7_FMT
     - OUT7 Clock Format See OUT4_FMT for bit settings
   * - OUTDIV_7_STG2
     - OUT7_STG2_DIV
     - Channel 7 Stage Two Output Divider OD2 = OUT7_STG2_DIV + 1 If OD2 > 1, then ODout7 must be ≥ 6. Total output 7 divide value = OD2 * ODout7
   * - OUTDIV_7
     - OUT7_DIV
     - Channel 7 Output Divider This is an 8-bit divider. The valid values for OUT7_DIV range from 1 to 255. ODOUT7 = OUT7_DIV + 1. If OD2 > 1, then total output 7 divide value = OD2 * ODout7 where OD2 is OUT7 secondary output divider value. Note 0x00 is disabled.
   * - PREDRIVER
     - PREDRIVER_RESERVED
     - 
   * - PREDRIVER
     - PLL1_CP_BAW
     - APLL1 Charge Pump Current Gain PLL1_CP_BAW ranges from 0 to 15. Gain = PLL1_CP_BAW x 100 μA.
   * - OUTSYNCCTL
     - PLL2_P2_SYNC_EN
     - Enable PLL2 P2 divider channel synchronizatrion
   * - OUTSYNCCTL
     - PLL2_P1_SYNC_EN
     - Enable PLL2 P1 divider channel synchronizatrion
   * - OUTSYNCCTL
     - PLL1_P1_SYNC_EN
     - Enable PLL1 P1 divider channel synchronizatrion
   * - OUTSYNCEN
     - CH7_SYNC_EN
     - Enable Channel 7 output synchronization
   * - OUTSYNCEN
     - CH6_SYNC_EN
     - Enable Channel 6 output synchronization
   * - OUTSYNCEN
     - CH5_SYNC_EN
     - Enable Channel 5 output synchronization
   * - OUTSYNCEN
     - CH4_SYNC_EN
     - Enable Channel 4 output synchronization
   * - OUTSYNCEN
     - CH2_3_SYNC_EN
     - Enable Channels 2 and 3 output synchronization
   * - OUTSYNCEN
     - CH0_1_SYNC_EN
     - Enable Channels 0 and 1 output synchronization
   * - PLL1_CTRL0
     - PLL1_PDN
     - PLL1 Power down The PLL1_PDN bit determines whether PLL1 is automatically enabled and calibrated after a hardware reset; 0x0 = PLL1 Enabled; 0x1 = PLL1 Disabled
   * - PLL1_CALCTRL0
     - BAW_LOCKDET_EN
     - BAW Lock Detect Enable
   * - PLL1_CALCTRL0
     - PLL1_CLSDWAIT
     - Closed Loop Wait Period, VCO calibration time per step (up to 7 steps).
   * - PLL1_CALCTRL0
     - PLL1_VCOWAIT
     - VCO Wait Period. Timeout counter before starting VCO calibration.
   * - BAW_LOCKDET_PPM_MAX_BY1
     - BAW_LOCK
     - BAW Lock Detect Status; 0x0 = Unlocked; 0x1 = Locked
   * - BAW_LOCKDET_PPM_MAX_BY1
     - BAW_LOCK_DET_1
     - BAW VCO Lock Detection
   * - BAW_LOCKDET_PPM_MAX_BY0
     - BAW_LOCK_DET_2
     - BAW VCO Lock Detection
   * - PLL2_CTRL0
     - PLL2_RDIV_SEC
     - APLL2 secondary reference divider in cascaded APLL2 mode; Divider value ranges from 1-32; Divider value = PLL2_RDIV_SEC + 1.
   * - PLL2_CTRL0
     - PLL2_RDIV_PRE
     - APLL2 primary reference divider in cascaded APLL2 mode
   * - PLL2_CTRL0
     - PLL2_PDN
     - PLL2 Power down The PLL2_PDN bit determines whether PLL2 is automatically enabled and calibrated after a hardware reset; 0x0 = PLL2 Enabled; 0x1 = PLL2 Disabled
   * - PLL2_CTRL1
     - PLL2_VM_BYP
     - PLL2 Vtune Monitor Bypass
   * - PLL2_CTRL1
     - PLL2_CP
     - PLL2 Charge Pump Gain; 0x0 = 1.6 mA; 0x1 = 3.2 mA; 0x2 = 4.8 mA; 0x3 = 6.4 mA
   * - PLL2_CTRL2
     - PLL2_P2
     - PLL2 Post-Divider2 Note A RESET is required after changing Divider values. See PLL2_P1 for bit settings.
   * - PLL2_CTRL2
     - PLL2_P1
     - PLL2 Post-Divider1 Note A RESET is required after changing Divider values; 0x0 = Invalid; 0x1 = 2; 0x2 = 3; 0x3 = 4; 0x4 = 5; 0x5 = 6; 0x6 = 7; 0x7 = Invalid
   * - PLL2_CTRL4
     - PLL2_RBLEED_CP
     - PLL2 Bleed resistor selection
   * - PLL2_CALCTRL0
     - PLL2_CLSDWAIT
     - Closed Loop Wait Period VCO calibration time per step (up to 7 steps); 0x0 = 0.3 ms; 0x1 = 3 ms; 0x2 = 30 ms; 0x3 = 300 ms
   * - PLL2_CALCTRL0
     - PLL2_VCOWAIT
     - VCO Wait Period. Timeout counter before starting VCO calibration.
   * - PLL1_MASHCTRL
     - PLL1_DUAL_PH_EN
     - PLL1 DUAL PHASE functionality on the feedback path enabled
   * - PLL1_MASHCTRL
     - PLL1_MASHSEED1
     - Mash Engine seed for second stage
   * - PLL1_MASHCTRL
     - PLL1_MASHSEED0
     - Mash Engine seed for first stage
   * - PLL1_MASHCTRL
     - PLL1_DTHRMODE
     - APLL1 SDM Dither Mode; 0x0 = Weak; 0x1 = Medium; 0x2 = Strong; 0x3 = Disabled
   * - PLL1_MASHCTRL
     - PLL1_ORDER
     - APLL1 SDM Order; 0x0 = Integer Mode; 0x1 = 1st; 0x2 = 2nd; 0x3 = 3rd; 0x4 = 4th
   * - PLL1_MODE
     - PLL1_IGNORE_GPIO_PIN
     - Ignore PLL1 frequency increment or decrement updates via pins
   * - PLL1_MODE
     - PLL1_FDEV_EN
     - Enable PLL1 frequency increment or decrement via pins or registers
   * - PLL1_MODE
     - PLL1_MODE
     - PLL1 operational mode; 0x0 = Free-run mode (APLL only); 0x1 = DPLL mode
   * - PLL1_LF_R2
     - PLL1_LF_R2
     - PLL1 Loop Filter R2, Ohm
   * - PLL1_LF_C1
     - PLL1_LF_C1
     - PLL1 Loop Filter C1. Not Used, fixed 100 pF
   * - PLL1_LF_R3
     - PLL1_LF_R3
     - PLL1 Loop Filter R3, Ohm
   * - PLL1_LF_R4
     - PLL1_LF_R4
     - PLL1 Loop Filter R4, Ohm
   * - PLL2_MASHCTRL
     - PLL2_DTHRMODE
     - SDM Dither Mode; 0x0 = Weak; 0x1 = Medium; 0x2 = Strong; 0x3 = Disabled
   * - PLL2_MASHCTRL
     - PLL2_ORDER
     - APLL2 SDM Order; 0x0 = Integer Mode; 0x1 = 1st; 0x2 = 2nd; 0x3 = 3rd; 0x4 = 4th
   * - PLL2_LF_R2
     - PLL2_LR_R2
     - PLL2 Loop Filter R2 (Ohm)
   * - PLL2_LF_R3
     - PLL2_LR_R3
     - PLL2 Loop Filter R3 (Ohm)
   * - PLL2_LF_R4
     - PLL2_LF_R4
     - PLL2 Loop Filter R4 (Ohm)
   * - PLL2_LF_C3C4
     - PLL2_LF_C4
     - PLL2 Loop Filter C4, pF
   * - PLL2_LF_C3C4
     - PLL2_LF_C3
     - PLL2 Loop Filter C3, pF
   * - XO_OFFSET_SW_TIMER
     - XO_TIMER
     - XO Input Wait Timer Sets the startup time for the oscillator input; 0x0 = 1.6 ms; 0x1 = 3.3 ms; 0x2 = 6.6 ms; 0x3 = 13.1 ms; 0x4 = 26.2 ms; 0x5 = 52.4 ms; 0x6 = 104.9 ms; 0x7 = Reserved
   * - REF01_DETAMP
     - DETECT_MODE_SECREF
     - SECREF Input Energy Detector Mode Control Determines the method for Energy Detection on the SECREF Input. See DETECT_MODE_PRIREF for bit settings.
   * - REF01_DETAMP
     - DETECT_MODE_PRIREF
     - PRIREF Input Energy Detector Mode Control Determines the method for Energy Detection on the PRIREF Input; 0x0 = Rising Slew Rate Detector; 0x1 = Rising and Falling Slew Rate Detector; 0x2 = Falling Slew Rate Detector; 0x3 = VIH/VIL Level Detector
   * - REF01_DETAMP
     - SECREF_LVL_SEL
     - SECREF Input Amplitude Detector See PRIREF_LVL_SEL for description and bit settings.
   * - REF01_DETAMP
     - PRIREF_LVL_SEL
     - PRIREF Input Amplitude Detector Specifies the minimum differential input peak-to-peak swing to be qualified; 0x0 = Vid is 200 mV Differential or 400 mVpp Single-Ended; 0x1 = Vid is 250 mV Differential or 500 mVpp Single-Ended; 0x2 = Vid is 300 mV Differential or 600 mVpp Single-Ended; 0x3 = Vid is 300 mV Differential or 600 mVpp Single-Ended
   * - REF0_DETEN
     - PRIREF_EARLY_DET_EN
     - PRIREF Early Clock Detect Enable
   * - REF0_DETEN
     - PRIREF_PH_VALID_EN
     - PRIREF Phase Valid Detect Enable
   * - REF0_DETEN
     - PRIREF_VALTMR_EN
     - PRIREF Validation Timer Enable
   * - REF0_DETEN
     - PRIREF_PPM_EN
     - PRIREF Frequency ppm Detect Enable
   * - REF0_DETEN
     - PRIREF_MISSCLK_EN
     - PRIREF Missing Clock Detect Enable
   * - REF0_DETEN
     - PRIREF_AMPDET_EN
     - PRIREF Amplitude Detect Enable
   * - REF1_DETEN
     - SECREF_EARLY_DET_EN
     - SECREF Early Clock Detect Enable
   * - REF1_DETEN
     - SECREF_PH_VALID_EN
     - SECREF Phase Valid Detect Enable
   * - REF1_DETEN
     - SECREF_VALTMR_EN
     - SECREF Validation Timer Enable
   * - REF1_DETEN
     - SECREF_PPM_EN
     - SECREF Frequency ppm Detect Enable
   * - REF1_DETEN
     - SECREF_MISSCLK_EN
     - SECREF Missing Clock Detect Enable
   * - REF1_DETEN
     - SECREF_AMPDET_EN
     - SECREF Amplitude Detect Enable
   * - REF_MISSCLK_CTL
     - SECREF_WINDOW_DET
     - SECREF Window Detection
   * - REF_MISSCLK_CTL
     - PRIREF_WINDOW_DET
     - PRIREF Window Detection
   * - REF0_PH_VALID_THR
     - REF0_PH_VALID_THR
     - PRIREF Phase Valid Threshold
   * - REF1_PH_VALID_THR
     - REF1_PH_VALID_THR
     - SECREF Phase Valid Threshold
   * - DPLL_REF01_PRTY
     - DPLL_SECREF_AUTO_PRTY
     - Set priorty for SECREF See DPLL_PRIREF_AUTO_PRTY for bit settings.
   * - DPLL_REF01_PRTY
     - DPLL_PRIREF_AUTO_PRTY
     - Set priorty for PRIREF; 0x1 = First priority; 0x2 = Second priority
   * - DPLL_REF_SWMODE
     - DPLL_REF_MAN_SEL
     - Controls source of manual selection; 0x0 = Software register DPLL_REF_MAN_REG_SEL; 0x1 = Hardware pin REFSEL
   * - DPLL_REF_SWMODE
     - DPLL_REF_MAN_REG_SEL
     - Controls software manual Ref selection; 0x0 = Primary Reference; 0x1 = Secondary Reference
   * - DPLL_REF_SWMODE
     - DPLL_SWITCH_MODE
     - Controls switchover mode; 0x0 = Auto non-revertive; 0x1 = Auto revertive; 0x2 = Manual fallback; 0x3 = Manual holdover
   * - DPLL_GEN_CTL
     - DPLL_ZDM_SYNC_EN
     - DPLL Zero Delay Synchronization enable
   * - DPLL_GEN_CTL
     - DPLL_ZDM_NDIV_RST_DIS
     - DPLL NDIV reset disable when ZDM mode is enabled
   * - DPLL_GEN_CTL
     - DPLL_SWITCHOVER_1
     - DPLL Switchover Timer
   * - DPLL_GEN_CTL
     - DPLL_FASTLOCK_ALWAYS
     - Enable DPLL fast lock
   * - DPLL_GEN_CTL
     - DPLL_LOCKDET_PPM_EN
     - Enable DPLL Frequency Lock Detect
   * - DPLL_GEN_CTL
     - DPLL_HLDOVR_MODE
     - DPLL Holdover mode when tuning word history unavailable; 0x0 = Enter free-run mode; 0x1 = Hold last control value prior to holdover
   * - DPLL_GEN_CTL
     - DPLL_LOOP_EN
     - DPLL Enable
   * - DPLL_SWITCHOVER_TMR_EXP
     - DPLL_SWITCHOVER_2
     - DPLL Switchover Timer
   * - DPLL_SWITCHOVER_TMR_MANT_BY1
     - DPLL_SWITCHOVER_3
     - DPLL Switchover Time
   * - DPLL_REF_TDC_CTL
     - DPLL_TDC_SW_MODE
     - DPLL TDC Software Control Enable. Value of TDC control word into the loop-filter is from register dpll_ref_frc_val[35:0].
   * - DPLL_REF_TDC_CTL
     - DPLL_REF_AVOID_SLIP
     - Disable Cycle Slip
   * - DPLL_REF_FB_PREDIV
     - DPLL_REF_FB_PRE_DIV
     - DPLL REF Feedback Pre Divider value Divider value ranges from 2 to 17; Divider value = DPLL_REF_FB_PRE_DIV + 2
   * - DPLL_REF_MASHCTL
     - DPLL_REF_DTHRMODE
     - 
   * - DPLL_REF_MASHCTL
     - DPLL_REF_ORDER
     - 
   * - PLL1_24B_NUM_23_16
     - PLL1_24B_NUM_23_16
     - APPL1 24-bit numerator bits 23:16
   * - DPLL_FDEV_CTL
     - DPLL_FDEV_EN
     - DPLL Freq Incr/Decr enable via pin or reg control
   * - DPLL_FDEV_REG_CTL
     - DPLL_FDEV_REG_UPDATE
     - DPLL Freq Incr/Decr register control Writing this register applies one FINC/FDEC of the Numerator as defined by the FDEV register
   * - PLL1_CALSTAT1
     - PLL1_VM_INSIDE
     - PLL1 VCO Status Denotes if the PLL1 charge pump voltage is within operational range.
   * - PLL2_CALSTAT1
     - PLL2_VM_INSIDE
     - PLL2 VCO Status Denotes if the PLL2 charge pump voltage is within operational range.
   * - REFVALSTAT
     - SECREF_VALSTAT
     - SECREF valid state
   * - REFVALSTAT
     - PRIREF_VALSTAT
     - PRIREF valid state



Software
========

.. note::
   | You must install the required software and driver packages first.
   | Please refer to the :doc:`/software/install`.

In order to use xMASS SDR, you can use the **usdr_dm_create** utility to receive or transmit data.

The following example creates a raw IQ data file with a sample rate of 10 MSamples per second per channel, a center frequency of 1700 MHz, using all 8 RX channels:

.. code-block:: bash

   usdr_dm_create -D bus=pci/dev/usdr0:/dev/usdr1:/dev/usdr2:/dev/usdr3 -r10e6 -l3 -e1700e6 -c -f output.raw

The first device in the list(usdr0 in this example) should be the master xMASS SDR board(slot A).

The software stack supports the **SoapySDR** interface, so you can use any compatible application.
