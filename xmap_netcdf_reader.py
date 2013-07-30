#!/usr/bin/env python

# Copyright (c) 2013 Synchrotron Light Source Australia Pty Ltd.
# Released under the Modified BSD license
# See LICENSE

import numpy as np
import os
import re
from utils import memoize

# This module supports three netCDF file readers; scipy.io.netcdf_file,
# pupynere.netcdf_file and netCDF4.Dataset and prefers them in that order.
# scipy.io.netcdf_file is based on pupynere.netcdf_file and is more likely to
# be installed. scipy.io.netcdf_file and pupynere.netcdf_file are both much
# faster than netCDF4 and are pure-Python modules, so they are preferred here.
# Note that the data endianness is treated differently by netCDF4.
NETCDF_READER = None
uint16 = '>u2'
uint32 = '>u4'
try:
    from scipy.io import netcdf_file
    NETCDF_READER = 'scipy'
except:
    try:
        from pupynere import netcdf_file
        NETCDF_READER = 'pupynere'
    except:
        print 'no netCDF reader found'
#print NETCDF_READER


CHANNELS_PER_MODULE = 4


# Buffer header defn see DXP-XMAP/xManager User Manual section 5.3.3.2
buffer_header_dtype = ([
    ('tag0'           , uint16 ),  # 0x55AA
    ('tag1'           , uint16 ),  # 0xAA55
    ('header_size'    , uint16 ),  # Buffer header size=256
    ('mapping_mode'   , uint16 ),  # Mapping mode (1=Full spectrum, 2=Multiple ROI, 3=List mode)
    ('run_number'     , uint16 ),
    ('buffer_number'  , uint32 ),  # Sequential buffer number, low word first
    ('buffer_id'      , uint16 ),  # 0=A, 1=B
    ('num_pixels'     , uint16 ),  # Number of pixels in buffer
    ('starting_pixel' , uint32 ),  # Starting pixel number, low word first
    ('module_number'  , uint16 ),
    ('channel_id'     , uint16, (4,2) ),
    ('channel_size'   , uint16, 4 ),   # Channel sizes: channel 0..3
    ('buffer_errors'  , uint16 ),
    ('reserved1'      , uint16, 31-25+1 ),
    ('user_defined'   , uint16, 63-32+1 ),
    ('reserved2'      , uint16, 255-64+1 ),
])


# Pixel header defn for mapping mode 1: Full Spectrum Mapping.
# Used by get_fixedbins_spectrum()
# See DXP-XMAP/xManager User Manual section 5.3.3.3
pixel_header_mode1_static_fixedbins_dtype = lambda mca_bins: ([
    ('tag0'             , uint16 ),  # 0x33CC
    ('tag1'             , uint16 ),  # 0xCC33
    ('header_size'      , uint16 ),  # Pixel header size=256
    ('mapping_mode'     , uint16 ),  # Mapping mode=1=Full spectrum
    ('pixel_number'     , uint32 ),
    ('total_pixel_block_size', uint32 ),
    ('ch0_size'         , uint16 ),  # K words
    ('ch1_size'         , uint16 ),  # L words
    ('ch2_size'         , uint16 ),  # M words
    ('ch3_size'         , uint16 ),  # N words

    ('reserved1'        , uint16, 31-12+1 ),

    # ch0 statistics
    ('ch0_realtime'     , uint32 ),
    ('ch0_livetime'     , uint32 ),
    ('ch0_triggers'     , uint32 ),
    ('ch0_output_events', uint32 ),

    # ch1 statistics
    ('ch1_realtime'     , uint32 ),
    ('ch1_livetime'     , uint32 ),
    ('ch1_triggers'     , uint32 ),
    ('ch1_output_events', uint32 ),

    # ch2 statistics
    ('ch2_realtime'     , uint32 ),
    ('ch2_livetime'     , uint32 ),
    ('ch2_triggers'     , uint32 ),
    ('ch2_output_events', uint32 ),

    # ch3 statistics
    ('ch3_realtime'     , uint32 ),
    ('ch3_livetime'     , uint32 ),
    ('ch3_triggers'     , uint32 ),
    ('ch3_output_events', uint32 ),

    ('reserved2'        , uint16, 255-64+1 ),

    # end of first 256 words

    ('ch0_spectrum'     , uint16, mca_bins ),
    ('ch1_spectrum'     , uint16, mca_bins ),
    ('ch2_spectrum'     , uint16, mca_bins ),
    ('ch3_spectrum'     , uint16, mca_bins ),
])


def show_header_content(header):
    """Show header content in human-readable form

    Keyword arguments:
    header - a header array view

    Example:
    >>> static_data = data[:12].view(pixel_header_static_dtype)
    >>> show_header_content(static_data)
    tag0: <type 'numpy.uint16'>: 13260
    tag1: <type 'numpy.uint16'>: 52275
    header_size: <type 'numpy.uint16'>: 256
    mapping_mode: <type 'numpy.uint16'>: 1
    pixel_number: <type 'numpy.uint32'>: 0
    total_pixel_block_size: <type 'numpy.uint32'>: 8448
    ch0_size: <type 'numpy.uint16'>: 2048
    ch1_size: <type 'numpy.uint16'>: 2048
    ch2_size: <type 'numpy.uint16'>: 2048
    ch3_size: <type 'numpy.uint16'>: 2048

    """
    for t in header.dtype.names:
        item = header[t][0]
        print "{}: {}: {}".format(t, type(item), item)


class DetectorData(object):
    """A container for accessing matching netCDF files corresponding to the XAS
    multi-element detector.
    """
    def __init__(self, shape, pixelsteps_per_buffer, buffers_per_file,
                 dirpaths, filepattern, mca_bins=2048, first_file_n=1):
        """Show header content in human-readable form

        Keyword arguments:
        shape - tuple (rows, cols) of detector shape rows and cols.
        pixelsteps_per_buffer - Mapping Pixels Per Buffer setting.
        buffers_per_file - no. of buffers per netCDF file.
        dirpaths - a filepath string or a list of filepath strings to the files.
        filepattern - a filename regex template whose capture group
                      is used to associate results across multiple files
                      e.g. ioc5[3-4]_([0-9]*)\.nc will group files such as
                      (ioc53_0.nc,ioc54_0.nc), (ioc53_11.nc,ioc54_11.nc).
                      Optionally, this can be a fixed string matching a single filename,
                      if only a single netCDF file is being accessed, e.g. 'ioc53_11.nc'
        mca_bins - no. of bins in MCA modules.
        first_file_n - e.g. 1 if first filename is ioc5[3-4]_1.nc

        """
        self.shape = shape
        self.rows, self.cols = shape
        self.mca_bins = mca_bins
        self.pixelsteps_per_buffer = pixelsteps_per_buffer
        self.buffers_per_file = buffers_per_file

        if isinstance(dirpaths, basestring):
            dirpaths = [dirpaths]
        self.dirpaths = dirpaths
        self.filepattern = filepattern
        self.first_file_n = first_file_n

    @staticmethod
    def _matching_n(files, pattern, n):
        """Return all netCDF filenames in the files list whose regex capture group
        matches the specified value of n.

        Keyword arguments:
        files - a list of filenames.
        pattern - a regex containing one capture group, used to match the number OR
                  a string used to directly match a filename in files.
        n - the number used to match the file.

        Returns:
        A list of filename strings.

        """
        if pattern in files:
            return [pattern]
        else:
            prog = re.compile(pattern)
            re_matches = [(prog.match(f), f) for f in files if prog.match(f)]
            filenames = [m[1] for m in re_matches if int(m[0].group(1)) == n]
            return filenames


    @memoize
    def _get_file_paths_for_pixel_step(self, pixel_step):
        """Get the paths to netCDF files on disk corresponding to a given
        pixel_step, sorted based on filename.
        Memoized to speed up multiple accesses to the same pixel.
        Raises an IndexError if files are not found.

        Keyword arguments:
        pixel_step - 0-based int.

        Returns:
        list of full paths to files for the specified pixel_step.

        """
        regex = self.filepattern
        file_n = self.first_file_n + pixel_step // self.buffers_per_file
        # make a list of tuples: (path, [list of matching files])
        filepaths = [(path, DetectorData._matching_n(os.listdir(path), regex,
                                                     file_n)) for path in self.dirpaths]
        # reassemble full paths to matching files but keep filename for sorting
        unsortedpaths = [(f, os.path.join(path, f))
                         for path, filenames in filepaths for f in filenames]
        if not unsortedpaths:
            raise IndexError
        # sort based on filename ignoring path
        sortedpaths = sorted(unsortedpaths, key=lambda x: x[0])
        # finally just keep the full paths, now sorted based on filename
        paths = [p[1] for p in sortedpaths]
        return paths

    @memoize
    def _get_data_location(self, pixel_step, row, col):
        """Locate the data buffer corresponding to the
        pixel_step, row and col.

        Keyword arguments:
        pixel_step - 0-based index to "pixel" step, i.e. mono position
        row, col - detector element row and column

        Returns:
        A 4-tuple (path, buffer_ix, module_ix, channel):
        path - netCDF file path
        buffer_ix - 0-based int referring to buffer contained in netCDF file.
        module_ix - 0 -> max_module-1 for the current file.
        channel - 0-3

        """
        # determine files to read
        filepaths = self._get_file_paths_for_pixel_step(pixel_step)

        # Get module index from element index
        module_ix, channel = divmod(row * self.rows + col, CHANNELS_PER_MODULE)

        # Now get the file and module index within that file by assuming the modules are
        # split evenly across the IOCs and are in increasing sequential order
        number_of_files = len(filepaths)
        number_of_detector_elements = self.rows * self.cols
        file_split_value = int(np.ceil(float(
            number_of_detector_elements / CHANNELS_PER_MODULE) / number_of_files))
        file_ix, module_ix = divmod(module_ix, file_split_value)

        # Get a netCDF file path
        path = filepaths[file_ix]

        # Get buffer index from module_ix and pixel_step
        buffer_ix = pixel_step % self.pixelsteps_per_buffer

        return path, buffer_ix, module_ix, channel

    def _get_buffer_header(self, f, buffer_ix, module_ix):
        """Return the buffer header of the buffer indexed by buffer_ix, module_ix

        Keyword arguments:
        f - netCDF file handle
        buffer_ix - 0-based int referring to buffer contained in netCDF file.
        module_ix - 0 -> max_module-1 for the current file.

        Returns:
        An ndarray view with dtype=buffer_header_dtype

        """
        array_data = f.variables['array_data']
        module_data = array_data[buffer_ix, module_ix, :]
        data = module_data[0: 256]      # read buffer header
        buffer_header = data.view(buffer_header_dtype)
        return buffer_header

    def _uint32_swap_words(self, item_array):
        """Deal with 32-bit uint32 items properly turning them into numpy np.uint32 values
        """
        if item_array.dtype == uint32:
            i = item_array.view(dtype=np.dtype([('f0', '>u2'), ('f1', '>u2')]))
            item_array = (
                i['f1'].astype(np.uint32) << 16) + i['f0'].astype(np.uint32)
        return item_array

    def _get_mode1_pixel_data(self, f, buffer_ix, module_ix):
        """Return the pixel data corresponding to mapping mode 1 and indexed by
        buffer_ix, module_ix

        Keyword arguments:
        f - netCDF file handle
        buffer_ix - 0-based int referring to buffer contained in netCDF file.
        module_ix - 0 -> max_module-1 for the current file.

        Returns:
        An ndarray view with dtype=pixel_header_mode1_static_fixedbins_dtype

        """
        array_data = f.variables['array_data']
        module_data = array_data[buffer_ix, module_ix, :]
        data = module_data[256: 256 + 256 + 4 * self.mca_bins]
            # skip buffer header
        dynamic_data = data.view(
            pixel_header_mode1_static_fixedbins_dtype(self.mca_bins))
        return dynamic_data

    def _get_fixedbins_spectrum(self, path, buffer_ix, module_ix, channel):
        """Return the spectrum array indexed by the buffer_ix, module_ix, and channel
        indices. This assumes that MCAs are all equal in length = self.mca_bins.

        Keyword arguments:
        path - netCDF file path
        buffer_ix - 0-based int referring to buffer contained in netCDF file.
        module_ix - 0 -> max_module-1 for the current file.
        channel - 0-3

        Returns:
        An ndarray with self.mca_bins uint16-words

        """
        f = netcdf_file(path, 'r')
        dynamic_data = self._get_mode1_pixel_data(f, buffer_ix, module_ix)
        f.close()

        return dynamic_data['ch{}_spectrum'.format(channel)][0]

    def _get_statistic(self, path, buffer_ix, module_ix, channel, metric):
        """Return the channel statistic specified by metric from the pixel data
        indexed by the buffer_ix, module_ix, and channel indices.
        This assumes that MCAs are all equal in length = self.mca_bins.

        Keyword arguments:
        path - netCDF file path
        buffer_ix - 0-based int referring to buffer contained in netCDF file.
        module_ix - 0 -> max_module-1 for the current file.
        channel - 0-3
        metric - one of 'realtime', 'livetime', 'triggers', 'output_events'

        Returns:
        uint32 containing the metric

        """
        f = netcdf_file(path, 'r')
        dynamic_data = self._get_mode1_pixel_data(f, buffer_ix, module_ix)
        f.close()

        assert metric in ['realtime', 'livetime', 'triggers', 'output_events']
        item_array = self._uint32_swap_words(
            dynamic_data['ch{}_{}'.format(channel, metric)])
        return item_array[0]

    def _get_pixel_header_mode1_item(self, path, buffer_ix, module_ix, item):
        """Return the specified item from the pixel header indexed by the
        buffer_ix and module_ix indices.
        This assumes that MCAs are all equal in length = self.mca_bins.

        Keyword arguments:
        path - netCDF file path
        buffer_ix - 0-based int referring to buffer contained in netCDF file.
        module_ix - 0 -> max_module-1 for the current file.
        item - e.g. 'total_pixel_block_size'

        Returns:
        uint16 or uint32 (item dependent)

        """
        f = netcdf_file(path, 'r')
        dynamic_data = self._get_mode1_pixel_data(f, buffer_ix, module_ix)
        f.close()

        item_array = self._uint32_swap_words(dynamic_data[item])
        return item_array[0]

    def _get_buffer_header_item(self, path, buffer_ix, module_ix, item):
        """Return the specified item from the buffer header indexed by the
        buffer_ix and module_ix indices.
        This assumes that MCAs are all equal in length = self.mca_bins.

        Keyword arguments:
        path - netCDF file path
        buffer_ix - 0-based int referring to buffer contained in netCDF file.
        module_ix - 0 -> max_module-1 for the current file.
        item - e.g. 'buffer_number'

        Returns:
        uint16 or uint32 (item dependent)

        """
        f = netcdf_file(path, 'r')
        buffer_header = self._get_buffer_header(f, buffer_ix, module_ix)
        f.close()

        item_array = self._uint32_swap_words(buffer_header[item])
        return item_array[0]

    def spectrum(self, pixel_step, row, col):
        """Return the spectrum array indexed by pixel_step, row, col.

        Keyword arguments:
        pixel_step - 0-based index to "pixel" step, i.e. mono position
        row, col - detector element row and column

        Returns:
        An ndarray with self.mca_bins uint16-words

        """
        location_indices = self._get_data_location(pixel_step, row, col)
        return self._get_fixedbins_spectrum(*location_indices)

    def statistic(self, pixel_step, row, col, metric):
        """Return the fast_peaks etc. values indexed by pixel_step, row, col.

        Keyword arguments:
        pixel_step - 0-based index to "pixel" step, i.e. mono position
        row, col - detector element row and column
        metric - one of 'realtime', 'livetime', 'triggers', 'output_events'

        Returns:
        uint32 containing the metric

        """
        path, buffer_ix, module_ix, channel = self._get_data_location(
            pixel_step, row, col)
        result = self._get_statistic(path, buffer_ix, module_ix, channel, metric)
        return result

    def buffer_header_item(self, pixel_step, row, col, item, check_validity=True):
        """Return a header item from the buffer_header indexed by pixel_step, row, col

        Keyword arguments:
        check_validity - Set False to skip check for item
        pixel_step - 0-based index to "pixel" step, i.e. mono position
        row, col - detector element row and column
        item - e.g. 'total_pixel_block_size'

        Returns:
        uint16 or uint32 (item dependent)

        """
        if check_validity:
            # Check item validity
            keys = [i[0] for i in buffer_header_dtype]
            assert item in keys

        # retrieve item
        path, buffer_ix, module_ix, _ = self._get_data_location(pixel_step, row, col)
        result = self._get_buffer_header_item(path, buffer_ix, module_ix, item)
        return result


    def pixel_header_mode1_item(self, pixel_step, row, col, item, check_validity=True):
        """Return a header item from the pixel_header indexed by pixel_step, row, col

        Keyword arguments:
        check_validity - Set False to skip check for item
        pixel_step - 0-based index to "pixel" step, i.e. mono position
        row, col - detector element row and column
        item - e.g. 'total_pixel_block_size'

        Returns:
        uint16 or uint32 (item dependent)

        """
        if check_validity:
            # Check item validity
            keys = [i[0]
                for i in pixel_header_mode1_static_fixedbins_dtype(self.mca_bins)]
            assert item in keys

        # retrieve item
        path, buffer_ix, module_ix, _ = self._get_data_location(pixel_step, row, col)
        result = self._get_pixel_header_mode1_item(path, buffer_ix, module_ix, item)

        return result


if __name__ == '__main__':
    #from profilehooks import profile

    #@profile(entries=None, immediate=True)
    def read_detector_data(detector_data, pixel_step):
        data = detector_data.spectrum(0, 0, 0)

    #@profile(entries=None, immediate=True)
    def read_detector_data_all(detector_data, pixel_step):
        for row in range(10):
            for col in range(10):
                data = detector_data.spectrum(pixel_step, row, col)

    # read data from paired files
    BASE_DIR = r'C:\Users\gary\VeRSI\NeCTAR_AS_XAS\test_data\2013-04-22_mapping_mode_collected\mnt\win'
    FILE1_DIR = os.path.join(BASE_DIR, r'ele100_1\out_1366616251')
    FILE2_DIR = os.path.join(BASE_DIR, r'ele100_2\out_1366616251')
    detector_data = DetectorData(
        shape=(10, 10), pixelsteps_per_buffer=4, buffers_per_file=5,
        dirpaths=(FILE1_DIR, FILE2_DIR), filepattern='ioc5[3-4]_([0-9]*)\.nc',
        mca_bins=2048, first_file_n=1)
    pixel_step = 5
    read_detector_data(detector_data, pixel_step)
    read_detector_data_all(detector_data, pixel_step)

    # read data from individual files
    FILE_DIR = r'C:\Users\gary\VeRSI\NeCTAR_AS_XAS\3rd_party_sw\asxas IDL\data\XAS_Example_Data'
    detector_data = DetectorData(
        shape=(10, 10), pixelsteps_per_buffer=1, buffers_per_file=1,
        dirpaths=FILE_DIR, filepattern='Cdstandard94test1_([0-9]*)',
        mca_bins=2048, first_file_n=1)
    pixel_step = 44
    read_detector_data_all(detector_data, pixel_step)
