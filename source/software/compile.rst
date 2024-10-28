=================
Build from source
=================

.. note::
   | For Raspberry Pi 5, please refer to the :doc:`/intro/raspberrypi5` document for additional configuration.

Clone the repository
--------------------

.. code-block:: sh

    git clone https://github.com/wavelet-lab/usdr-lib.git
    cd usdr-lib

Dependencies
------------

Ubuntu 18.04
^^^^^^^^^^^^

.. code-block:: sh

    sudo apt install build-essential dwarves -y
    sudo apt install libsoapysdr-dev libusb-1.0-0-dev check dkms curl -y

    # Install latest version of Cmake
    apt-get install libssl-dev -y
    curl https://cmake.org/files/v3.28/cmake-3.28.3.tar.gz -o cmake-3.28.3.tar.gz
    tar xvf cmake-3.28.3.tar.gz
    cd cmake-3.28.3
    ./bootstrap
    make
    make install
    update-alternatives --install /usr/bin/cmake cmake /usr/local/bin/cmake 10

    # Install Python 3.8
    apt-get install python3.8 python3.8-distutils -y
    update-alternatives --install /usr/bin/python3 python3 /usr/bin/python3.8 10
    curl https://bootstrap.pypa.io/get-pip.py | python3.8
    python3.8 -m pip install pyyaml

Ubuntu 20.04, 22.04, 24.04, Debian 12
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

.. code-block:: sh

    sudo apt install build-essential cmake python3 python3-venv python3-yaml dwarves -y
    sudo apt install libsoapysdr-dev libusb-1.0-0-dev check dkms -y

Build
-----

.. code-block:: sh

    mkdir build
    cd build
    cmake -DCMAKE_INSTALL_PREFIX:PATH=/usr ../src
    make

.. note::
   | If you want to install the library to ``/usr/local``, you can skip the ``-DCMAKE_INSTALL_PREFIX:PATH=/usr`` option.
   | In this case, you will need to set ``LD_LIBRARY_PATH=/usr/local/lib`` to run utilities.

Debug build
-----------

.. code-block:: sh

    mkdir build
    cd build
    cmake -DCMAKE_INSTALL_PREFIX:PATH=/usr -DCMAKE_BUILD_TYPE=Debug ../src
    make

Build and install the kernel module
-----------------------------------

.. code-block:: sh

    sudo apt install linux-headers-$(uname -r)
    cd ../src/lib/lowlevel/pcie_uram/driver/
    make
    # Sign the module
    sudo kmodsign sha512 /var/lib/shim-signed/mok/MOK.priv /var/lib/shim-signed/mok/MOK.der usdr_pcie_uram.ko
    sudo insmod usdr_pcie_uram.ko
    # Copy the udev rules
    sudo cp ./helpers/50-usdr-pcie-driver.rules /etc/udev/rules.d/
