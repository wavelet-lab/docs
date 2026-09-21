=====================================
Installing AFE79xx support for dSDR
=====================================

dSDR requires the proprietary ``libcapi79xx`` runtime plugin. dSDR will not
work unless this package is installed. The plugin is distributed separately
from ``usdr-lib``.

System requirements
===================

Prebuilt packages are available for the following Ubuntu releases:

* Ubuntu 20.04 Focal
* Ubuntu 22.04 Jammy
* Ubuntu 24.04 Noble
* Ubuntu 26.04 Resolute

Both AMD64 and ARM64 architectures are supported.

Determine the Ubuntu release codename:

.. code-block:: sh

    lsb_release --codename --short

If ``lsb_release`` is not installed, read the codename from
``/etc/os-release`` instead:

.. code-block:: sh

    . /etc/os-release
    echo "$VERSION_CODENAME"

Determine the package architecture:

.. code-block:: sh

    dpkg --print-architecture

The command should report either ``amd64`` or ``arm64``.

Add the uSDR repository
=======================

``libcapi79xx`` depends on ``usdr-lib``. Add the Wavelet Lab PPA before
installing ``libcapi79xx``:

.. code-block:: sh

    sudo add-apt-repository ppa:wavelet-lab/usdr-lib
    sudo apt update

Download ``libcapi79xx``
========================

Download the package matching the Ubuntu release and system architecture from
the `libcapi79xx 1.0.0 release
<https://github.com/wavelet-lab/usdr-releases/releases/tag/v1.0.0>`_.

Access to the release repository may require signing in to an authorized
GitHub account.

For example, a system running Ubuntu 26.04 on AMD64 requires:

.. code-block:: text

    libcapi79xx_1.0.0~resolute0_amd64.deb

Download the corresponding ``.deb.sha256`` file as well.

Verify the package
==================

Place the package and its checksum file in the same directory, then run:

.. code-block:: sh

    sha256sum --check libcapi79xx_1.0.0~resolute0_amd64.deb.sha256

Replace the file name with the package selected for the target system. A
successful verification produces output similar to:

.. code-block:: text

    libcapi79xx_1.0.0~resolute0_amd64.deb: OK

Do not install the package if checksum verification fails.

Install the package
===================

Open a terminal in the directory containing the downloaded package and install
it using APT:

.. code-block:: sh

    sudo apt install ./libcapi79xx_1.0.0~resolute0_amd64.deb

Replace the file name with the package appropriate for the target system.
Using APT instead of ``dpkg -i`` allows required dependencies to be installed
automatically.

Verify the installation
=======================

Verify that the package is installed:

.. code-block:: sh

    dpkg-query --show libcapi79xx

List the files installed by the package:

.. code-block:: sh

    dpkg -L libcapi79xx

After successful installation, restart the application that uses dSDR.

Environment variables
=====================

``usdr-lib`` automatically uses the runtime library and reference configuration
files installed by the ``libcapi79xx`` package. Environment variables are not
normally required.

Custom locations can still be specified when necessary:

.. code-block:: sh

    export AFECAPI=/custom/path/libcapi79xx.so
    export AFECFG_PATH=/custom/path/refs

``AFECAPI`` overrides the path to the runtime library. ``AFECFG_PATH``
overrides the directory containing the AFE79xx reference configuration files.

Unset these variables to restore the package defaults:

.. code-block:: sh

    unset AFECAPI
    unset AFECFG_PATH

Troubleshooting
===============

If ``usdr-lib`` cannot find the runtime plugin, first confirm that the package
is installed:

.. code-block:: sh

    dpkg-query --show libcapi79xx
    dpkg -L libcapi79xx

Check whether custom environment variables are overriding the installed
locations:

.. code-block:: sh

    printenv AFECAPI
    printenv AFECFG_PATH

If either variable points to an old build directory, unset it and restart the
application:

.. code-block:: sh

    unset AFECAPI
    unset AFECFG_PATH

Remove the package
==================

To remove ``libcapi79xx``:

.. code-block:: sh

    sudo apt remove libcapi79xx

Licensing
=========

``libcapi79xx`` is proprietary and confidential Wavelet Lab software.

Unauthorized copying, modification, distribution, sublicensing, or use is
prohibited without prior written permission from Wavelet Lab.
