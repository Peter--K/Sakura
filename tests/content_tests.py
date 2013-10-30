import unittest
import nose
from nose.tools import eq_, ok_
import os, sys

PATH_HERE = os.path.abspath(os.path.dirname(__file__))
sys.path = [os.path.join(PATH_HERE, '..')] + sys.path

import readMDA
from xmap_netcdf_reader import DetectorData

TESTDATA_DIR = os.path.join(PATH_HERE, '..', '..', 'test_data', '2013-07-26_mapping_mode')
MDA_FILE = 'SR12ID01H22707.mda'
NETCDF_DIR = os.path.join(TESTDATA_DIR, 'out_1374804236')
NETCDF_PATTERN = 'ioc5[3-4]_([0-9]*)\.nc'

''' The structure of test_data.xml is specifically built to test functionality of the
code. Changes to test_data.xml will cause failures in these tests.
'''

class DetectorTest(unittest.TestCase):
    def setUp(self):
        self.d = DetectorData(
            shape = (10,10),
            pixelsteps_per_buffer = 1,
            buffers_per_file = 1,
            dirpaths = NETCDF_DIR,
            filepattern = NETCDF_PATTERN,
            mca_bins = 2048,
            first_file_n = 1,
        )

    def get_spectrum_first_test(self):
        pixel_step, row, col = (0, 0, 0)
        spectrum = self.d.spectrum(pixel_step, row, col)
        self.assertEqual(len(spectrum), 2048)
        self.assertEqual(spectrum.sum(), 5445)

    def get_spectrum_last_test(self):
        pixel_step, row, col = (538, 9, 9)
        spectrum = self.d.spectrum(pixel_step, row, col)
        self.assertEqual(len(spectrum), 2048)
        self.assertEqual(spectrum.sum(), 155276)

    def get_statistic_first_test(self):
        pixel_step, row, col = (0, 0, 0)
        stat = self.d.statistic(pixel_step, row, col, 'realtime')
        self.assertEqual(stat, 3125023)

if __name__ == '__main__':
    nose.run(defaultTest=__name__)
