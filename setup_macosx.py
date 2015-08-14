import ez_setup
ez_setup.use_setuptools()

from setuptools import setup

import glob
import os

exec(open('version.py').read())

includes = ['netCDF4', 'numpy', 'scipy', 'wx']

packages = []

excludes = ['email', 'Finder', 'jinja2', 'nose', 'xml']

data_files = glob.glob('./*.ini')
data_folders = [('resources', 'resources')]

# Parsing folders and building the data_files table
for folder, relative_path in data_folders:
    for file in os.listdir(folder):
        f1 = os.path.join(folder,file)
        if os.path.isfile(f1):          # skip directories
            f2 = relative_path, [f1]
            data_files.append(f2)

# resources = [('', ['gist_heat.cmap'])]

setup(
    name='Sakura',
    app=['sakura.py'],
    setup_requires=['py2app'],
    author = 'Peter Kappen, Gary Ruben',
    author_email='sakura@synchrotron.org.au',
    version = __version__,
    description = 'Sakura',
    options = {'py2app' : {
#        'resources': resources,
        'iconfile': 'resources/app_ico.icns',
        'optimize': 2,
        'packages': packages,
        'includes': includes,
        'excludes': excludes,
        'dist_dir': 'dist',
        'xref': False,
        'compressed' : True,
        'argv_emulation': False,
    },},
    data_files=data_files)
