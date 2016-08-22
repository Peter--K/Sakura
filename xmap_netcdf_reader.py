#!/usr/bin/env python

# Copyright (c) 2013-2014 Synchrotron Light Source Australia Pty Ltd.
# Released under the Modified BSD license
# See LICENSE

import numpy as np
import os
import re
from utils import memoize
from collections import defaultdict


# This module supports two netCDF file readers; scipy.io.netcdf_file and
# pupynere.netcdf_file and prefers them in that order.
# scipy.io.netcdf_file is based on pupynere.netcdf_file and is more likely to
# be installed. scipy.io.netcdf_file and pupynere.netcdf_file are pure-Python modules.
NETCDF_READER = None
uint16 = '>u2'
uint32 = '>u4'

try:
    import scipy.io
except:
    print 'Could not import scipy.io'

try:
    from scipy.io import netcdf_file
    NETCDF_READER = 'scipy'
except:
    try:
        from pupynere import netcdf_file
        NETCDF_READER = 'pupynere'
    except:
        print 'no netCDF reader found'
print NETCDF_READER


CHANNELS_PER_MODULE = 4


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


class DataCache(dict):
    """The module_data_cache implements a lazy read system for reading all data from
    specific files. Attempting to read data for a (step, row, col) triple looks in
    module_data_cache. A cache hit causes data to be read from the module_data and
    channel specified:
    {(step, row, col): [module_data object reference, 0-3], ... }

    """
    def __init__(self, fn):
        self.fn = fn

    def __missing__(self, key):
        lookup = self.fn(key)
        self[key] = lookup
        return lookup


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
        buffers_per_file - no. of buffers per group of p netCDF files.
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
        self.file_paths_dict = self._get_all_file_groups()
        self.files_indexed_by_pixel_step = self._get_file_paths_for_all_pixel_steps()
        self.reverse_lookup_file_paths_dict = self._build_reverse_file_lookup(
            self.files_indexed_by_pixel_step)
        # Create data cache to implement single-file reading on any data access
        self.module_data_cache = DataCache(self._default_cache_entry_factory)

    def _get_all_file_groups(self):
        """Get the paths to netCDF files on disk corresponding to all available
        file indices, sorted based on filename.

        Returns:
        a dictionary keyed by filepattern regex capture group value containing a sorted
        list of full paths to files for that value. Sorting is based on the filename only
        without the path info.

        """
        # get a list of all files with full paths 
        allfiles = []
        for d in self.dirpaths:
            files = os.listdir(d)
            paths = [os.path.join(d, f) for f in files]
            allfiles.extend(paths)

        # now create a dict containing lists of all matching files (with full path) with
        # keys matching the capture group value
        prog = re.compile(self.filepattern)
        files = {os.path.basename(f): f for f in allfiles}  # a lookup of paths from files
        pathsdict = defaultdict(list)
        for f in files:
            if prog.match(f):
                pathsdict[int(prog.match(f).group(1))].append(files[f])

        # now sort all the lists based on the basename only, i.e. ignore the directory
        for i in pathsdict:
            pathsdict[i] = sorted(pathsdict[i], key=lambda x: os.path.basename(x))

        return pathsdict

    def _get_file_paths_for_all_pixel_steps(self):
        """Get the paths to netCDF files on disk corresponding to all available
        pixel_steps, sorted based on filename.

        Returns:
        a dictionary keyed by pixel step with values containing a sorted list of full
         paths to files for that step. Sorting is based on the filename only
        without the path info.

        """
        p = 0
        pathsdict = {}
        while True:
            pathsdict[p] = self._get_file_paths_for_pixel_step(p)
            if pathsdict[p]:
                # got back some paths
                p += 1
            else:
                # got back an empty list, i.e. a cache miss
                del pathsdict[p]
                break

        return pathsdict

    def _build_reverse_file_lookup(self, d):
        """Builds a dictionary of pixel_steps keyed by the corresponding file basename.
        e.g. an arbitrary example of an entry might be 'ioc53_10.nc':[24,25,26]
        Note, this doesn't tell you which detector elements are contained in that file,
        so for example, there might also be another entry 'ioc54_10.nc':[24,25,26] if
        there are multiple IOCs.

        Keyword arguments:
        d - dictionary returned by _get_file_paths_for_all_pixel_steps()

        Returns:
        Dictionary of keys equal to file basenames and value entries a list of
        contained pixel_steps in numerically increasing order.
        e.g. {'ioc53_1.nc':[0,1], 'ioc54_1.nc':[0,1],
              'ioc53_2.nc':[2,3], 'ioc54_2.nc':[2,3], ...}

        """
        stepdict = defaultdict(list)
        for key, val in d.iteritems():
            for name in val:
                stepdict[os.path.basename(name)].append(key)

        # now sort all the lists numerically
        for i in stepdict:
            stepdict[i].sort()

        return stepdict

    @memoize
    def _get_file_paths_for_pixel_step(self, pixel_step):
        """Get the paths to netCDF files on disk corresponding to a given
        pixel_step, sorted based on filename.
        Raises an IndexError if files are not found.

        Keyword arguments:
        pixel_step - 0-based int.

        Returns:
        list of full paths to files for the specified pixel_step.

        """
        file_n = self.first_file_n + pixel_step // (
            self.pixelsteps_per_buffer * self.buffers_per_file)
        return self.file_paths_dict[file_n]

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

    def _enumerate_all_data_indices_in_file(self, filename):
        """Given a filename, returns a list of tuples
        (pixel_step, row, col, channel, buffer_ix, module_ix)
        for indexing the file contents.

        Keyword arguments:
        filename - string e.g. 'ioc53_1.nc'

        Returns:
        A list of all 6-tuples (pixel_step, row, col, channel, buffer_ix, module_ix)
        enumerating the contents, where:
            pixel_step, row, col - detector element indices
            channel - 0-3
            buffer_ix - 0-based int referring to buffer contained in netCDF file.
            module_ix - 0 -> max_module-1 for the current file.

        """
        # pixel step range for this file
        pixel_steps = self.reverse_lookup_file_paths_dict[filename]
        # get element range for this file, e.g. 0, 51 (first 52 of 100-element detector)
        p = len(self.file_paths_dict[self.first_file_n])
        m = self.rows * self.cols / CHANNELS_PER_MODULE
        modules_per_file = int(np.ceil(float(m) / p))

        # now we have modules_per_file, get the file index so we can determine the
        # element range
        files_for_this_step = self._get_file_paths_for_pixel_step(pixel_steps[0])
        files_for_this_step = [os.path.basename(f) for f in files_for_this_step]
        file_index = files_for_this_step.index(filename)

        # if e.g. file_index==n, range is
        # n*elements_in_file -> (n+1)*elements_in_file-1.
        elements_per_file = modules_per_file * CHANNELS_PER_MODULE
        low_element = file_index * elements_per_file
        # The last file in a group may contain fewer elements.
        if files_for_this_step[-1] == filename:
            high_element_plus1 = self.rows * self.cols
        else: 
            high_element_plus1 = (file_index + 1) * elements_per_file

        # Now collect the tuples
        indices = []
        for pixel_step in pixel_steps:
            for el in range(low_element, high_element_plus1):
                row, col = divmod(el, self.cols)

                # Get module index from element index
                module_ix, channel = divmod(row * self.rows + col, CHANNELS_PER_MODULE)

                # Now get the file and module index within that file by assuming the
                # modules are split evenly across the IOCs and are in increasing
                # sequential order
                module_ix = module_ix % modules_per_file
                buffer_ix = pixel_step % self.pixelsteps_per_buffer
                indices.append( (pixel_step, row, col, channel, buffer_ix, module_ix) )

        return indices

    def _default_cache_entry_factory(self, key):
        """Called on a DataCache access __missing__() call.
        Gets all (step, row, col) entries for the file indexed by key and reads all data
        returning the entry for the requested key

        Arguments:
        key - (pixel_step, row, col) tuple

        """
        # A cache miss will generate a file lookup, read and cache of the associated data.
        path, _, _, _ = self._get_data_location(*key)   # path of file containing our data

        # Generate all the entries like the following for data in the file path
        # {(step, row, col): [module_data object reference, 0-3], ... }
        # First, enumerate data indices in current file.
        indices = self._enumerate_all_data_indices_in_file(os.path.basename(path))

        # OK, now read everything from the file
        f = netcdf_file(path, 'r')
        # buffer_ix, module_ix
        for pixel_step, row, col, channel, buffer_ix, module_ix in indices:
            self.module_data_cache[(pixel_step, row, col)] = \
                [self._get_mode1_pixel_data(f, buffer_ix, module_ix), channel]
        f.close()

        return self.module_data_cache[key]

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
        data = module_data[256: 256 + 256 + 4 * self.mca_bins]  # skip buffer header
        dynamic_data = data.view(pixel_header_mode1_static_fixedbins_dtype(self.mca_bins))
        return dynamic_data

    def spectrum(self, pixel_step, row, col):
        """Return the spectrum array indexed by pixel_step, row, col.

        Keyword arguments:
        pixel_step - 0-based index to "pixel" step, i.e. mono position
        row, col - detector element row and column

        Returns:
        An ndarray with self.mca_bins uint16-words

        """
        # retrieve item - we get a [buffer, channel] list
        data, channel = self.module_data_cache[(pixel_step, row, col)]
        # now extract what we're after
        item_array = data['ch{}_spectrum'.format(channel)]
        return item_array[0]

    def statistic(self, pixel_step, row, col, metric):
        """Return the fast_peaks etc. values indexed by pixel_step, row, col.

        Keyword arguments:
        pixel_step - 0-based index to "pixel" step, i.e. mono position
        row, col - detector element row and column
        metric - one of 'realtime', 'livetime', 'triggers', 'output_events'

        Returns:
        uint32 containing the metric

        """
        # retrieve item - we get a [buffer, channel] list
        data, channel = self.module_data_cache[(pixel_step, row, col)]
        assert metric in ['realtime', 'livetime', 'triggers', 'output_events']
        # now extract what we're after
        item_array = self._uint32_swap_words(data['ch{}_{}'.format(channel, metric)])
        return item_array[0]

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
            keys = [i[0] for i in pixel_header_mode1_static_fixedbins_dtype(self.mca_bins)]
            assert item in keys
 
        # retrieve item - we get a [buffer, channel] list
        data, _ = self.module_data_cache[(pixel_step, row, col)]
        # now extract what we're after
        item_array = data[item]
        return item_array[0]

    def pixel_header_mode1_channel_item(self, pixel_step, row, col, item,
                                        check_validity=True):
        """Return a header item from the pixel_header indexed by pixel_step, row, col

        Keyword arguments:
        check_validity - Set False to skip check for item
        pixel_step - 0-based index to "pixel" step, i.e. mono position
        row, col - detector element row and column
        item - e.g. 'realtime'

        Returns:
        uint16 or uint32 (item dependent)

        """
        # retrieve item - we get a [buffer, channel] list
        data, channel = self.module_data_cache[(pixel_step, row, col)]
        # now extract what we're after
        item = 'ch{}_{}'.format(channel, item)
        if check_validity:
            # Check item validity
            keys = [i[0] for i in pixel_header_mode1_static_fixedbins_dtype(self.mca_bins)]
            assert item in keys

        item_array = data[item]
        return item_array[0]

if __name__ == '__main__':
    pass
