Using Raspberry Pi 5
====================

.. note::
   | To connect uSDR via MiniPCIe you have to use MiniPCIe hat and MiniPCIe to M.2 E Key Adapter.
   | Please refer to the :doc:`/hardware/minipcieadapter` document and `M2 HAT+ <https://www.raspberrypi.com/documentation/accessories/m2-hat-plus.html>`_.

.. note::
   | You don't need any additional configuration for the USB connection.

Prepare the system
^^^^^^^^^^^^^^^^^^

For MiniPCIe usage on Raspberry Pi, additional configuration is required.
You have to enable 32bit dma and enable PCIe x1 mode.

.. code-block:: sh

    echo "dtparam=pciex1" | sudo tee /boot/firmware/config.txt
    echo "dtoverlay=pcie-32bit-dma" | sudo tee /boot/firmware/config.txt
    sudo reboot

Installation
^^^^^^^^^^^^

.. note::
   | Please refer to the :doc:`/software/install` document.

Build from source
^^^^^^^^^^^^^^^^^

.. note::
   | Please refer to the :doc:`/software/compile` document.