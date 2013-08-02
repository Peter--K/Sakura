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

from scipy import polyfit
from scipy import polyval
from scipy.stats.stats import pearsonr

import edge_tables as etab

## import pylab as pl

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

    def GetDead(self, fpeaks, speaks):
        """get detector dead time parameter 'tau' """
        self.tau = fpeaks / speaks

    def DeadCorr(self, tau, roi):
        """apply dead time parameter"""
        self.roiCorr = roi * tau

    def NormI0(self, I0):
        """normalise data to incoming intensity (I0)"""
        self.roiCorrNorm = self.roiCorr / I0

    def WeightSpectrum(self):
        """apply weight factor which was derived from relative edge step"""
        self.weightedSpec = self.weightFactor * self.roiCorr


def makeDet(detSize, scanSize):
    """Combines 100 pixels into one multi-element detector.

    Returns:
    a list of size "detSize" (e.g., 100) "Pixel" objects

    """
    det = [pixel(i) for i in np.arange(detSize)]
    for j in np.arange(detSize):
        det[j].CreateArrays(scanSize)
    return det


def detDeadCorr(det, goodPixels):
    """Correct dead time ("tau") for each detector pixel

    """
    goodPixels = np.compress(goodPixels >= 0, goodPixels)
    for i in goodPixels:
        det[i].GetDead(det[i].fpeaks, det[i].speaks)
        det[i].DeadCorr(det[i].tau, det[i].roi)


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
    mda = readMDA.readMDA(fname, verbose=False)
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

    ts = trans[pvColumnNames.index('scaler1.T')]    # get the sample time
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
    #	pixels, but it does not work for pixels that are just clocking up
    #	randomly high count rates
    # thus, out of now remaining GoodPixels,
    #	if TCR average of pixel > 3-times average TCR-average, then exclude
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
    #	if SlowPeaks = 0 anywhere, set value to +1
    #	(a spectrum could still be OK, even though there might be a zero
    #	 count in the background before the edge in low-TCR scenarios)
    #
    #
    for i in goodPixels:
        det[i].speaks[np.where(det[i].speaks == 0)] = 1

    return goodPixels, excludeForeverPixels


def normaliseI0(det, goodPixels, i0):
    """Normalise the individual, dead-time corrected spectra ("roiCorr") to I0

    Returns: nothing  (all handled internally in the Class of "pixel" objects)
                      (generates new pixel object attribute "det[*].roiCorrNorm")

    """
    goodPixels = np.compress(goodPixels >= 0, goodPixels)
    for i in goodPixels:
        det[i].NormI0(i0)


def getWeightFactors(det, e, e0, goodPixels):
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

    # use E0 + XXX eV to define start of fit range (depending on length of scan)
    #   end of fit range is simply end of scan (last index of "e")
    # use E0 - 10eV to do pre-edge fit in range [0 ; E0-10]eV
    e0Index = np.argmin(np.abs(e - e0))
    print 'E0 index = ', e0Index
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

    print 'E - E0 =', max(e)-e0    
    print 'start post = ', e[startIndexPost]
    print 'stop post  = ', e[stopIndexPost]
    
    # first, set all weight factors to zero (user/mouse events may access weight factors
    #   in the GUI, so need at least something)
    for i in range(len(det)):
        det[i].weightFactor = 0

    # determine individual weight factors and write into "weights" array
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
        yPost = np.ndarray.flatten(det[i].roiCorr[startIndexPost:
                                   stopIndexPost])  # mu(E') above edge
        fitparams = polyfit(x, yPost, 2)
        postEdgeCurve = polyval(fitparams, e)

        # now fit the pre-edge using same algorithm
        yPre = np.ndarray.flatten(det[i].roiCorr[startIndexPre:stopIndexPre])
        fitparams = polyfit(e[startIndexPre:stopIndexPre], yPre, 2)
        preEdgeCurve = polyval(fitparams, e)
        #preEdgeAverage = np.mean( det[i].roiCorr[startIndexPre:stopIndexPre] )
        #w = ( postEdgeCurve[e0Index] - preEdgeAverage ) / preEdgeAverage
        w = (postEdgeCurve[e0Index] - preEdgeCurve[e0Index]) / \
            preEdgeCurve[e0Index]
        weights[i] = w

        # while we have the fit in memory, extract something like "chi(k)" and
        #    write into detector Pixel Objects for use in the GUI
        postE = postEdgeCurve[startIndexPost:stopIndexPost]
            # fit(E') only above edge
        det[i].chi = (yPost - postE) / (postE)
        # use weighting with "w" to get consistent y-scale

    # normalise weight factors to 1 (makes output ROI and TCR values less arbitrary)
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
            correls[i] = correls[i] + pearsonr(det[i].roi, det[j].roi)[0]
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
                elements.append(k)
                                # store dict keys (element names) in list
                shells.append(etab.QNTransition[j])
                                # get corresponding shell and put into list
                edgeEnergies.append(energyList[j])     # append corresponding edge energy
                print 'edge: ', energyList[j], k, etab.QNTransition[j]
    # concatenate findings into 2D array:
    result = [elements, shells, edgeEnergies]

    # give preference to K, then L3, L2, L1 edges if more than one edge candidate found
    #
    #  sort by shells (K, L1/2/3) and get indices of items before sort;
    #  then sort all three subarrays (elements, shells, edgeEnergies) accordingly
    sortIndices = sorted(range(len(result[1])), key=lambda x: result[1][x])
    temp = []     # empty array
    for i in range(len(result)):    # loop over subarrays;
        for j in sortIndices:       # in each subarray, loop over items in order of sorted indices
            temp.append(result[i][j])   # extract item using sort index and append to temporary list
        result[i] = temp            # overwrite subarray with subarray sorted according to "shells"
        temp = []
            # empty out temp for next iteration in loop 'i'

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


def writeDataBlock(f, output, numFormat):
    """Write a 2D-array of floats as 2D-array of strings into a file

    Input arguments:
    f - file handle
    output - 2D-array to convert
    numFormat - float format

    """
    for i in range(len(output)):
        f.write('# ')
        f.write(output[i])
        f.write(' \n')


def writeAverages(mdaOutName, goodPixels, correls,
                  k, e, trans, weights, averageMu, averageChi):
    """Produces an output file containing averaged data and meta-information
    and writes this file to disk.

    """
    f = open(mdaOutName.split('.mda')[0] + '.asc', 'w')

    f.write('# \n')
    f.write('#  SAKURA output \n')
    f.write('# \n')
    f.write('# \n')
    f.write('# MDA file processed: ' + mdaOutName + '\n')
    f.write('# \n')

    # write matrix of "goodPixels" to file; replace "-1" and "-2" with "--"
    f.write('# \n')
    f.write('# \n')
    f.write('# Detector pixels used (reads "--" if excluded): \n')
    f.write('# ---------------------------------------------- \n')
    f.write('# \n')
    indices = np.where(goodPixels < 0)
    output = np.asarray(goodPixels, dtype='string')
    output[indices] = '--'
    output = np.reshape(output, (10, 10))
    for i in range(len(output)):
        f.write('# ')
        f.write(output[i])
        f.write(' \n')

    # write matrix of correlation coefficients to file
    f.write('# \n')
    f.write('# \n')
    f.write('# Correlation coefficients: \n')
    f.write('# ------------------------- \n')
    f.write('# \n')
    output = np.reshape(correls, (10, 10))
    for i in range(len(output)):
        f.write('# ')
        for j in range(len(output[i])):
            f.write(('{:.2%}  ').format(output[i][j]))
        f.write('\n')
    f.write('# \n')

    # write matrix of weight factors to file
    f.write('# \n')
    f.write('# \n')
    f.write('# Weight Factors: \n')
    f.write('# --------------- \n')
    f.write('# \n')
    output = np.reshape(weights, (10, 10))
    for i in range(len(output)):
        f.write('# ')
        for j in range(len(output[i])):
            f.write(('{:.2%}  ').format(output[i][j]))
        f.write('\n')
    f.write('# \n')

    # write data to file
    f.write('# \n')
    f.write('# Data: \n')
    f.write('# ----- \n')
    f.write('# \n')
    f.write('# E[eV]    mu(E)_fluo_average/I0[a.u.]    I0[cts/sec]    I1[cts/sec]    ' +
              'I2[cts/sec]    sample_time[sec]    encoder_Bragg_angle[deg] \n')

    output = []
    output = np.append(e, averageMu)
    output = np.append(
        output, trans[1:])   # energy axis already used (e = trans[0])
    output = np.reshape(output, (len(e), -1), order='F')
            # "-1" means that np.reshape determines second dimension itself
    output = np.asarray(output, dtype='string')

    outYDim = np.shape(output)[1]
    for i in range(len(output)):
        for j in range(outYDim):
            f.write(output[i][j])
            f.write('    ')
        f.write(' \n')

    f.close
    print '... data saved.'


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
