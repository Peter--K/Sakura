#!/usr/bin/env python

import os
import numpy as np
from xmap_netcdf_reader import DetectorData
import readMDA

from utils import memoize

#
# set up a CLASS for detector pixels
#


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

    # expose the DetectorData spectrum(), statistic(), buffer_header_item() and
    #    pixel_header_mode1_item() methods here
    def spectrum(self, *args, **kwargs):
        return self.detector_data.spectrum(*args, **kwargs)

    @memoize
    def statistic(self, *args, **kwargs):
        return self.detector_data.statistic(*args, **kwargs)

    def pixel_header_mode1_item(self, *args, **kwargs):
        return self.detector_data.pixel_header_mode1_item(*args, **kwargs)

    def buffer_header_item(self, *args, **kwargs):
        return self.detector_data.buffer_header_item(*args, **kwargs)

    def _GetSpectrumROI(self, pixel_step, low, high):
        """ low and high are semi-open range indices
        """
        spectrum = self.detector_data.spectrum(pixel_step, self.row, self.col)
        return spectrum[low:high]

    @property
    @memoize
    def fpeaks(self):
        return np.array([self.statistic(step, self.row, self.col, 'realtime')
                        for step in range(self.detector.steps)])

    @property
    @memoize
    def speaks(self):
        return np.array([self.statistic(step, self.row, self.col, 'livetime')
                        for step in range(self.detector.steps)])

    @property
    @memoize
    def roi(self):
        return np.array([self._GetSpectrumROI(step, self.detector.roi_low,
                         self.detector.roi_high).sum()
                        for step in range(self.detector.steps)])

#     def NormT(self, tsample) :
#         # normalise all raw data (FastPeaks, SlowPeaks, ROI) to sampling time tsample
#         self.fpeaks = np.divide(np.ndarray.flatten(self.fpeaks), tsample)
#         self.speaks = np.divide(np.ndarray.flatten(self.speaks), tsample)
#         self.roi = np.divide(np.ndarray.flatten(self.roi), tsample)

    def GetDead(self, fpeaks, speaks):
        # get detector dead time parameter "tau"
        try:
            self.tau = fpeaks / speaks
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
        self.weightedSpec = self.weightFactor * self.roiCorr


class Detector(list):
    """A detector class that acts like a list container for accessing pixel elements
    http://stackoverflow.com/questions/921334/how-to-use-classes-derived-from-pythons-list-class
    http://docs.python.org/2/reference/datamodel.html#emulating-container-types
    It needs to store a reference to a DetectorData instance and contain all the pixel
    objects.

    """
    def __init__(self, detector_data):
        """detector is a DetectorData instance
        """
        self.detector_data = detector_data
        self.rows, self.cols = detector_data.shape
        detector_size = self.rows * self.cols
        self.det = [Pixel(self) for _ in range(detector_size)]
        self.steps = None           # Holds no. of energy/mca/pixel-steps
        self.iter_pointer = 0
        # The roi limits will apply to all contained detector elements - the pixel
        # element objects keep a reference to this object so they can access these fields
        self.roi_low = 0
        self.roi_high = -1

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
    def set_roi_limits(self, low, high):
        """Set the roi limits for the detector."""
        self.roi_low = low
        self.roi_high = high


def getExtraPV(mda_dict, pv):
    """Return the PV value using the PV part of an IOC:PV id for matching
    e.g. getExtraPV(mda_dict, 'CUR_TIME_STAMP') will match SR12ID01MC01:CUR_TIME_STAMP

    Arguments:
    mda_dict - the dict returned by Tim Mooney's readMDA
    pv - a string, e.g. 'CUR_TIME_STAMP'

    Returns:
    The matching PV keyname in the mda_dict

    """
    extra_pvs = mda_dict[0]
    keys = {i.split(':')[-1]: i for i in extra_pvs}
    return extra_pvs[keys[pv]]


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
    timestamp = getExtraPV(mda, 'CUR_TIME_STAMP')[-1][0]
    netcdf_directory = os.path.join(os.path.dirname(os.path.abspath(fname)),
                                    'out_{}'.format(timestamp))

    scanData = mda[1]
    scanSize = scanData.npts

    # create and set the reader for the fluorescence detector
    detector_data = DetectorData(shape=(10, 10), pixelsteps_per_buffer=1,
                                 buffers_per_file=1, dirpaths=netcdf_directory,
                                 filepattern='ioc5[3-4]_([0-9]*)\.nc', mca_bins=2048, first_file_n=1)

    detector = Detector(detector_data)
    detector.set_roi_limits(600, 800)

    # step through the netCDF files to verify we have all the fluoresence data available
    for i in range(scanSize):
        try:
            detector.det[0].pixel_header_mode1_item(i, 0, 0, 'tag0')
        except IndexError:
            print 'netCDF data truncated'
    scanSize = i + 1    # set scanSize according to the netCDF data that was available
    detector.steps = scanSize

    # read transmission data
    pvColumnNames = ['EncEnergy:ActPos', 'scaler1:S2C', 'scaler1:S3C',
                     'scaler1:S4C', 'scaler1.T', 'EncAngle:ActPos']

    trans = np.empty((len(pvColumnNames), scanSize))
    for series in scanData.d:
        try:
            tag = ':'.join(series.name.split(':')[1:])  # use the PV part after the IOC id
            if tag in pvColumnNames:
                trans[pvColumnNames.index(tag)] = series.data
        except:
            print 'missing PV ' + tag

    ts = trans[pvColumnNames.index('scaler1.T')]    # get the sample time
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


def getAverage(goodPixels, det):
    """
    Compute the average of all weighted, deadtime corrected spectra
    (from det[i].weightedSpec, which is = det[i].roiCorr * det[i].weightFactor)

    Returns:
    averageMu [...]Chi

    """
    # goodPixels is designed to include index values <0 to mark bad pixels;
    #    thus, needs compressing out all indices <0 first before using in a loop
    goodPixels = goodPixels[goodPixels >= 0]
    #
    scanSize = len(
        det[0].fpeaks)   # choose random pixel array to determine scan length
    averageMu = np.zeros(scanSize)
    averageChi = np.zeros(len(det[goodPixels[0]].chi))
    for i in goodPixels:
        averageMu = averageMu + det[i].weightedSpec
        averageChi = averageChi + det[i].chi
    averageMu = averageMu / len(goodPixels)
    averageChi = averageChi / len(goodPixels)

    return averageMu, averageChi


def getWeightFactors(det, e, e0, goodPixels):
    """Run through all detector pixels and determine a weight factor
             (= edge-step / pre-edge-background-intensity)

    Returns:
    nothing but writes weight factors
    into detector pixel Class as attribute to each pixel

    """
    weights = np.zeros(len(det))
    for i in range(len(det)):
        det[i].weightFactor = 0

    det[0].k = 1.0
    for i in goodPixels:
        det[i].chi = 1.0
        weights[i] = 1.0

    weights = weights / np.nanmax(weights)

    for i in goodPixels:
        det[i].weightFactor = weights[i]

    return weights


def getGoodPixels(det, detSize):
    """FUNCTION to check data from individual detector pixels for quality and
              remove any bad pixels from the list of pixels considered
       returns: "goodPixels", a 1-D array of "detSize" marking bad pixels with value "-2"
    """
    # define goodPixels array
    goodPixels = np.arange(detSize)

    #     to start with, assume that all pixels (spectra) are good
    #  (list is complete; over time, elements of bad pixels will be set to -2 or -1;
    #    * where goodPixels is used, the list will be compressed
    #      to remove the '-2' indices and thus permit easy
    #       looping via 'for i in goodPixels : [...]';
    #    * later in the code, we use '-1' to exclude spectra
    #      following user interaction; the '-2's cannot be undone
    #      while the '-1's can
    #    * ultimately, goodPixels will contian indices >0
    #     of spectra to be processed further and included in the
    #     weighted, corrected average of pixels)

    # ------------------------------------------------------------------------
    # test for bad pixels -- Step 1:
    #    all pixels that are defunct (average <= 10 cts/sec) are excluded
    # ------------------------------------------------------------------------
    tempROIaverage = np.zeros(detSize)
    for i in range(detSize):
        tempROIaverage[i] = np.mean(det[i].roi)

    # search through ROIaverage and set to '-2' all indices of elements
    #    below certain threshold  (here, ROIaverage <10 cts/sec)
    excludeForeverPixels = np.where(tempROIaverage < 10)[0]
    goodPixels[excludeForeverPixels] = -2

    # ------------------------------------------------------------------------
    # test for bad pixels -- Step 2:
    #    high TCR pixels
    # ------------------------------------------------------------------------
    #
    # above approach works well for defunct (low count rate) detector
    #    pixels, but it does not work for pixels that are just clocking up
    #    randomly high count rates
    # thus, out of now remaining GoodPixels,
    #    if TCR average of pixel > 3-times average TCR-average, then exclude
    #   the factor "3" is stored in "cutOffFactor = 3"; *** modify this if required ***
    #
    cutOffFactor = 3
    remainPixels = np.compress(goodPixels >= 0, goodPixels)
    tempTCRaverage = []
    for i in remainPixels:
        tempTCRaverage = np.append(tempTCRaverage, np.mean(det[i].fpeaks))
    badTCRpixels = np.where(
        tempTCRaverage > cutOffFactor * np.mean(tempTCRaverage))
    goodPixels[remainPixels[badTCRpixels]] = -2
    excludeForeverPixels = np.append(excludeForeverPixels, badTCRpixels)
    print 'exclude forever (mark red): ', excludeForeverPixels

    # ------------------------------------------------------------------------
    # test for bad pixels -- Step 3:
    #    SlowPeaks have zero values
    # ------------------------------------------------------------------------
    # problematic are also pixels that show Zeros in some of the SlowPeaks
    #   ("det.speaks") as they cause infinity values ("nan") when computing #
    #   detector dead time correction by using the ratio "FastPeaks/SlowPeaks";
    # thus, out of now remaining GoodPixels,
    #    if SlowPeaks = 0 anywhere, set value to +1
    #    (a spectrum could still be OK, even though there might be a zero
    #     count in the background before the edge in low-TCR scenarios)
    #
    #
    # GR20130716
    # I've commented out the following line because I don't want to overwrite the speaks
    # property - I prefer to just catch any divide-by-zero exceptions as they occur
    #
    # for i in goodPixels :
    #     det[i].speaks[ np.where(det[i].speaks == 0) ]  = 1
    #
    return goodPixels, excludeForeverPixels


if __name__ == '__main__':
    pass
