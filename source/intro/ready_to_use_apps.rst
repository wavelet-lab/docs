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
