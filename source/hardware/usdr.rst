===========
uSDR module
===========

A tiny **M.2 single-side component SDR** designed for seamless integration into embedded and portable systems..


.. image:: ../_static/hw_usdr_1.jpg
   :alt: uSDR module


Introduction
============

The uSDR is an **M.2 embedded software-defined radio (SDR) card** ready for integration into systems that support either **M.2 or Mini PCIe** (with an adapter) form factors. It features an **RF tuning range of 250 MHz to 3.8 GHz** with a separate **RX-only band from 1 to 250 MHz**.  

By leveraging applications from the **web platform wsdr.io** and different host devices (**laptops, tablets, smartphones, embedded computers, etc.**), users can immediately build an **RF device** tailored to their needs and share or stream data worldwide.

General Specifications
======================

**FPGA**  
  - AMD XC7A35T  

**Power Consumption**  
  - 2.1W Typical  
  - 3.6W Max  

**Interface**  
  - M.2 2230 A+E key (USB 2.0 & PCIe 2.0 x2)  

**Extended Power Supply Range**  
  - 2.85 - 5.5 V  

RF Specifications
=================

**RFIC**  
  - LMS6002D  
  - LTC5562 UpConverter for **1 - 250 MHz**  

**Frequency Range**  
  - **RX/TX:** 250 MHz to 3.8 GHz  
  - **RX-only band:** 1 - 250 MHz with **7th order 250 MHz LPF**  

**Sample Rate**  
  - 0.1 MSps - 65 MSps  

**Channel Bandwidth**  
  - 0.5 MHz - 40 MHz  

Temperature Range
=================

- **Standard:** 0°C to 85°C  
- **Extended (on request):** -40°C to 105°C  

Target Applications
===================

**Cellular Communication**  
  - Establish dedicated wireless networks by implementing **BTS, eNodeB, or gNodeB** systems via open-source solutions like **srsRAN** or **Amarisoft**  

**Temperature Stability**  
  - **LMS6002D BiCMOS technology** ensures RF stability and predictable performance over a **wide temperature range (-50°C to 100°C)**  

**Embedded Applications**  
  - Develop **compact and high-performance** frequency analysis devices  

**Data Link**  
  - Build a **communication channel** between points worldwide via a **web platform**  

Legacy Software Support
=======================

- **GNU Radio, srsRAN, and many more through SoapySDR**  


uSDR Pinout Diagram
-------------------

.. image:: ../_static/hw_usdr_2.jpg
   :alt: uSDR Pinout Diagram

* RX(HF) - RF Input (for signal below 250 MHz)
* RX(UHF) - RF Input
* TX(UHF) - RF Output
