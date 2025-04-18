Ready-to-use Applications
=========================

FM Receiver
-----------

**Overview**

The FM Receiver application on WSDR.io allows users to tune into FM radio stations, demodulate signals, and visualize frequency spectrums in real-time.

**Key Features:**

- Real-time FM signal reception & demodulation  
- Wide/Narrow FM band selection  
- Adjustable tuning frequency, gain, and sample rate  
- Customizable FFT settings & visualization parameters  
- Waterfall and spectrum display for signal analysis  

**Getting Started**

**Step 1: Open the FM Receiver App**

- Navigate to WSDR.io  
- Click on **Applications**  
- Select **FM Receiver** from the list  
- Click **+** to launch the application  

**Step 2: Select the Signal Source**

- Click the **Source** dropdown  
- Select one of the following:  
  - USB Device (uSDR)  
  - File  
  - Stream  
  - Storage  

**Step 3: Configure Radio Settings**

1. **Set the Frequency**  
   - Adjust "Frequency" (e.g., 95.4 MHz)  
   - Fine-tune with "Tune Frequency" in kHz  

2. **Adjust Bandwidth**  
   - Default 500 kHz  
   - Larger bandwidth = more data, more processing  

3. **Configure Gain**  
   - Use Gain Slider (0 - 24 dB)  

4. **Set the Sample Rate**  
   - Choose (e.g., 1 MHz)  

5. **Select FM Demodulation Mode**  
   - Choose WBFM or NBFM  

**Step 4: Adjust Audio Settings**

- Use the Volume Slider  
- Ensure system audio output is configured correctly  

**Step 5: Customize the Visual Display**

1. **Waterfall Spectrum Display (Left Panel)**  
   - Displays frequency spectrum over time  
   - Color intensity = signal strength  

2. **Power Spectral Density (Top Right Panel)**  
   - Shows instantaneous signal power  

3. **Demodulated FM Spectrum (Bottom Right Panel)**  
   - Displays demodulated FM  
   - FFT configurable  

**Step 6: Configure Advanced Parameters**

1. **Adjust FPS (Frame Rate per Second)**  
   - Default: 20 FPS  

2. **Set Alpha Blending**  
   - Default: 0.1  

3. **Configure FFT & Windowing**  
   - FFT Size: 1024, 2048, 4096  
   - Window Types: Blackman-Harris, Hanning, Hamming  

**Step 7: Start Receiving & Listening**

- Click **Play**  
- Scroll to fine-tune frequency  
- View changes in real-time visualization  

Cellular Network
----------------

**Overview**

The WSDR Cellular Network application enables deployment and management of a **2G GSM cellular network** based on the Osmocom stack. This cloud-based setup is ideal for experimentation, research, and development.

**Getting Started**

1. **Interface Overview**

- **Device Selection**: uSDR via USB Adapter or Dev Board  
- **Configuration Dropdown**: Select BTS config  
- **Osmo-BTS Log**: Real-time BTS status  
- **Network Status Bar**:  
  - TX / RX frequencies  
  - Connection instructions for mobile  

2. **BTS Configuration**

- Select from predefined BTS configurations  
- ⚠️ Note: Current version supports a limited set  
- Each config includes:  
  - Band (e.g., GSM900, DCS1800)  
  - ARFCN  
  - Tx/Rx Frequency pair  

3. **Registering to the Network**

- **Plug in uSDR**  
  - Use USB adapter or USB-C dev board  

- **Select the Device**  
  - Choose from dropdown in the app  

- **Start the BTS**  
  - Click **Play** to initialize  
  - ⚠️ Stopping BTS requires power cycle to restart  

- **Insert an Unlocked SIM Card**  
  - Carrier-locked SIMs won’t work  

**On Your Android Device:**

- Go to:  
  Settings → Connections → Mobile networks → Network operators → Scan networks  
- Select network named **901-70**  
- Dial *#100# to confirm registration

Signal Analyzer
----------------

The Signal Analyzer application in WSDR.io allows users to analyze digital and analog signals, supporting multiple modulation types and advanced visualization features. It can process both live signals and pre-recorded files.

1. Features

WSDR currently supports FM, GMSK, and FSK modulation, with ongoing development for additional modulations.

**Multiple Signal Views:**

- **IQ View** – In-phase & Quadrature representation  
- **Analog View** – Time-domain signal visualization  
- **Power View** – Signal strength over time  
- **Demodulated View** – Extracted baseband signal  

**Current Decoding Options:**

- **BTLE** (Bluetooth Low Energy)  
- **NRF** (Nordic Semiconductor RF protocol)  

**Recording & File Loading:**

- Record a live signal directly from SDR  
- Load a pre-recorded file from a PC or Cloud Storage  

2. Getting Started

.. image:: ../_static/wsdr/signal_anlz.jpg

**A. Opening a Signal Source**

- Go to **Applications** and select **Signal Analyzer**  
- Choose a signal source:  
  - **Live Signal** – Direct from SDR device  
  - **Pre-Recorded File** – Load from PC or Cloud Storage  

**B. Configuring Signal Parameters**

- Set the Rate (e.g., 100 kHz)  
- Select Modulation Type (FM, GMSK, or FSK)  
- Adjust Signal Processing Options:  
  - **Samples/Symbol** – Defines signal resolution  
  - **Modulation Index** – Adjusts signal characteristics  
  - **Threshold & Error Settings** – Useful for decoding  

Choose the Signal View:

- IQ View  
- Analog View  
- Power View  
- Demodulated View  

**C. Decoding and Analyzing the Signal**

- Enable **Vector Diagram** to visualize the constellation  
- Select **Data Format**: Bits or Symbols  
- Choose Decoder:  
  - BTLE  
  - NRF  
- Specify the Channel (e.g., 37 for Bluetooth)  
- View the decoded bits in the bottom section  

**D. Recording and Saving Data**

- Click **Record Signal** to start recording live data  
- To load a file, select from PC or Cloud Storage  
- Store analyzed signals in Cloud Storage for later use 



3. Additional Notes

- Ensure the correct modulation type is selected for accurate decoding  
- The vector diagram helps visualize signal integrity  
- Cloud Storage Integration allows seamless access across WSDR.io applications  

