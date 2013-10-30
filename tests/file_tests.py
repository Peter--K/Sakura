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

class DatasetLoadingTest(unittest.TestCase):
    def simple_load_test(self):
        fname = os.path.join(TESTDATA_DIR, MDA_FILE)
        mda = readMDA.readMDA(fname, verbose=False)
        self.assertEqual(mda[0]['rank'], 1)


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

    def get_all_file_groups_test(self):
        fg_dict = self.d._get_all_file_groups()
        self.assertTrue(not fg_dict[0])         # 0: entry doesn't exist
        self.assertEqual(len(fg_dict[1]), 2)    # 1: group has two paths

    def get_all_file_groups_len_test(self):
        fg_dict = self.d._get_all_file_groups()
        self.assertEqual(len(fg_dict), 539)     # 539 netCDF pairs

    def get_step0_file_paths_test(self):
        paths = self.d._get_file_paths_for_pixel_step(pixel_step=0)
        self.assertEqual(len(paths), 2)
        paths = self.d._get_file_paths_for_pixel_step(pixel_step=538)
        self.assertEqual(len(paths), 2)
        paths = self.d._get_file_paths_for_pixel_step(pixel_step=539)
        self.assertEqual(len(paths), 0)

    def get_file_paths_for_all_pixel_steps_test(self):
        fg_dict = self.d._get_file_paths_for_all_pixel_steps()
        self.assertEqual(len(fg_dict), 539)
        self.assertEqual(len(fg_dict[1]), 2)

    def build_reverse_file_lookup_test(self):
        fg_dict = self.d._get_file_paths_for_all_pixel_steps()
        d = self.d._build_reverse_file_lookup(fg_dict)
        self.assertEqual(d['ioc53_1.nc'], [0])
        self.assertEqual(d['ioc54_1.nc'], [0])
        self.assertEqual(d['ioc53_539.nc'], [538])
        self.assertEqual(d['ioc54_539.nc'], [538])

    def reverse_file_lookup_test(self):
        files = self.d._get_file_paths_for_all_pixel_steps()
        reverse_dict = self.d._build_reverse_file_lookup(files)
        self.assertEqual(len(reverse_dict), 539*2)
        self.assertEqual(reverse_dict['ioc53_1.nc'][0], 0)
        self.assertEqual(reverse_dict['ioc54_1.nc'][0], 0)
        self.assertEqual(reverse_dict['ioc53_539.nc'][0], 538)

    def get_data_location_test(self):
        tests = [
            [(0, 0, 0), (0,  0, 0)],
            [(0, 5, 1), (0, 12, 3)],
            [(0, 5, 2), (0,  0, 0)],
            [(0, 9, 9), (0, 11, 3)],
        ]
        for input, output in tests:
            pixel_step, row, col = input
            path, buffer_ix, module_ix, channel = self.d._get_data_location(pixel_step, row, col)
            self.assertTrue(isinstance(path, basestring))
            self.assertEqual((buffer_ix, module_ix, channel), output)

    def enumerate_all_data_indices_in_file_test(self):
        tests = [
            # filename, no. of elements in file,
            # first and last (pixel_step, row, col, channel, buffer_ix, module_ix)
            ['ioc53_1.nc',   52, (  0, 0, 0, 0, 0, 0), (  0, 5, 1, 3, 0, 12)],
            ['ioc54_1.nc',   48, (  0, 5, 2, 0, 0, 0), (  0, 9, 9, 3, 0, 11)],
            ['ioc53_539.nc', 52, (538, 0, 0, 0, 0, 0), (538, 5, 1, 3, 0, 12)],
        ]
        for filename, el, first, last in tests:
            d = self.d._enumerate_all_data_indices_in_file(filename)
            self.assertEqual(len(d), el)
            self.assertEqual(d[0], first)
            self.assertEqual(d[-1], last)

if __name__ == '__main__':
    nose.run(defaultTest=__name__)
