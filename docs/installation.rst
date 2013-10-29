.. _installation_root:

***************
Installation
***************

For MS Windows users, a standalone installer is available from the `main site <http://www.synchrotron.org.au/sakura>`_. Download and install this to run Sakura.

Linux and Mac users or Windows users wishing to install from source must install `Python 2.7.x<http://python.org>`_ and the packages listed below.
Sakura is written in `Python <http://python.org>`_ (2.7 at the time of writing). The easiest way to satisfy the Python module dependencies is to install one of the `Enthought Canopy Distributions <http://www.enthought.com/products/epd.php>`_. The older Enthought EPDFree distribution (also available from the `main site <http://www.synchrotron.org.au/sakura>`_) also contains all the modules on which Sakura depends. A typical user can just install one of these, then download and unpack the Sakura source code and run the sakura.py file.

Some users might prefer alternatives to EPDFree or Canopy. Other popular Python distributions are `Python(x,y) <http://code.google.com/p/pythonxy/>`_ and ActiveState's `ActivePython <http://www.activestate.com/activepython/downloads>`_, both of which will require installation of at least some of the following dependencies:

.. _python_package_dependencies:

Python package dependencies
---------------------------------

Sakura depends on the following Python modules being installed in the Python environment

* `Python 2.7.x <http://python.org/>`_
* `numpy <http://numpy.scipy.org/>`_
* `scipy <http://numpy.scipy.org/>`_
* `wxPython 2.8 <http://wxpython.org/>`_

Those wishing to build the documentation from source will also need `Sphinx <http://sphinx.pocoo.org/>`_.
For those familiar with installing Python packages, the dependencies can be found in the `central repository of Python modules <http://pypi.python.org/pypi>`_. For Microsoft Windows users, Christoph Gohlke (C.G.) maintains a useful `repository of Windows installers <http://www.lfd.uci.edu/~gohlke/pythonlibs/>`_ containing the required packages. Linux users can typically find the dependencies using their package manager (e.g. synaptic or yum). Mac users should visit the individual sites linked above for instructions. In all cases, be careful to choose the package versions complied for Python 2.7.x and choose either the 32bit or 64bit package versions to match the version of Python you installed.

.. _example1:

Example 1. Windows installation using Enthought EPDFree (recommended)
---------------------------------------------------------------------

#. Visit the `Sakura download page <http://www.synchrotron.org.au/sakura>`_ and follow the instructions to obtain the EPDFree Python installer and the Sakura file archive. You may wish to visit the `Enthought website <http://www.enthought.com>`_, directly, and choose one of Enthought's Canopy Python distributions. However, these include wxPython 2.9, which may cause incompatibility problems with Sakura.
#. Run the epd_free-\*.msi installer to install EPD Free (or install using the Canopy installer).
#. Verify that Python is running correctly.
   e.g. for Windows 7, click on ``Start Menu|All Programs|Accessories|Command Prompt``.
   At the ``>`` prompt type ``python -c "print 'hello world'"`` noting single and double quotes.
   Verify that ``hello world`` is displayed.
#. Download the Sakura source code bundle and uncompress it.
#. Double-click sakura.py to run Sakura.

Example 2. Windows installation using Python(x,y) (optional)
------------------------------------------------------------

#. Visit the `Python(x,y) <http://code.google.com/p/pythonxy/>`_ `downloads page <http://code.google.com/p/pythonxy/wiki/Downloads>`_ and install a distribution.
#. Verify that Python is running correctly (see :ref:`example1`).
#. Visit the `Sakura download page <http://www.synchrotron.org.au/Sakura>`_ and follow the instructions to obtain the Sakura setup file.
#. Download the Sakura source code bundle and uncompress it.
#. Double-click sakura.py to run Sakura.

Example 3. Linux installation using Enthought Python Distribution (recommended)
-------------------------------------------------------------------------------

#. Visit the `Sakura download page <http://www.synchrotron.org.au/sakura>`_ and follow the instructions to obtain the EPD Free Python installer and the Sakura .zip package for Linux. You may wish to visit the `Enthought website <http://www.enthought.com/products/epd.php>`_, directly, and choose one of Enthought's other Python distributions. Note, `EPD Free <http://www.enthought.com/products/epd_free.php>`_ satisfies the dependencies listed above.
#. Run the epd_free-\*.sh shell script to install EPD Free.
#. Verify that Python is running correctly.
   e.g. for Ubuntu, open a terminal.
   At the ``$`` prompt type ``python -c "print 'hello world'"`` noting single and double quotes.
   Verify that ``hello world`` is displayed.
#. The main Sakura application file is ``sakura.py`` in the directory into which Sakura was unpacked.
#. Start Sakura by running ``python ./sakura.py``.

Example 4. Linux installation using synaptic (experienced)
----------------------------------------------------------

Note: untested.

This description is for Ubuntu Linux. yum packaged names in Fedora Linux flavours should have similar names.

#. First, verify that Python2.7 is running correctly.
   e.g. for Ubuntu, open a terminal.
   At the ``$`` prompt type ``python -c "import sys; print sys.version"``.
   Verify that a string displays identifying a 2.7 branch version of Python.
#. Using synaptic or ``apt-get install <package>`` install the following packages: ``python-numpy``, ``python-scipy``, ``python-wxgtk2.8``
#. Visit the `Sakura download page <http://www.synchrotron.org.au/sakura>`_ and follow the instructions to obtain the package.
#. The main application file is ``sakura.py`` in the directory into which Sakura was unpacked.
#. Start Sakura by running ``python ./sakura.py``.

Example 5. Mac OSX installation (recommended)
---------------------------------------------

Note: untested.

#. Visit the `Sakura download page <http://www.synchrotron.org.au/sakura>`_ and follow the instructions to obtain the EPD Free Python installer and the Sakura .zip package for Mac OSX. You may wish to visit the `Enthought website <http://www.enthought.com/products/epd.php>`_, directly, and choose one of Enthought's other Python distributions. Note, `EPD Free <http://www.enthought.com/products/epd_free.php>`_ satisfies the dependencies listed above.
#. Run the epd_free-\*.dmg installer to install EPD Free.
#. Move the .zip package to the Applications folder.
#. Double click the Application .zip package to unpack it the first time.
#. At a command prompt, start Sakura by running ``python ./sakura.py``.
