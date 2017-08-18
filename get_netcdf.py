#!/usr/bin/env python

import os
import numpy as np
from xmap_netcdf_reader import DetectorData
import readMDA

from memoize_core import Memoizer
store = {}
expiring_memoize = Memoizer(store)

from utils import memoize

#
# set up a CLASS for detector pixels
#

"""
This module provides an interface to a DetectorData netCDF reader object that provides
the same interface to netCDF-based mapping-mode data as for mda-file-based step-mode data.
For example, step-mode data from the 100-element Canberra detector is accessed from Sakura
through a list object that contains pixel objects, each of which accesses the roi, fpeaks,
speaks values through attributes (.roi, .fpeaks, .speaks). Access to an individual pixel
object is through a standard list indexing operation, e.g. self.det[i], so accessing the
ith pixel's roi value would be self.det[i].roi
Furthermore, the pixel class for step-mode data provides a number of methods that are
also provided here in the Pixel class, e.g. .DeadCorr(), .NormIO().
To speed up access to computed roi, fpeaks and speaks values, which are accessed using the
attribute syntax (self.det[i].fpeaks, self.det[i].speaks, self.det[i].roi), fpeaks and
speaks values are computed once and cached (@memoize decorator), and the roi value is
computed and temporarily cached (@expiring_memoize decorator with 10s expiry).
The roi value in particular is computed on the fly based on the roi limits (roi_low and
roi_high) stored in the Detector instance (e.g. self.det.roi_low).

"""

class Pixel(object):
    """Class to describe a detector element and its 'contents'
    There will be 100 instances later to represent the 100-element detector.

    """
    __pxId = 0    # class variable for generating a unique pixel id on construction

    def __init__(self, detector):
        self.detector = detector    # set the "parent" detector
        self.detector_data = detector.detector_data
        # assign and increment unique id
        self.pixNum = Pixel.__pxId
        Pixel.__pxId += 1
        self.row, self.col = divmod(self.pixNum, self.detector.rows)
        self.roiCorr = None
        self.roiCorrNorm = None
        self.weightedSpec = None
        self.weightFactor = None
        self.chi = None
        self.tau = None

    @classmethod
    def __reset_px_count__(self):
        """Call this class method to reset the pixel Id class variable"""
        Pixel.__pxId = 0

    # expose the DetectorData spectrum(), statistic() and
    #    pixel_header_mode1_item() methods here
    def spectrum(self, pixel_step):
        return self.detector_data.spectrum(pixel_step, row=self.row, col=self.col)

    @memoize
    def statistic(self, *args, **kwargs):
        return self.detector_data.statistic(*args, **kwargs)

    def pixel_header_mode1_item(self, *args, **kwargs):
        return self.detector_data.pixel_header_mode1_item(*args, **kwargs)

    def _GetSpectrumROI(self, pixel_step, low, high):
        """ low and high are semi-open range indices
        """
        spectrum = self.detector_data.spectrum(pixel_step, self.row, self.col)
        return spectrum[low:high]

    @expiring_memoize(max_age=10)
    def _roi(self, roi_low, roi_high):
        data = np.array([self._GetSpectrumROI(step, roi_low, roi_high).sum()
                         for step in self.detector.steprange])
        data /= self.detector.ts
        return data

    @property
    @memoize
    def fpeaks(self):
        data = np.array([self.statistic(step, self.row, self.col, 'realtime')
                        for step in self.detector.steprange])
        data /= self.detector.ts
        return data

    @property
    @memoize
    def speaks(self):
        data = np.array([self.statistic(step, self.row, self.col, 'livetime')
                        for step in self.detector.steprange])
        data /= self.detector.ts
        return data

    @property
    def roi(self):
        return self._roi(self.detector.roi_low, self.detector.roi_high)

    def GetDead(self, fpeaks, speaks):
        # get detector dead time parameter "tau"
        try:
            self.tau = fpeaks.astype(float) / speaks
        except ZeroDivisionError:
            self.tau = fpeaks

    def DeadCorr(self, tau, roi):
        # apply dead time parameter
        self.roiCorr = roi * tau

    def NormI0(self, I0):
        # normalise data to incoming intensity (I0)
        self.roiCorrNorm = self.roiCorr / I0

    def WeightSpectrum(self):
        # apply weight factor which was derived from relative edge step
        self.weightedSpec = self.weightFactor * self.roiCorrNorm


class Detector(list):
    """A detector class that acts like a list container for accessing pixel elements
    http://stackoverflow.com/questions/921334/how-to-use-classes-derived-from-pythons-list-class
    http://docs.python.org/2/reference/datamodel.html#emulating-container-types
    It needs to store a reference to a DetectorData instance and contain all the pixel
    objects.

    """
    def __init__(self, detector_data):
        """detector_data is a DetectorData instance
        """
        self.detector_data = detector_data
        self.rows, self.cols = detector_data.shape
        detector_size = self.rows * self.cols
        Pixel.__reset_px_count__()
        self.det = [Pixel(self) for _ in range(detector_size)]
        self.steprange = None           # Holds an iterable containing the energy/mca/pixel-steps
        self.iter_pointer = 0
        # The roi limits will apply to all contained detector elements - the pixel
        # element objects keep a reference to this object so they can access these fields
        self.roi_low = None
        self.roi_high = None
        self.ts = None

    # Implement __getitem__, __setitem__, __iter__ and __len__ methods to implement
    # list-like behaviour
    def __getitem__(self, key):
        return self.det[key]

    def __setitem__(self, key, value):
        self.det[key] = value

    def __iter__(self):
        # from http://stackoverflow.com/questions/4019971/how-to-implement-iter-self-for-a-container-object-python
        if hasattr(self.det[0], "__iter__"):
            return self.det[0].__iter__()
        return self.det.__iter__()

    def __len__(self):
        return len(self.det)

    def __str__(self):
        return '<{}.{} object at {}>'.format(
            self.__class__.__module__,
            self.__class__.__name__,
            hex(id(self))
        )

    # Methods for our container class additional to those required for list-like behaviour

    def set_ts(self, ts):
        """Set sample times for NormT correction."""
        self.ts = ts


def getAllExtraPVs(fname):
    """Return a dictionary of all "Extra" PVs, indexed by the part of the PV name
    following the colon, e.g. if fname contains the PV SR12ID01DET01:mca1.R0LO with a
    value ("long", "", [1200]), the returned dict will contain a key:value entry
    'mca1.R0LO':("long", "", [1200]), where the value is the triple obtained from readMDA

    Arguments:
    fname - mda filename

    Returns:
    dict e.g. {'mca1.R0LO':("long", "", [1000]), 'mca1.R0HI':("long", "", [1200]), ...}

    """
    # get the path to the netCDF files from the mda file
    mda = readMDA.readMDA(fname, verbose=False)
    extra_pvs = mda[0]         # get the first list entry - a dict containing the PVs
    extra_pvs_dict = {i.split(':')[-1]: extra_pvs[i] for i in extra_pvs}
    return extra_pvs_dict


def getExtraPV(mda_list, pv):
    """Return the PV value using the PV part of an IOC:PV id for matching
    e.g. getExtraPV(mda_list, 'CUR_TIME_STAMP') will match SR12ID01MC01:CUR_TIME_STAMP
    then use this as the key to retrieve the corresponding value from the dictionary
    inside mda_list

    Arguments:
    mda_list - the list returned by Tim Mooney's readMDA
    pv - a string, e.g. 'CUR_TIME_STAMP'

    Returns:
    The matching PV keyname in the dict inside mda_list

    """
    extra_pvs = mda_list[0]         # get the first list entry - a dict containing the PVs 
    keys = {i.split(':')[-1]: i for i in extra_pvs}
    return extra_pvs[keys[pv]]


def highest_available_scandata(detector, scanSize):
    """Step through the netCDF files to verify we have all the fluoresence data available
    Arguments:
    detector - detector instance reference
    scanSize - expected number of pixel steps, likely based on the number written in the
               mda file

    Returns:
    index of the highest pixel step read (0-based)

    Exceptions:
    Raises IndexError if expected data is unavailable

    """
    for i in range(scanSize):
        try:
            detector.det[0].pixel_header_mode1_item(i, 0, 0, 'tag0', check_validity=False)
        except Exception as exc:
            print 'netCDF data truncated', exc.message
            i = i - 1
            break
    return i + 1


def getData(fname):
    """Extract data from mda-ASCII file and distribute into Pixel objects

    Returns: XAS scan data in a detector 'object' (variable "det")
            energy axis, transmission data array and detector filled with fluo data
    (detector object simply full of '0' values if no fluorescence data available)
    Transmission data in "trans" comprises encoder_E, I0/1/2, sample_time, encoder_angle
    !! I0/1/2  are already normalised to t !!

    """
    # get the path to the netCDF files from the mda file
    mda = readMDA.readMDA(fname, verbose=False)
    netcdf_basename = os.path.splitext(os.path.basename(fname))[0]
    netcdf_directory = os.path.join(os.path.dirname(os.path.abspath(fname)),
                                    netcdf_basename)
    netcdf_filepattern = '{}_([0-9]*)\.nc'.format(netcdf_basename)

    scanData = mda[1]
    scanSize = scanData.npts

    # create and set the reader for the fluorescence detector
    detector_data = DetectorData(shape=(6, 6), pixelsteps_per_buffer=1,
        buffers_per_file=1, dirpaths=netcdf_directory,
        filepattern=netcdf_filepattern, mca_bins=2048, first_file_n=1)

    detector = Detector(detector_data)

    # set scanSize according to the netCDF data that was available
    scanSize = highest_available_scandata(detector, scanSize)
    detector.steprange = range(scanSize)

    # read transmission data
    # The PVs listed in pvColumnNames all refer to columnar data such as axis values.
    # This is contrasted by thoselisted in pvSingleValues, which are all single values.
    pvColumnNames = ['EncEnergy:ActPos', 'scaler1:S2C', 'scaler1:S3C',
                     'scaler1:S4C', 'scaler1.T', 'EncAngle:ActPos']

    trans = np.empty((len(pvColumnNames), scanSize))
    for series in scanData.d:
        try:
            tag = ':'.join(series.name.split(':')[1:])  # use the PV part after the IOC id
            if tag in pvColumnNames:
                trans[pvColumnNames.index(tag)] = series.data[:scanSize]
        except Exception as e:
            print e
            print 'missing PV ' + tag

    ts = trans[pvColumnNames.index('scaler1.T')]    # get the sample time
    detector.set_ts(ts)
    e = trans[pvColumnNames.index('EncEnergy:ActPos')] * 1000.0  # Energy axis (in eV !!)

    # normalise I0, I1, I2 to sample_time ts (use string "scaler1:" as identifier)
    for i, name in enumerate(pvColumnNames):
        if name.startswith('scaler1:'):
            trans[i] = trans[i] / ts

    ## call dead time correction later; should be performed only on
    ## good spectra ("goodPixels") as bad spectra can contain zeros which
    ## this function would divide by
    ## call is via function:  detDeadCorr(det, goodPixels)

    return e, trans, detector


if __name__ == '__main__':
    pass
