=================
Build from source
=================

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
    sudo apt install libusb-1.0-0-dev check dkms curl -y

    # Install fresh version of Cmake
    apt-get install libssl-dev -y
    curl https://cmake.org/files/v3.28/cmake-3.28.3.tar.gz -o cmake-3.28.3.tar.gz
    tar xvf cmake-3.28.3.tar.gz
    cd cmake-3.28.3
    ./bootstrap
    make
    make install
    update-alternatives --install /usr/bin/cmake cmake /usr/local/bin/cmake 10

    # Install Python3.8
    apt-get install python3.8 python3.8-distutils -y
    update-alternatives --install /usr/bin/python3 python3 /usr/bin/python3.8 10
    curl https://bootstrap.pypa.io/get-pip.py | python3.8
    python3.8 -m pip install pyyaml

Ubuntu 20.04, 22.04, 24.04, Debian 12
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

.. code-block:: sh

    sudo apt install build-essential cmake python3 python3-venv python3-yaml dwarves -y
    sudo apt install libusb-1.0-0-dev check dkms -y

Build
-----

.. code-block:: sh

    mkdir build
    cd build
    cmake ../src
    make

Build kernel module
-------------------

.. code-block:: sh

    sudo apt install linux-headers-$(uname -r)
    cd ../src/lib/lowlevel/pcie_uram/driver
    make
    sudo insmod usdr_pcie_uram.ko
