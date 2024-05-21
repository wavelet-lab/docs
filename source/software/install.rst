=====================
Software installation
=====================

Ubuntu 20.04, 22.04, 24.04
--------------------------

Add the repository
^^^^^^^^^^^^^^^^^^

.. code-block:: sh

    sudo add-apt-repository ppa:wavelet-lab/usdr-lib
    sudo apt update


Install the tools
^^^^^^^^^^^^^^^^^

.. code-block:: sh

    sudo apt install usdr-tools

SoapySDR plugin
^^^^^^^^^^^^^^^

.. code-block:: sh

    sudo apt install soapysdr-module-usdr

PCIe driver
^^^^^^^^^^^

.. code-block:: sh

    sudo apt install usdr-dkms
    sudo modprobe usdr_pcie_uram

Install the development package
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

.. code-block:: sh

    sudo apt install libusdr-dev

Ubuntu 18.04, Debian 12
-----------------------

Download
^^^^^^^^

Go to `releases page <https://github.com/wavelet-lab/usdr-lib/releases>`_ and download the corresponding archive.

* Ubuntu 18.04: ``usdr_X.Y.Z~bionic1.tar``
* Debian 12: ``usdr_X.Y.Z~bookworm1.tar``

Unpack
^^^^^^

Ubuntu 18.04
""""""""""""

.. code-block:: sh

    tar xf usdr_X.Y.Z~bionic1.tar

Debian 12
"""""""""

.. code-block:: sh

    tar xf usdr_X.Y.Z~bookworm1.tar

Install package
^^^^^^^^^^^^^^^

.. code-block:: sh

    sudo apt install libusb-1.0-0 libsoapysdr0.8 dkms
    sudo dpkg -i *.deb
