# This file based on the example by Thomas Lecocq at
# http://www.geophysique.be/2011/08/01/pack-an-enthought-traits-app-inside-a-exe-using-py2exe-ets-4-0-edit/
# retrieved 2013-04-05
# Quoting the blog entry:
#
# then, to launch the packing, just do:
# $ python setup.py py2exe
#
# The build and packing process takes some time, but it works. The /dist directory contains a lot of
# libraries (~73 MB), there must be a way to cut down the imports, but I have to admit, now that I
# have a successful build, I really don't care if it's 110 MB or 80 MB ! I left the lines to include
# the matplotlib data files, although they are not needed for this example.
#
# To launch the script, just hit "example.exe" in the /dist folder. Note, I set the "console" value
# to "example.py", because I wanted to have a python console running behind my GUI. If you replace
# "console" by "windows", double-clicking "example.exe" will just load your GUI.
#
# Note, tested with Christoph Gohlke's version of py2exe 0.6.10dev

from distutils.core import setup
import py2exe
import os
import glob
import sys

#~ DLL_PATH = os.path.join(sys.exec_prefix, 'lib', 'site-packages', 'numpy', 'core')
#~ sys.path.append(DLL_PATH)

exec(open('version.py').read())

includes = []
includes.append('numpy')
includes.append('numpy.core')
includes.append('scipy')
includes.append('logging')
includes.append('wx')
includes.append('wx.*')

excludes = ['_ssl', 'ipython', 'tcl',
            'PIL._imagingtk', 'PIL.ImageTk',
            'qt', 'PyQt4Gui', 'Carbon', 'email', 'PySide',
           ]

packages = ['scipy.io']

data_files = []
data_folders = [('resources', 'resources')]

# Parsing folders and building the data_files table
for folder, relative_path in data_folders:
    for file in os.listdir(folder):
        f1 = os.path.join(folder,file)
        if os.path.isfile(f1):          # skip directories
            f2 = relative_path, [f1]
            data_files.append(f2)

# data_files.append(('.', ['gist_heat.cmap']))

setup(\
    #windows = ['Sakura.py'],
    console = ['Sakura.py'],
    author = "Peter Kappen, Gary Ruben",
    author_email='sakura@synchrotron.org.au',
    version = __version__,
    description = "Sakura",
    name = "Sakura",
    options = {"py2exe": {
        "optimize": 0,
        "packages": packages,
        "includes": includes,
        "excludes": excludes,
        "dll_excludes": ["MSVCP90.dll", "w9xpopen.exe"],
        "dist_dir": 'dist',
        #"bundle_files":2,
        "xref": False,
        "skip_archive": True,
        "ascii": False,
        "custom_boot_script": '',
        "compressed":False,
        },
    },
    data_files=data_files)
