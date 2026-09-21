========================
Software troubleshooting
========================

``usdr-dkms``
=============

Package installation fails
--------------------------

Update the package index and make sure that the kernel headers for the running
kernel are installed:

.. code-block:: sh

    sudo apt update
    sudo apt install linux-headers-$(uname -r)
    sudo apt install --reinstall usdr-dkms

Check the DKMS build status:

.. code-block:: sh

    dkms status

DKMS build fails after an Ubuntu upgrade
-----------------------------------------

After upgrading Ubuntu, old kernels and their header packages may remain
installed. When installing or upgrading ``usdr-dkms``, DKMS attempts to build
the module for every detected kernel.

This may result in an error similar to the following:

.. code-block:: text

    Building initial module usdr-dkms/1.0.0~resolute0 for 6.17.0-23-generic
    /bin/sh: 1: gcc-13: not found
    Error! Bad return status for module build on kernel: 6.17.0-23-generic

In this example, the old kernel was built with GCC 13, which is no longer
installed on the upgraded system.

Check the running kernel
^^^^^^^^^^^^^^^^^^^^^^^^

Before removing an old kernel, verify that the system is running a newer one:

.. code-block:: sh

    uname -r

.. warning::

   Do not remove the kernel that is currently running. Removing an active
   kernel may leave the system unable to boot.

Find remaining old kernel packages
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Set ``OLD_KERNEL`` to the kernel release reported in the build error. The value
below corresponds to the preceding example; replace it with the release shown
on your system. ``OLD_KERNEL_ABI`` is the release without the flavor suffix:

.. code-block:: sh

    OLD_KERNEL=6.17.0-23-generic
    OLD_KERNEL_ABI=6.17.0-23
    dpkg -l "*$OLD_KERNEL_ABI*"

Also check whether the corresponding module and header directories remain:

.. code-block:: sh

    ls -ld "/lib/modules/$OLD_KERNEL"
    ls -ld "/lib/modules/$OLD_KERNEL/build"

Remove the old kernel
^^^^^^^^^^^^^^^^^^^^^

Remove only the old kernel packages reported by the previous command. A
typical command looks like this:

.. code-block:: sh

    sudo apt purge \
      "linux-headers-$OLD_KERNEL_ABI" \
      "linux-headers-$OLD_KERNEL" \
      "linux-image-$OLD_KERNEL" \
      "linux-modules-$OLD_KERNEL" \
      "linux-modules-extra-$OLD_KERNEL"

The exact package list may differ. Include only packages that are actually
installed on the system.

Clean up the DKMS state
^^^^^^^^^^^^^^^^^^^^^^^

Use ``dkms status`` to find the installed ``usdr-dkms`` version, assign it to
``DKMS_VERSION``, and remove the module build state associated with the old
kernel. Replace the example version below with the version shown on your
system:

.. code-block:: sh

    DKMS_VERSION=1.0.0~resolute0
    sudo dkms remove "usdr-dkms/$DKMS_VERSION" -k "$OLD_KERNEL"

If the corresponding entry has already been removed from the DKMS tree, the
command may report that the module was not found. No additional action is
required in that case.

Complete package configuration
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

After removing the old kernel, complete the interrupted package configuration:

.. code-block:: sh

    sudo apt --fix-broken install

Check the DKMS module status:

.. code-block:: sh

    dkms status

The module should have the ``installed`` status for each current kernel, for
example:

.. code-block:: text

    usdr-dkms/1.0.0~resolute0, 7.0.0-30-generic, x86_64: installed
    usdr-dkms/1.0.0~resolute0, 7.0.0-31-generic, x86_64: installed

Inspect build failures
^^^^^^^^^^^^^^^^^^^^^^

If the module also fails to build for a current kernel, inspect the DKMS build
log. Use the ``DKMS_VERSION`` value reported by ``dkms status``:

.. code-block:: sh

    sudo cat "/var/lib/dkms/usdr-dkms/$DKMS_VERSION/build/make.log"

A message stating that the kernel headers are unsupported is usually only a
generic DKMS failure message. Locate the first compiler message containing
``error`` or ``fatal error`` to determine the actual cause.

Kernel module does not load
---------------------------

If the package is installed and DKMS reports a successful build, try to load
the module manually:

.. code-block:: sh

    sudo modprobe usdr_pcie_uram

Then verify that the module is active:

.. code-block:: sh

    lsmod | grep usdr_pcie_uram

If ``modprobe`` reports an error or the module is not listed, inspect the
kernel log for more details:

.. code-block:: sh

    sudo dmesg | grep -i usdr

Secure Boot prevents module loading
-----------------------------------

Secure Boot is a common reason why a successfully built DKMS module cannot be
loaded: the kernel may reject a module that is not signed with an enrolled key.
Check the Secure Boot state and look for signature or verification errors in
the kernel log:

.. code-block:: sh

    mokutil --sb-state
    sudo dmesg | grep -i -E 'secure boot|verification|signature|usdr'
    modinfo -F signer usdr_pcie_uram

If Secure Boot is enabled and ``modinfo`` does not report a signer, the
installed module is unsigned. If it reports a signer that is not trusted, the
corresponding Machine Owner Key (MOK) has not been enrolled. Sign the module
with a key enrolled on the system, or contact Wavelet Lab support for help with
the packaged DKMS module. The signing procedure in :doc:`/software/compile`
applies to a module built manually from source and may not use the same key as
the ``usdr-dkms`` package.
