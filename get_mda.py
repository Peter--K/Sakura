#!/usr/bin/env python

#
# careful with the variable "goodPixels";
#   * we have "self.goodPixels" in the GUI code which is managed over there
#     to keep track of good spectra as the user de-selects and re-selects
#     detector pixels (spectra) to include;
#   * consequently, the detector dead time correction Method will need to be
#     called upon from the GUI, because goodPixels is only known there
#   * the functions in this library will thus be called with "self.goodPixels"
#     going in; while within this library (via __main__), we have a separate
#     function "getGoodPixels" which deliveres an array useful for debugging and coding
#


# ToDo: check that no critical parameter is strictly dependent on existence of data in a
#       specific pixel (e.g., "len(det[0].chi" or similar))


import os
import numpy as np
import readMDA
#import pylab as pl
#import Ifeffit
import time
from textwrap import dedent
from itertools import chain, repeat, izip
import version
import wx

from numpy import polyfit, polyval

import edge_tables as etab


class pixel(object):
    """Class to describe a detector pixel and its 'contents'.
    Will make 100 instances later to represent 100-element detector.

    """
    def __init__(self, pixNum):
        self.pixNum = pixNum

    def CreateArrays(self, size):
        self.fpeaks = np.zeros((size, 1))
        self.speaks = np.zeros((size, 1))
        self.roi = np.zeros((size, 1))

    def NormT(self, tsample):
        """ normalise all raw data (FastPeaks, SlowPeaks, ROI) to sampling time
        tsample.

        """
        self.fpeaks = np.divide(np.ndarray.flatten(self.fpeaks), tsample)
        self.speaks = np.divide(np.ndarray.flatten(self.speaks), tsample)
        self.roi = np.divide(np.ndarray.flatten(self.roi), tsample)

    def ICRCorr(self, fpeaks, ICRCorrParams):
        """apply dead time correction to ICR (fpeaks)
        for better normalisation"""
        self.fpeaksCorr = sum(
            [(fpeaks**i) * ICRCorrParams[i] for i in np.arange(4)]
        )

    def GetDead(self, fpeaks, speaks):
        """get detector dead time parameter 'tau' """
        self.tau = fpeaks.astype(float) / speaks

    def DeadCorr(self, tau, roi):
        """apply dead time parameter"""
        self.roiCorr = roi * tau

    def NormI0(self, I0):
        """normalise data to incoming intensity (I0)"""
        self.roiCorrNorm = self.roiCorr / I0

    def WeightSpectrum(self):
        """apply weight factor which was derived from relative edge step"""
        self.weightedSpec = self.weightFactor * self.roiCorrNorm


def makeDet(detSize, scanSize):
    """Combines 100 pixels into one multi-element detector.

    Returns:
    a list of size "detSize" (e.g., 100) "Pixel" objects

    """
    det = [pixel(i) for i in np.arange(detSize)]
    for j in np.arange(detSize):
        det[j].CreateArrays(scanSize)
    return det


def readICRParams(selection, e, threshold, detSize, home_path):
    """Reads in detector deadtime parameter file to correct ICR

    Parameters:
      selection = type of dead-time correction;
                  0 = ICR_correct / OCR     (preferred option; default; see GUI)
                  1 = ICR / OCR             ( = FastPeaks / SlowPeaks)
      e = energy axis
      threshold = cut-off for low-energy / high-energy detector mode
      detSize = number of detector pixels
      home_path = SAKURA_HOME_PATH
    Returns:
    """
    if detSize == 100 :
        filename = "100eleICRcorrect"
    elif detSize == 36 :
        filename = "36eleICRcorrect"

    if selection == 0 :
        if e[0] < threshold :
            filename = filename + "-lowE.ini"
        else :
            filename = filename + "-highE.ini"
    elif selection == 1 :
        filename = filename + "-FPEAKS.ini"

    ICRCorrParams = np.loadtxt(home_path+"\\"+filename)

    return ICRCorrParams


def detDeadCorr(det, goodPixels, ICRCorrParams):
    """Correct dead time ("tau") for each detector pixel

    """
    goodPixels = np.compress(goodPixels >= 0, goodPixels)
    for i in goodPixels:
        ### DEAD TIME CORRECTION ###
        # use the next two lines for NEW DTC
        if hasattr(det[i], 'ICRCorr'):
            det[i].ICRCorr(det[i].fpeaks, ICRCorrParams[i])

        if hasattr(det[i], 'fpeaksCorr'):
            det[i].GetDead(det[i].fpeaksCorr, det[i].speaks)
        else:
            # use next one line of OLD DTC
            det[i].GetDead(det[i].fpeaks, det[i].speaks)

        # don't modify line below
        det[i].DeadCorr(det[i].tau, det[i].roi)
    print 'ICR correction parameters (Pixel #0):', ICRCorrParams[0]
    print i


def searchStr(f, search):
    """Skip parts of the mda ASCII header (find string "search")

    Returns:
    the last string read in before exiting the loop

    """
    line = ''
    while str.count(line, search) == 0:
        line = f.readline()
        if len(line) == 0:
            break
    return line


def searchStrStarts(f, search):
    """Skips parts of mda ASCII header (find line starting with "search")

    Returns:
    the last string read in before exiting the loop

    """
    line = ''
    while not line.startswith(search):
        line = f.readline()
        if len(line) == 0:
            break
    return line


def getHeader(f):
    """Extract scan information such as
        "scanSize" (number of energy points in the XAS scan
        "detSize"  (number of detector pixels for multi-element dets.; e.g. 100)

    Returns:
    list of above parameters

    """

    # work through header to get data dimensions (as LONGintegers)
    #  (do step-by-step for better code readability)
    #
    found = searchStrStarts(f, '# Total req')
    info = found.split('=')[1]
    info = info.split('x')
    scanSize = np.long(info[0])     # "scanSize" = number of energy points in XAFS scan
    if len(info) > 1:
        detSize = np.long(info[1])  # check for 2nd dimension
    else:                           # if not present, then detSize = 0
        detSize = 0                 # (i.e., transmission XAS scan only)

    return scanSize, detSize


def getData(fname):
    """Extract data from mda-ASCII file and distribute into Pixel objects

    Returns:
    XAS scan data in a detector 'object' (variable "det") energy axis, 
    transmission data array and detector filled with fluo data
    (detector object simply full of '0' values if no fluorescence data available)
    Transmission data in "trans" comprises encoder_E, I0/1/2, sample_time, encoder_angle
    !! I0/1/2  are already normalised to t !!

    """
    mda = readMDA.readMDA(fname, verbose=True)
    scanData = mda[1]
    scanSize = scanData.npts
    try:
        detectorData = mda[2]
        detSize = detectorData.npts
    except:
        detSize = 0

    det = makeDet(detSize, scanSize)

    # read transmission data
    pvColumnNames = ['EncEnergy:ActPos', 'scaler1:S2C', 'scaler1:S3C',
                     'scaler1:S4C', 'scaler1.T', 'EncAngle:ActPos']

    trans = np.empty((len(pvColumnNames), scanSize))
    for series in scanData.d:
        try:
            tag = ':'.join(series.name.split(':')[1:])  # use the PV part after the IOC id
            trans[pvColumnNames.index(tag)] = series.data
        except:
            pass

    ts = trans[pvColumnNames.index('scaler1.T')]    # get the sample time "t_s"
    e = trans[pvColumnNames.index('EncEnergy:ActPos')] * 1000.0   # Energy axis (in eV !!)

    # normalise I0, I1, I2 to sample_time ts (use string "scaler1:" as identifier)
    for i, name in enumerate(pvColumnNames):
        if name.startswith('scaler1:'):
            trans[i] = trans[i] / ts

    # read fluorescence data (if it exists)
    if detSize != 0:
        print 'reading fluorescence data...'
        for k in range(scanSize):
            for i in np.arange(detSize):
                det[i].fpeaks[k] = detectorData.d[0].data[k][i]
                det[i].speaks[k] = detectorData.d[1].data[k][i]
                det[i].roi[k] = detectorData.d[2].data[k][i]

        for i in np.arange(detSize):
            det[i].NormT(ts)        # ("ts" = sampling time per data point t_s)

    ## call dead time correction later; should be performed only on
    ## good spectra ("goodPixels") as bad spectra can contain zeros which
    ## this function would divide by
    ## call is via function:  detDeadCorr(det, goodPixels)

    return e, trans, det


def getGoodPixels(det, detSize):
    """Check data from individual detector pixels for quality and
    remove any bad pixels from the list of pixels considered

    Returns:
    a 1-D array of "detSize" marking bad pixels with value "-2"
    """
    # define goodPixels array
    goodPixels = np.arange(detSize)

    # 	to start with, assume that all pixels (spectra) are good
    #  (list is complete; over time, elements of bad pixels will be set to -2 or -1;
    #	* where goodPixels is used, the list will be compressed
    #	  to remove the '-2' indices and thus permit easy
    # 	  looping via 'for i in goodPixels : [...]';
    #	* later in the code, we use '-1' to exclude spectra
    #	  following user interaction; the '-2's cannot be undone
    #	  while the '-1's can
    #	* ultimately, goodPixels will contian indices >0
    #     of spectra to be processed further and included in the
    #     weighted, corrected average of pixels)

    # ------------------------------------------------------------------------
    # test for bad pixels -- Step 1:
    #    all pixels that are defunct (average ROI <= 10 cts/sec) are excluded
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
    #    very high and very low TCR pixels
    # ------------------------------------------------------------------------
    #
    # above approach works well for defunct (low count rate) detector
    #	pixels, but it does not work for pixels that are just clocking up
    #	randomly high count rates
    # thus, out of now remaining GoodPixels,
    #	if TCR average of pixel > 3-times average TCR-average, then exclude
    #   the factor "3" is stored in "cutOffFactor = 3"; *** modify this if required ***
    #
    highCutOffFactor = 3
    lowCutOffFactor  = 0.05
    remainPixels = np.compress(goodPixels >= 0, goodPixels)
    tempTCRaverage = []
    for i in remainPixels:
        tempTCRaverage = np.append(tempTCRaverage, np.mean(det[i].fpeaks))

    badTCRpixels = np.where(
        tempTCRaverage > highCutOffFactor * np.mean(tempTCRaverage))
    goodPixels[remainPixels[badTCRpixels]] = -2
    excludeForeverPixels = np.append(excludeForeverPixels, badTCRpixels)
    print 'exclude forever (mark red): ', excludeForeverPixels

    badTCRpixels = np.where(
        tempTCRaverage < lowCutOffFactor * np.mean(tempTCRaverage))
    goodPixels[remainPixels[badTCRpixels]] = -2

    excludeForeverPixels = np.append(excludeForeverPixels, remainPixels[badTCRpixels])


    # ------------------------------------------------------------------------
    # test for bad pixels -- Step 4:
    #    SlowPeaks have zero values
    # ------------------------------------------------------------------------
    # problematic are also pixels that show Zeros in some of the SlowPeaks
    #   ("det.speaks") as they cause infinity values ("nan") when computing #
    #   detector dead time correction by using the ratio "FastPeaks/SlowPeaks";
    # thus, out of now remaining GoodPixels,
    #	if SlowPeaks = 0 anywhere, set value to +1
    #	(a spectrum could still be OK, even though there might be a zero
    #	 count in the background before the edge in low-TCR scenarios)
    #
    #
    for i in goodPixels :
        det[i].speaks[np.where(det[i].speaks == 0)] = 1


    #manually removed pixels (cheap hack to save time) -- 15/3/2015
    #alsoExcludePixels = np.asarray( [8,19, 89,98, 15,24,26,35] )
    #excludeForeverPixels = np.append(excludeForeverPixels, alsoExcludePixels )
    #goodPixels[ alsoExcludePixels ] = -2


    print 'exclude forever (mark red): ', excludeForeverPixels


    return goodPixels, excludeForeverPixels


def normaliseI0(det, goodPixels, i0):
    """Normalise the individual, dead-time corrected spectra ("roiCorr") to I0

    Returns: nothing  (all handled internally in the Class of "pixel" objects)
                      (generates new pixel object attribute "det[*].roiCorrNorm")

    """
    goodPixels = np.compress(goodPixels >= 0, goodPixels)
    for i in goodPixels:
        det[i].NormI0(i0)


def getWeightFactors(det, e, e0, goodPixels, TCRaverage, ROIaverage, weightType=None):
    """
    Run through all detector pixels and determine a weight factor
              (= edge-step / pre-edge-background-intensity)
    Returns: nothing but writes weight factors
             into detector pixel Class as attribute to each pixel

    """
    # goodPixels is designed to include index values <0 to mark bad pixels;
    #    thus, needs compressing out all indices <0 first before using in a loop
    goodPixels = np.compress(goodPixels >= 0, goodPixels)

    # also need an array to export later (for use by the GUI to display in pixel arrays)
    #   looks awkward here, but makes it cleaner in the GUI, because we can just call
    #   this function here with something like "self.weights = getWeightFactors(...)"
    #   and have one array returned into "self.weights"
    weights = np.zeros(len(det))

    # first, set all weight factors to zero (user/mouse events may access weight factors
    #   in the GUI, so need at least something)
    for i in range(len(det)):
        det[i].weightFactor = 0.0

    if weightType is not None :
        # use E0 + XXX eV to define start of fit range (depending on length of scan)
        #   end of fit range is simply end of scan (last index of "e")
        # use E0 - 10eV to do pre-edge fit in range [0 ; E0-10]eV
        e0Index = np.argmin(np.abs(e - e0))
        print 'E0 index = ', e0Index
        print 'E0 =', e0
        startIndexPre = 0
        stopIndexPre = np.argmin(np.abs(e - (e0 - 10)))
        if max(e)-e0 > 100 :
            startIndexPost = np.argmin(np.abs(e - (e0 + 50)))
        elif max(e)-e0 < 70 :
            startIndexPost = np.argmin(np.abs(e - (e0 + 15)))
        else :
            startIndexPost = np.argmin(np.abs(e - (e0 + 25)))
        startIndexK = np.argmin(np.abs(e - (e0 + 15)))
        stopIndexPost = len(e) - 1

        print 'start pre =', e[0]
        print 'stop pre =', e[stopIndexPre]
        print 'Emax - E0 =', max(e)-e0
        print 'start post = ', e[startIndexPost]
        print 'stop post  = ', e[stopIndexPost]

        ### determine individual weight factors and write into "weights" array
        m_e = 9.109381e-31  # kg
        hbar = 1.054572e-34  # Jsec = 6.582119e-16 eVsec
        ee = 1.602176e-19  # Asec , i.e., J/eV
        x = e[startIndexPost:stopIndexPost]    # E' for region above edge
        k = np.sqrt(2 * m_e * (x - e0) * ee) / hbar * 1e-10     # k in A^-1 for
                                                                # the postEdge region
        # The following is a bit of a cheap hack; we need to make "k" available to the GUI;
        # here we use the first detector Pixel Object as a vessel to transport "k" from this
        # module to the GUI "sakura[...].py"; this is not elegant, but it works
        det[0].k = k
        for i in goodPixels:
            yPost = np.ndarray.flatten(det[i].roiCorrNorm[startIndexPost:
                                       stopIndexPost])  # mu(E') above edge
            fitparams = polyfit(x, yPost, 2)
            postEdgeCurve = polyval(fitparams, e)

            # now fit the pre-edge (here linear fit)
            yPre = np.ndarray.flatten(det[i].roiCorrNorm[startIndexPre:stopIndexPre])
            fitparams = polyfit(e[startIndexPre:stopIndexPre], yPre, 1)
            preEdgeCurve = polyval(fitparams, e)
            #preEdgeAverage = np.mean( det[i].roiCorr[startIndexPre:stopIndexPre] )
            #w = ( postEdgeCurve[e0Index] - preEdgeAverage ) / preEdgeAverage
            w = (postEdgeCurve[e0Index] - preEdgeCurve[e0Index]) / \
                preEdgeCurve[e0Index]

            weights[i] = w
            det[i].postEdgeCurve = postEdgeCurve
            det[i].preEdgeCurve = preEdgeCurve

            # while we have the fit in memory, extract something like "chi(k)" and
            #    write into detector Pixel Objects for use in the GUI
            postE = postEdgeCurve[startIndexPost:stopIndexPost]
                # fit(E') only above edge
            det[i].chi = (yPost - postE) / (postE)
            # use weighting with "w" to get consistent y-scale

        # normalise weight factors to 1 (makes output ROI and TCR values less arbitrary)
        # First replace any infs with max value in remainder of array

    # weightType can be integer 0, 1, or 2  [see user GUI "Weight Factor RadioBox"
    #   0 = "Edge Step"
    #   1 = "TCR"
    #   2 = " =1 "
    #
    #  "Edge Step" was already calculated, so assume it is this option and
    #    go into the if-elif statement on that assumption
    #
    if weightType == 1 :
        weights = TCRaverage
        nanmask = np.isnan(weights)
        weights[nanmask] = 0
        print "TCR"
    elif weightType == 2 :
        weights[:] = 1
        print "=1"
    elif weightType is None :
        weights[:] = 1
        print "none"

    # normalise weight factors to maximum=1
    infmask = np.isinf(weights)
    weights[infmask] = np.nanmax(weights[~infmask])
    weights = weights / np.nanmax(weights)
    
    # append weight factors as attributes to detector Pixels Objects
    for i in goodPixels:        
        det[i].weightFactor = weights[i]
    
    return weights ####, preEdgeCurve, postEdgeCurve


def applyWeights(det, goodPixels):
    """Apply weight factors to the individual spectra

    Returns: nothing  (handled in "pixel" objects)
                      (generates new pixel object attribute "det[*].weightedSpec")

    """
    goodPixels = np.compress(goodPixels >= 0, goodPixels)
    for i in goodPixels:
        det[i].WeightSpectrum()


def pearsonr(x, y):
    """
    Calculates a Pearson correlation coefficient and the p-value for testing
    non-correlation.

    This is scipy's pearsonr function with the 2-tailed p-value return-value removed

    The Pearson correlation coefficient measures the linear relationship
    between two datasets. Strictly speaking, Pearson's correlation requires
    that each dataset be normally distributed. Like other correlation
    coefficients, this one varies between -1 and +1 with 0 implying no
    correlation. Correlations of -1 or +1 imply an exact linear
    relationship. Positive correlations imply that as x increases, so does
    y. Negative correlations imply that as x increases, y decreases.

    The p-value roughly indicates the probability of an uncorrelated system
    producing datasets that have a Pearson correlation at least as extreme
    as the one computed from these datasets. The p-values are not entirely
    reliable but are probably reasonable for datasets larger than 500 or so.

    Parameters
    ----------
    x : (N,) array_like
        Input
    y : (N,) array_like
        Input

    Returns
    -------
    Pearson's correlation coefficient

    References
    ----------
    http://www.statsoft.com/textbook/glosp.html#Pearson%20Correlation

    """
    # x and y should have same length.
    x = np.asarray(x)
    y = np.asarray(y)
    n = len(x)
    mx = x.mean()
    my = y.mean()
    xm, ym = x-mx, y-my
    r_num = n*(np.add.reduce(xm*ym))
    ss = lambda x: np.dot(x, x)
    r_den = n*np.sqrt(ss(xm)*ss(ym))
    r = (r_num / r_den)

    # Presumably, if abs(r) > 1, then it is only some small artifact of floating
    # point arithmetic.
    r = max(min(r, 1.0), -1.0)

    return r


def getCorrels(det, goodPixels):
    """Compute spectra correlation coefficients (using Pearsons Correlation)

    Returns: array "correls" of size "detSize", containing average correlation
            coefficient of pixel i with all other good pixels {0...i-1, i+1... n}

    """
    # goodPixels is designed to include index values <0 to mark bad pixels;
    #    thus, needs compressing out all indices <0 first before using in a loop
    goodPixels = np.compress(goodPixels >= 0, goodPixels)

    correls = np.zeros(len(det))
    for i in goodPixels:
        for j in goodPixels:
            correls[i] += pearsonr(det[i].roi, det[j].roi)

    correls = correls / len(det)

    return correls


def getE0(e):
    """Estimate which edge position (E0) might be most adequate

    Returns: e0

    """
    # use simple approach:
    #   E0 is within the first 300 eV of the scan;
    #   if scan shorter than 500 eV, then E0 is within half the scan range

    eMin = min(e)
    scanRange = max(e) - eMin
    if scanRange < 500:
        eMax = eMin + scanRange / 2.0
    else:
        eMax = eMin + 300

    # from etab.edgeEnergy dict find all keys (elements) that have edges
    #   between eMin and eMax
    # also get the corresponding shells (only K, L1,2,3 as in etab.QNTransition
    elements = []
    shells = []
    edgeEnergies = []
    for k in etab.edgeEnergy.keys():
        energyList = np.asarray(etab.edgeEnergy[k])
        for j in range(len(energyList)):
            if energyList[j] > eMin and energyList[j] < eMax and j < 4:
                elements.append(k)          # store dict keys (element names) in list
                shells.append(etab.QNTransition[j])
                                # get corresponding shell and put into list
                edgeEnergies.append(energyList[j])     # append corresponding edge energy
                print 'edge: ', energyList[j], k, etab.QNTransition[j]
    # concatenate findings into 2D array:
    result = [elements, shells, edgeEnergies]

    # give preference to K, then L3, L2, L1 edges if more than one edge candidate found
    #
    #  sort by shells (K, L1/2/3) and get indices of items before sort;
    #  then reverse (L3/2/1, K)
    #  and sort all three subarrays (elements, shells, edgeEnergies) accordingly
    sortIndices = sorted(range(len(result[1])), key=lambda x: result[1][x])
    sortIndices.reverse()
    for j in range(len(result)) :                     ## result is a list containing 3 lists; len(result) is 3
        result[j] = [result[j][i] for i in sortIndices]
        
    # take the list items that correspond to 'K' shells and put them up the front
    #     this gives order K -> L3 -> L2 -> L1
    where_k = np.where(np.asarray(result[1]) == 'K')[0]
    for i in where_k :
        result[0].insert( 0,result[0].pop() )
        result[1].insert( 0,result[1].pop() )
        result[2].insert( 0,result[2].pop() )
    
    print result
    
    
    ##temp = []     # empty array
    ##for i in range(len(result)):    # loop over subarrays;
    ##    for j in sortIndices:       # in each subarray, loop over items in order of sorted indices
    ##        temp.append(result[i][j])   # extract item using sort index and append to temporary list
    ##    result[i] = temp            # overwrite subarray with subarray sorted according to "shells"
    ##    temp = []
    ##        # empty out temp for next iteration in loop 'i'


    return result


def getAverage(goodPixels, det):
    """Compute the average of all weighted, deadtime corrected spectra
    from det[i].weightedSpec ( which is = det[i].roiCorr * det[i].weightFactor)

    This creates class attributes "self.averageMu" "[...]Chi"

    """
    # goodPixels is designed to include index values <0 to mark bad pixels;
    #    thus, needs compressing out all indices <0 first before using in a loop
    goodPixels = np.compress(goodPixels >= 0, goodPixels)
    scanSize = len(det[0].fpeaks)   # choose a random pixel array to determine scan length
    averageMu = np.zeros(scanSize)
    averageChi = np.zeros(len(det[goodPixels[0]].chi))
    for i in goodPixels:
        averageMu = averageMu + det[i].weightedSpec
        averageChi = averageChi + det[i].chi
    averageMu = averageMu / len(goodPixels)
    averageChi = averageChi / len(goodPixels)

    return averageMu, averageChi


def writePvBlock(extra_pvs):
    """returns a multi-line string containing important PVs
    to be written to the output ASCII file.

    """
    # Block Header
    s = dedent("""\
        #
        # Process Variables:
        # ------------------
        #
        """)
    pvNames = ['mca1.R0LO', 'mca1.R0HI']

    for pv in pvNames:
        try:
            s += '# {}: {}\n'.format(pv, extra_pvs[pv])
        except:
            pass

    return s

def writeAverages(results, reader_type, detSize):
    """Produces an output file containing averaged data and meta-information
    and writes this file to disk.

    Arguments:
    results - Results() class instance
    reader_type - String representing current reader module in use: 'gnc' or 'gmda'
    detSize - number of detector pixels

    """
    mdaOutName = results.fname
    goodPixels = results.goodPixels
    correls = results.correls
    e = results.e
    trans = results.trans
    weights = results.weights
    averageMu = results.averageMu
    extra_pvs = results.extra_pvs

    print ''
    print 'checksum: ',np.average(averageMu)


    ## make a 10-at-a-time iterator; see examples in Python itertools documentation
    ### ten_of = lambda x: izip(*[chain(x, repeat(None, 9))]*10)

    # make an iterator to describe the detector array;
    #   assume "rectangular shape" and backfill with "None" where there are not enough pixels;
    #   e.g. if the detector is a detSize=26 element detector, then generate a 5x6 array
    #        with the last row containing 1 value and four values reading "None"
    # note that "numCol" needs to be integer for the iterable to work
    numCols = int(np.round(np.sqrt(detSize)))
    nPix_of = lambda x: izip(*[chain(x, repeat(None, (numCols-1) ))]*numCols)
    
    asciiFilename = mdaOutName.replace('.mda', '.asc')
    try:
        open(asciiFilename, 'r')
        file_exists = True
    except IOError:
        file_exists = False
    if file_exists:
        message = os.path.basename(asciiFilename) + ' exists, overwrite?'
        md = wx.MessageDialog(parent=None, message=message,
            caption='Attention', style=wx.YES_NO | wx.NO_DEFAULT | wx.ICON_QUESTION)
        result = md.ShowModal()
        if result == wx.ID_NO:
            return

    with open(asciiFilename, 'w') as f:
        # Header
        timestamp = time.asctime(time.localtime())
        print >>f, dedent("""\
            #
            # SAKURA {version} output
            #
            # Generated on {timestamp}
            # MDA file processed: {mdaOutName}
            #\
            """.format(
                mdaOutName=mdaOutName,
                timestamp=timestamp,
                version=version.__version__))

        # write matrix of "goodPixels"; replace "-1" and "-2" with "--"
        print >>f, dedent("""\
            #
            # Detector pixels used (reads "--" if excluded):
            # ----------------------------------------------
            #\
            """)
        
        output = ['{:02d}'.format(i) if i > 0 else '--' for i in goodPixels+1]
        for items in nPix_of(output):
            print >>f, '#',
            print >>f, ' '.join(items)
        
        # write matrix of correlation coefficients
        print >>f, dedent("""\
            #
            #
            # Correlation coefficients (%):
            # -----------------------------
            #\
            """)
        output = ['{:>6.2f}'.format(i*100) for i in correls]
        for items in nPix_of(output):
            print >>f, '#',
            print >>f, '  '.join(items)
        
        # write matrix of weight factors
        print >>f, dedent("""\
            #
            #
            # Weight Factors (%):
            # -------------------
            #\
            """)
        output = ['{:>6.2f}'.format(i*100) for i in weights]
        for items in nPix_of(output):
            print >>f, '#',
            print >>f, '  '.join(items)
        
        print >>f, '#'
        
        # Write PVs of interest
        if extra_pvs != {}:
            s = writePvBlock(extra_pvs)
            print >>f, s,

        # Write other notes here
        if reader_type == 'gnc':
            # Write current ROIs if a mapping mode dataset
            print >>f, dedent("""\
                #
                #
                # ROI values:
                # -----------
                #
                # roi_low:  {roi_low}
                # roi_high: {roi_high}
                #\
                """.format(
                    roi_low=results.det.roi_low,
                    roi_high=results.det.roi_high
                    ))

        # write data
        #   multiply  averageMu  by scaling factor 100 to increase accuracy (otherwise, typical result = 0.000xxxx,
        #   which some programs like VIPER/XANDA have difficulties reading in with full number of digits
        print >>f, '#'
        output = np.vstack((e, averageMu * 100, trans[1:])).T
        print >>f, '# E[eV]    mu(E)_fluo_average[a.u.]    I0[cts/sec]    I1[cts/sec]' + \
                     '    I2[cts/sec]    sample_time[sec]    encoder_Bragg_angle[deg]'
        np.savetxt(f, output, fmt='%14.6f %14.6f %14.6f %14.6f %14.6f %4.1f %14.6f')
        #    header = 'E[eV]    mu(E)_fluo_average[a.u.]    I0[cts/sec]    I1[cts/sec]' + \
        #             '    I2[cts/sec]    sample_time[sec]    encoder_Bragg_angle[deg]')
        print '... data saved.'

        message = os.path.basename(asciiFilename) + ' written'
        md = wx.MessageDialog(parent=None, message=message,
            caption='File saved', style=wx.OK)
        md.ShowModal()





def notepad_gmda():
    """notepad to develop and brainstorm code; not a callable function
    """

    e = data[0] * 1000.0
    trans = data[1]
    det = data[2]
    mu = det[0].roiCorr

    iff.put_array("my.energy, e")
    iff.put_array("my.mu, mu")

    print iff.ifeffit("spline(my.energy, my.mu, rbkg=1, kmin=0)")
    k = iff.get_array("k")
    chi = iff.get_array("chi")
    bkg = iff.get_array("bkg")
    de = iff.get_scalar("edge_step")

    execfile('get_mda2.py')
    det = data[2]
    trans = data[1]
    e = data[0] * 1000.0
    iff.put_array("my.e", e)

    goodPixs = getGoodPixels()

    iff.ifeffit("&screen_echo=0")
    k = doSplines(det, goodPixs)

    getWeights(det, goodPixs)

    applyWeights(det, goodPixs)

##
## ==== MAIN ====
##
if __name__ == '__main__':

    #iff = Ifeffit.Ifeffit()
    fname = 'SR12ID01H18879.mda'
#    command = ''.join(['mda2ascii -1 ',fname])
    ##os.system(command)

#    ascfname = fname.split('.mda')[0] + '.asc'

#    print ascfname
#    data = getData(ascfname)        #"data" is received as a numpy array

#    pass
