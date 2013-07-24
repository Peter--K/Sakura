# -----------------------------------------------------------------------------
#
#   SAKURA,
#      a toolkit to process and average multi-element fluorescence data
#      (currently built for the XAS Beamline at Synchrotron Light Source Australia)
#
# -----------------------------------------------------------------------------
#                       {Peter Kappen, XAS Beamline;
#                        Gary Ruben,
#                                   Synchrotron Light Source Australia, 2013}
#


# -*- coding: utf-8 -*-

###########################################################################
## Python code generated with wxFormBuilder (version Sep  8 2010)
## http://www.wxformbuilder.org/
##
###########################################################################

import os

import wx
import wx.lib.plot as plot

import numpy as np
from matplotlib import cm

import get_mda as gmda
import edge_tables as etab
import get_netcdf as gnc
import readMDA


class Results(object):
    """An empty container to hold averaged data; used to store
    data while processing multiple files and to be filled in the
    Class MainFrame with data from averaging scans.

    """
    def __init__(self):
        print " instance of 'results'-object created..."


class MainFrame(wx.Frame):
    def __init__(self, parent):
        # -----------------------------------------------------------
        # Main GUI creation
        # -----------------------------------------------------------
        # build widget/GUI architecture using sizers
        wx.Frame.__init__(self, parent, id=wx.ID_ANY,
                          title=u"-- SAKURA --", pos=wx.DefaultPosition,
                          size=wx.Size(1250, 780),
                          ##size = wx.Size( 2000,1200 ),
                          style=wx.HSCROLL | wx.VSCROLL | wx.TAB_TRAVERSAL |
                                wx.DEFAULT_FRAME_STYLE |
                                wx.FULL_REPAINT_ON_RESIZE )

        self.SetSizeHintsSz(wx.DefaultSize, wx.DefaultSize)

        # Main window BoxSizer (fills entire frame)
        bSizer_Main = wx.BoxSizer(wx.HORIZONTAL)
        bSizer_Main.SetMinSize(wx.Size(1250, 780))

        # Controls BoxSizers (open, close, detector, etc)
        self.bSizer_Controls = wx.BoxSizer(wx.VERTICAL)
        bSizer_Controls1 = wx.BoxSizer(wx.HORIZONTAL)
        bSizer_Controls11 = wx.BoxSizer(wx.VERTICAL)
        bSizer_Controls11.SetMinSize(wx.Size(100, -1))
        self.m_button_Load = wx.Button(
            self, wx.ID_ANY, u"Load", wx.DefaultPosition, wx.DefaultSize, 0)
        bSizer_Controls11.Add(
            self.m_button_Load, 0, wx.ALL | wx.ALIGN_CENTER_HORIZONTAL, 5)

        self.m_button_Save = wx.Button(
            self, wx.ID_ANY, u"Save", wx.DefaultPosition, wx.DefaultSize, 0)
        bSizer_Controls11.Add(
            self.m_button_Save, 0, wx.ALL | wx.ALIGN_CENTER_HORIZONTAL, 5)

        #self.m_button_SaveAll = wx.Button( self, wx.ID_ANY, u"Save All",
        #                        wx.DefaultPosition, wx.DefaultSize, 0 )
        #bSizer_Controls11.Add( self.m_button_SaveAll, 0,
        #                       wx.ALIGN_CENTER_HORIZONTAL|wx.ALL, 5 )

        self.m_button_Unload = wx.Button(
            self, wx.ID_ANY, u"Unload", wx.DefaultPosition, wx.DefaultSize, 0)
        bSizer_Controls11.Add(
            self.m_button_Unload, 0, wx.ALL | wx.ALIGN_CENTER_HORIZONTAL, 5)

        self.m_staticline11 = wx.StaticLine(self, wx.ID_ANY, wx.DefaultPosition,
                                            wx.DefaultSize, wx.LI_HORIZONTAL)
        bSizer_Controls11.Add(self.m_staticline11, 0, wx.EXPAND | wx.ALL, 5)

        self.m_button_Exit = wx.Button(
            self, wx.ID_ANY, u"Exit", wx.DefaultPosition, wx.DefaultSize, 0)
        bSizer_Controls11.Add(self.m_button_Exit, 0, wx.ALL |
                              wx.RIGHT | wx.ALIGN_CENTER_HORIZONTAL, 5)

        bSizer_Controls1.Add(bSizer_Controls11, 0, 0, 5)
        bSizer_Controls12 = wx.BoxSizer(wx.HORIZONTAL)

        self.m_staticline12 = wx.StaticLine(self, wx.ID_ANY, wx.DefaultPosition,
                                            wx.Size(2, -1), wx.LI_HORIZONTAL)
        bSizer_Controls12.Add(
            self.m_staticline12, 0, wx.EXPAND | wx.TOP | wx.BOTTOM, 5)

        ##m_listBox_SpectraChoices = [ 'file' ]
        ##self.m_listBox_Spectra = wx.ListBox( self, wx.ID_ANY, wx.DefaultPosition,
        #   wx.Size( 100,100 ), m_listBox_SpectraChoices, wx.LB_EXTENDED|wx.LB_NEEDED_SB )
        ##bSizer_Controls12.Add( self.m_listBox_Spectra, 0, wx.ALL, 5 )

        m_checkList_SpectraChoices = ['file']
        self.m_checkList_Spectra = wx.CheckListBox(self, wx.ID_ANY, wx.DefaultPosition,
            wx.DefaultSize, m_checkList_SpectraChoices, 0)
        bSizer_Controls12.Add(self.m_checkList_Spectra, 0, wx.ALL, 5)

        m_listBox_EdgeChoices = etab.edgesAvailable
        self.m_listBox_Edge = wx.ListBox(self, wx.ID_ANY, wx.DefaultPosition,
            wx.Size(-1, -1), m_listBox_EdgeChoices, wx.LB_NEEDED_SB | wx.LB_SINGLE)
        bSizer_Controls12.Add(self.m_listBox_Edge, 0, wx.ALL, 5)
        bSizer_Controls1.Add(bSizer_Controls12, 0, 0, 5)
        self.bSizer_Controls.Add(bSizer_Controls1, 0, 0, 5)

        # this BoxSizer contains the detector panels and their options;
        #   unlike other sizers, make this an attribute to the MainFrame class
        #   in order to manipulate it later;
        # reason: we want to disable the Sizer (it is mouse-over sensitive)
        #   before it is loaded up with data
        self.sbSizer6 = wx.StaticBoxSizer(wx.StaticBox(
            self, wx.ID_ANY, u"Fluorescence Detector"), wx.VERTICAL)


        # first detector panel
        gSizer_Det1 = wx.GridSizer(10, 10, 0, 0)
        # TODO: find a way to get detSize here (hasn't been defined in this Class, yet)
        self.pixel_ids1 = np.zeros(100, dtype=int)
        for i in range(100):
            ID_PIXEL = wx.NewId()
            self.pixel_ids1[i] = ID_PIXEL
            self.label = wx.StaticText(
                self, ID_PIXEL, label=str(i + 1), size=(22, 22),
                style=wx.ALIGN_CENTRE | wx.ST_NO_AUTORESIZE)
            #self.label.SetBackgroundColour('grey')
            gSizer_Det1.Add(self.label, 0, wx.ALIGN_CENTER | wx.ALL, 1)

            # Connect static texts (=detector pixels) to events
            self.label.Bind(wx.EVT_RIGHT_DOWN, self.OnRightDownPixel)
            self.label.Bind(wx.EVT_LEFT_DOWN, self.OnLeftDownPixel)
            self.label.Bind(wx.EVT_ENTER_WINDOW, self.OnEnterPixel)
            self.label.Bind(wx.EVT_LEAVE_WINDOW, self.OnLeavePixel)

        self.sbSizer6.Add(gSizer_Det1, 0, wx.SHAPED, 0)


        # divider line between detector panels
        self.m_staticline2 = wx.StaticLine(self, wx.ID_ANY, wx.DefaultPosition,
                                           wx.DefaultSize, wx.LI_HORIZONTAL)
        self.sbSizer6.Add(self.m_staticline2, 0, wx.EXPAND | wx.ALL, 5)


        # second detector panel
        gSizer_Det2 = wx.GridSizer(10, 10, 0, 0)
        # TODO: find a way to get detSize here (hasn't been defined in this Class, yet)
        self.pixel_ids2 = np.zeros(100, dtype=int)
        for i in range(100):
            ID_PIXEL = wx.NewId()
            self.pixel_ids2[i] = ID_PIXEL
            self.label = wx.StaticText(
                self, ID_PIXEL, label=str(i + 1), size=(22, 22),
                style=wx.ALIGN_CENTRE | wx.ST_NO_AUTORESIZE)
            gSizer_Det2.Add(self.label, 0, wx.ALIGN_CENTER | wx.ALL, 1)

            # Connect static texts(=detector pixels) to events
            self.label.Bind(wx.EVT_LEFT_DOWN, self.OnLeftDownPixel)
            self.label.Bind(wx.EVT_RIGHT_DOWN, self.OnRightDownPixel)
            self.label.Bind(wx.EVT_ENTER_WINDOW, self.OnEnterPixel)
            self.label.Bind(wx.EVT_LEAVE_WINDOW, self.OnLeavePixel)

        self.sbSizer6.Add(gSizer_Det2, 0, wx.SHAPED, 0)
        # END of BoxSizer ------


        # add radio buttons to Det2Control BoxSizer,
        #    add Det2Control sizer to sBoxSizer6
        bSizer_Det2Control = wx.BoxSizer(wx.HORIZONTAL)

        self.m_radioBtn_Correl = wx.RadioButton(self, wx.ID_ANY, u"Correlation",
            wx.DefaultPosition, wx.DefaultSize, wx.RB_GROUP)
        bSizer_Det2Control.Add(self.m_radioBtn_Correl, 0, wx.ALL, 5)

        self.m_radioBtn_Weights = wx.RadioButton(self, wx.ID_ANY, u"Weights",
            wx.DefaultPosition, wx.DefaultSize, 0)
        bSizer_Det2Control.Add(self.m_radioBtn_Weights, 0, wx.ALL, 5)

        self.m_radioBtn_DetInt = wx.RadioButton(self, wx.ID_ANY, u"TCR (averaged)",
            wx.DefaultPosition, wx.DefaultSize, 0)
        bSizer_Det2Control.Add(self.m_radioBtn_DetInt, 0, wx.ALL, 5)

        self.sbSizer6.Add(bSizer_Det2Control, 1, wx.EXPAND, 5)
        # END of radio buttons ----


        # add Fluorescence Detector Static Box Sizer to Controls Box Sizer
        self.bSizer_Controls.Add(self.sbSizer6, 0, 0, 5)


        # add Controls Box Sizer to Main
        bSizer_Main.Add(self.bSizer_Controls, 0, wx.EXPAND, 5)
        bSizer_Display = wx.BoxSizer(wx.VERTICAL)
        sbSizer5 = wx.StaticBoxSizer(
            wx.StaticBox(self, wx.ID_ANY, u"Averaged XAS"), wx.VERTICAL)
        bSizer_Avgs = wx.BoxSizer(wx.HORIZONTAL)
        self.m_panelMuAverage = wx.Panel(self, wx.ID_ANY, wx.DefaultPosition,
                                         wx.Size(-1, -1), wx.TAB_TRAVERSAL)
        self.m_panelMuAverage.SetMinSize(wx.Size(-1, 300))
        bSizer_Avgs.Add(self.m_panelMuAverage, 1, wx.ALL, 5)
        self.m_panelChiAverage = wx.Panel(self, wx.ID_ANY, wx.DefaultPosition,
                                          wx.DefaultSize, wx.TAB_TRAVERSAL)
        self.m_panelChiAverage.SetMinSize(wx.Size(-1, 300))
        bSizer_Avgs.Add(self.m_panelChiAverage, 1, wx.ALL, 5)


        # add Box Sizer with average spectrum (mu(E) and chi(k) to top row (sizer) )
        sbSizer5.Add(bSizer_Avgs, 0, wx.EXPAND, 0)


        # add top row Box Sizer to Display Box Sizer
        bSizer_Display.Add(sbSizer5, 0, wx.EXPAND, 0)


        # generate second box sizer for Display Box Sizer (this one for single spectra)
        sbSizer_Singles = wx.StaticBoxSizer(wx.StaticBox(self, wx.ID_ANY,
                                                         u"Selected detector channels"),
                                            wx.HORIZONTAL)


        # toggle button to choose between mu(E) and chi(k)
        bSizer_SglsButtons = wx.BoxSizer(wx.VERTICAL)
        #self.m_spinCtrl_SpecSelect = wx.SpinCtrl( self, wx.ID_ANY, wx.EmptyString,
        #    wx.DefaultPosition, wx.Size( 50,30 ), wx.SP_ARROW_KEYS, 0, 100, 0 )
        #bSizer_SglsButtons.Add( self.m_spinCtrl_SpecSelect, 0, wx.ALL, 5 )
        #self.m_buttonMu = wx.Button( self, wx.ID_ANY, u"Mu(E)", wx.DefaultPosition,
        #    wx.Size( 50, -1 ), 0 )
        #bSizer_SglsButtons.Add( self.m_buttonMu, 0, wx.BOTTOM|wx.TOP, 5 )
        #self.m_buttonChi = wx.Button( self, wx.ID_ANY, u"Chi(k)", wx.DefaultPosition,
        #    wx.Size( 50, -1 ), 0 )
        #bSizer_SglsButtons.Add( self.m_buttonChi, 0, wx.BOTTOM|wx.TOP, 5 )
        self.m_toggleBtn_MuChi = wx.ToggleButton(
            self, wx.ID_ANY, u"chi(k)", wx.DefaultPosition, wx.DefaultSize, 0)
        bSizer_SglsButtons.Add(self.m_toggleBtn_MuChi, 0, wx.ALL, 5)
        sbSizer_Singles.Add(bSizer_SglsButtons, 0, wx.ALIGN_BOTTOM, 5)


        # add 2 panels to display spectra from individual detector channels
        #   (there might be a need to add more panels later, thus this "clumsy"
        #    loop to generage 2 panels; this to keep flexibility)
        gSizer_SglsSpectra = wx.GridSizer(0, 2, 0, 0)
        self.panel_ids = np.zeros(2)
        for i in range(2):
            ID_PANEL = wx.NewId()
            self.panel_ids[i] = ID_PANEL
            self.m_panelSpec = wx.Panel(self, ID_PANEL, wx.DefaultPosition,
                                        wx.Size(-1, -1), wx.TAB_TRAVERSAL)
            self.m_panelSpec.SetBackgroundColour('grey')
            gSizer_SglsSpectra.Add(self.m_panelSpec, 1, wx.ALL | wx.EXPAND, 5)
        sbSizer_Singles.Add(gSizer_SglsSpectra, 1, wx.EXPAND, 5)


        # add the grid (sizer) to the StaticBox Sizer containing the grid and
        # the {mu(E);chi(k)} buttons
        bSizer_Display.Add(sbSizer_Singles, 1, wx.EXPAND, 0)
        bSizer_Main.Add(bSizer_Display, 1, wx.EXPAND, 5)
        self.SetSizer(bSizer_Main)
        self.Layout()


        # After the layout call (see above line), hide the static-box-sizer (sbSizer6)
        # which contains the fluorescence detector panels;
        # These panels are sensitive to MOUSE_OVER events that rely on data present in the
        # fluroescence detector. Lack of data causes error messages; by hiding the panels,
        # no events are triggered;
        # panels will be activated in OnLoadButton event routine (after data loaded)
        self.bSizer_Controls.Hide(self.sbSizer6)


        # also:
        #   (a) disable the "Unload" button as it attempts to delete variables from memory
        #       which are not loaded yet
        #       (enable this button after data has been loaded)
        #   (b) disable the edge selector list box
        #   (enable once data is loaded and an edge has been identified)
        #   (c) disable file selector checkList box
        self.m_button_Unload.Disable()
        self.m_listBox_Edge.Disable()
        self.m_checkList_Spectra.Disable()
        self.m_statusBar = self.CreateStatusBar(1, wx.ST_SIZEGRIP, wx.ID_ANY)
        self.Centre(wx.BOTH)
        self.Show(True)

        # for each panel to display spectra, generate a graphics canvas object
        self.canvasMuAverage = plot.PlotCanvas(self.m_panelMuAverage)
        self.canvasMuAverage.SetInitialSize(
            size=self.m_panelMuAverage.GetSize())
        self.canvasMuAverage.SetEnableZoom(True)
        self.canvasMuAverage.SetEnableGrid(True)
        self.canvasMuAverage.SetGridColour('grey')

        self.canvasChiAverage = plot.PlotCanvas(self.m_panelChiAverage)
        self.canvasChiAverage.SetInitialSize(
            size=self.m_panelChiAverage.GetSize())
        self.canvasChiAverage.SetEnableZoom(True)
        self.canvasChiAverage.SetEnableGrid(True)
        self.canvasChiAverage.SetGridColour('grey')

        self.canvasSingleSpectra = []
        for i in self.panel_ids:
            panel = wx.FindWindowById(i)
            canvas = plot.PlotCanvas(panel)
            canvas.SetInitialSize(size=panel.GetSize())
            canvas.SetEnableZoom(True)
            canvas.SetEnableGrid(True)
            canvas.SetGridColour('grey')
            self.canvasSingleSpectra.append(canvas)


        # Connect events to event handlers
        #   (detector clickPixel events connected in above loops that create detector)
        self.m_button_Load.Bind(wx.EVT_BUTTON, self.OnClick_Load)
        self.m_button_Save.Bind(wx.EVT_BUTTON, self.OnClick_Save)
        #self.m_button_SaveAll.Bind( wx.EVT_BUTTON, self.OnClick_SaveAll )
        self.m_button_Unload.Bind(wx.EVT_BUTTON, self.OnClick_Unload)
        self.m_button_Exit.Bind(wx.EVT_BUTTON, self.OnClick_Exit)

        #self.m_listBox_Spectra.Bind( wx.EVT_LISTBOX, self.OnList_SpecSelect )
        #self.m_listBox_Spectra.Bind( wx.EVT_MOUSEWHEEL, self.OnWheel_SpecSelect )
        self.m_checkList_Spectra.Bind(
            wx.EVT_LISTBOX, self.OnCheckList_SpecSelect)
        self.m_checkList_Spectra.Bind(
            wx.EVT_CHECKLISTBOX, self.OnCheckList_SpecToggle)

        self.m_listBox_Edge.Bind(wx.EVT_LISTBOX, self.OnList_EdgeSelect)
        self.m_listBox_Edge.Bind(wx.EVT_MOUSEWHEEL, self.OnWheel_EdgeSelect)
        self.m_radioBtn_DetInt.Bind(wx.EVT_RADIOBUTTON, self.OnRadioBtn_TCR)
        self.m_radioBtn_Correl.Bind(
            wx.EVT_RADIOBUTTON, self.OnRadioBtn_Correl)
        self.m_radioBtn_Weights.Bind(
            wx.EVT_RADIOBUTTON, self.OnRadioBtn_Weights)
        #self.m_buttonMu.Bind( wx.EVT_BUTTON, self.OnClick_Mu )
        #self.m_buttonChi.Bind( wx.EVT_BUTTON, self.OnClick_Chi )
        self.m_toggleBtn_MuChi.Bind(wx.EVT_TOGGLEBUTTON, self.OnToggleMuChi)
        #self.m_spinCtrl_SpecSelect.Bind( wx.EVT_SPINCTRL, self.OnSpinControl )
        #self.m_spinCtrl_SpecSelect.Bind( wx.EVT_TEXT, self.OnSpinControlText )


        # -----------------------------------------------------------
        # Non-GUI attributes
        # -----------------------------------------------------------
        # create an empty container (list) to hold results from averaging data
        #    later on, this will be filled with instances of the "Results()" Object
        #    (see above Class definition)
        # this is adequate here as part of initialising the whole application
        # see end of event function "OnClick_Load" for first use and details
        self.results = []

        # array to hold filenames of files already processed
        #   (see end of event function "OnClick_Load" for first use and details)
        self.whichProcessed = []

        # Holds a reference to the get_mda or get_netcdf module depending on the type of
        # mda opened by the Open File dialog. Ensure that this is set from None to
        # gmda or gnc and back to None but NOT from gmda to gnc or gnc to gmda. This will
        # ensure that users don't try to process mapping mode and step mode data at the
        # same time.
        self.reader = None
        
        # Holds the index of the last detector pixel left-clicked by the user
        self.index_lastPixelLeftClicked = None


    def __del__(self):
        pass

    def colourPixels(self, whichDet, inputArray, goodPixels, scale):
        """Scale the colour mapping only if keyword scale is True

        """
        # goodPixels is designed to include index values <0 to mark bad pixels;
        #    thus, needs compressing out all indices <0 first before using in a loop
        goodPixels = np.compress(goodPixels >= 0, goodPixels)

        # set colours of Det1/2 pixels according to inputArray values
        colourTable = cm.gist_heat                          # @UndefinedVariable
        numCols = colourTable.N

        if scale == True:
            # use MAX and MIN values of inputArray to stretch colour scale
            # (only consider values related to "goodPixels" (ie, good spectra))
            array_max = max(inputArray[goodPixels])
            array_min = min(inputArray[goodPixels])
            useArray = (numCols - 1) * (inputArray - array_min) / (array_max - array_min)
        else:
            # don't rescale
            useArray = (numCols - 1) * inputArray

        pixel_IDs = np.zeros(self.detSize)
        if whichDet == 1:          # choose which detector array to colour (Det1 or Det2)
            pixel_IDs = self.pixel_ids1
        elif whichDet == 2:
            pixel_IDs = self.pixel_ids2

        for i in goodPixels:
            colour = np.asarray(colourTable(int(useArray[i]))[0:3]) * 255
            pixelIdToColour = wx.FindWindowById(pixel_IDs[i])
            pixelIdToColour.SetBackgroundColour(colour)
            pixelIdToColour.Refresh()

    def plotSpectrum(self, x, y, xtitle, ytitle, outputWindow, moreY=None):
        """Send list of (x/y) tuples to plot output in destination   (here called "where")

        Returns:
        ID of the canvas object drawn on (useful for clearing a canvas from
        outside this function; needs XXX = wx.FindWindowById(canvasID)
        at external point to find this canvas; then clear with   XXX.Clear() )

        """
        # clear corresponding canvas
        canvas = outputWindow
        canvas.Clear()

        # zip data arrays together into list of tuples (wx.plot requires tuples)
        #   then define "line" objects to carry the data into the plot
        plotData = zip(x, y)
        line = plot.PolyLine(plotData, colour='red', width=1)
        if moreY is not None:
            plotMoreData = zip(x, moreY)
            moreLine = plot.PolyLine(plotMoreData, colour='blue', width=2)

        # send "line" objects to canvas and draw everything
        if moreY is not None:
            gc = plot.PlotGraphics([moreLine, line], '', xtitle, ytitle)
        else:
            gc = plot.PlotGraphics([line], '', xtitle, ytitle)

        canvas.Draw(gc)  # , xAxis=(0,15), yAxis=(0,15))

        return canvas.GetId()   # return canvas Object ID (will be used to write
                                # into self.ATTRIBUTES after external call; see there)

    def _mdaIsSelfContained(self, fname):
        """A method that checks whether we have an mda file containing fpeaks+speaks+roi
        values or whether we have that along with all MCA data in netCDF files. Just
        checks the 'rank' entry in the mda file to make a decision.

        Arguments:
        fname - mda filename

        Returns:
        True if the 'rank' entry in the mda file = 2
        False otherwise

        """
        # get the path to the netCDF files from the mda file
        mda = readMDA.readMDA(fname, verbose=False)
        return (mda[0]['rank'] == 2)

    def processData(self, whichFileToProcess):
        # read in ASCII file and extract energy axis (e=data[0])
        #   transmission data (trans=data[1]), and
        #   "detector" (list of pixel objects; see "get_mda.py" for details) (det=data[2])
        e, trans, det = self.reader.getData(whichFileToProcess)

        # add these variables as attributes to the MainFrame Class (here as "self")
        self.e = e            # energy axis in eV (conversion keV-->eV in "get_mda3.py")
        self.trans = trans
        self.t = self.trans[4][:]  # although this looks redundant it gives a separate
            # attribute for faster access to "t"
            # March/2013: at this stage, we are not using "self.t" anywhere; normalisation
            # to sample time is entirely done in module "gmda" ("get_mda[...].py");
            # careful also with this explicit column assignment [4]; column numbers could
            # change in "gmda"; check there!
        self.i0 = self.trans[1][:] # ! --> careful with explicit column assignment [1]
        self.det = det

        self.detSize = len(self.det)
        self.scanSize = len(self.e)

        # Average ROI countrate:
        #  (this is used for the first detector panel as information for the user)
        self.ROIaverage = np.zeros(self.detSize)
        for i in range(self.detSize):
            self.ROIaverage[i] = np.mean(self.det[i].roi)

        # Good Detector Pixels:
        assessPixels = self.reader.getGoodPixels(self.det, self.detSize)
        self.goodPixels = assessPixels[0]
        excludeForeverPixels = assessPixels[1]
            # no need to make that an attribute; only used here locally

        print 'exclude forever (mark red): ', excludeForeverPixels
        for i in excludeForeverPixels:
            foreverBadID1 = self.pixel_ids1[i]
            foreverBadID2 = self.pixel_ids2[i]
            foreverBadPixel1 = wx.FindWindowById(foreverBadID1)
            foreverBadPixel2 = wx.FindWindowById(foreverBadID2)
            #
            foreverBadPixel1.SetForegroundColour('red')
            foreverBadPixel2.SetForegroundColour('red')
            #
            foreverBadPixel1.Refresh()
            foreverBadPixel2.Refresh()

        # set colours of Det1 pixels according to ROI average countrate
        self.colourPixels(1, self.ROIaverage, self.goodPixels, scale=True)
        # END of goodPixels

        # estimate edge energy E0:
        self.edges = gmda.getE0(self.e)
        self.e0 = self.edges[2][0]
        #   "self.edges" is a list of lists [elements, shells, edgeEnergies]
        #   and is sorted by shells {K, L1, L2, L3};
        #   for the choice of E0, priority is given to K-shells where available,
        #   thus the choice "self.edges[2][0]"  (K = zero-th item in list edgeEnergies)
        #
        # END of e0 estimate

        # now insert all edges found up the top into the List Box (edges);
        #   for user to verify or choose from
        # also remove all other edge choices
        # highlight top priority edge just found
        temp = np.asarray([self.edges[0], np.repeat(
            '-', len(self.edges[0])), self.edges[1]]).T
        #       this generates a list of lists style of ['El','-','K']
        addListItems = []
        for i in range(len(temp)):
            print i, temp[i]
            addListItems.append(''.join(temp[i]))
        #       this loops through the list of lists, joins the
        #       sublists together, then writes them into "listItems"
        self.m_listBox_Edge.Clear()
        self.m_listBox_Edge.InsertItems(addListItems, 0)
        self.m_listBox_Edge.SetItemBackgroundColour(1, 'blue')
        self.m_listBox_Edge.SetItemForegroundColour(1, 'white')
        self.m_listBox_Edge.Refresh()

        # garbage collection
        del temp

        # Dead Time Correction:
        # now that we know a basic set of GoodPixels, apply dead time correction to
        #   obtain "roiCorr"
        gmda.detDeadCorr(self.det, self.goodPixels)
        # END of DeadTimeCorrection

        # Correlation Coefficients:
        # as starting point, set colours of Det2 pixels according to
        #   correlation coefficients
        #   (users can choose via radio buttons what to display in Det2 pixels)
        self.correls = gmda.getCorrels(self.det, self.goodPixels)
        self.colourPixels(2, self.correls, self.goodPixels, scale=False)
        # END of Correclation

        # Total Countrates (averaged):
        self.TCRaverage = np.zeros(self.detSize)
        for i in self.goodPixels:
            self.TCRaverage[i] = np.mean(self.det[i].fpeaks)
        #       np.divide(np.ndarray.flatten(self.det[i].fpeaks), self.t)
        # END of TCR

        # Normalise to I0
        #   this is done in the Detector Pixel Class because:
        #   each individual spectrum needs normalising (thus, this is a "pixel" matter)
        # conceptually, normalising could also be done after applying
        # the weight factors;
        #   however, during the weighting process, we are using polynomial fits, and
        #   while those fits are still in memory, we extract something like "chi(k)";
        #   if there is structure in the data from I0, then it is better to
        #   do the normalisation to I0 *before* the fitting
        gmda.normaliseI0(self.det, self.goodPixels, self.i0)
        # END of normalise to I0

        # Weight Factors:
        # compute weight factors for each spectrum (these reflect the statistical
        #   quality of a spactrum, based on the ratio of edge step height
        #   and pre-edge background)
        # this is useful to minimise the noise input of bad spectra into the
        #   final average
        self.weights = gmda.getWeightFactors(
            self.det, self.e, self.e0, self.goodPixels)
        gmda.applyWeights(self.det, self.goodPixels)
        # END of weight factors

        # Compute Average:
        # average all selected ("good") spectra using above weight factors
        averages = gmda.getAverage(self.goodPixels, self.det)
        self.averageMu = averages[0]
        self.averageChi = averages[1]
        print 'E0 = ', self.e0, 'eV'
        # END of Compute average

        # lastly, we need to get the k-axis for chi(k) from det[0]
        #   (remember, det[0] was used as a container only to transport k from "get_mda*" to here)
        self.k = self.det[0].k


    ############################################
    #
    # Event handlers
    #
    ############################################

    def OnClick_Load(self, event):
        """Load/Save/etc buttons (in controls area)"""
        dialog = wx.FileDialog(
            self, message="Choose a file",
            defaultDir=os.getcwd(),
            defaultFile="",
            ##wildcard='SR12ID01*.mda',
            style=wx.OPEN | wx.MULTIPLE | wx.CHANGE_DIR)

        if dialog.ShowModal() == wx.ID_OK:
            self.fname = dialog.GetFilename()

            # in spectra ListBox, remove initial default label reading "file"
            #   if present; then add new filename to ListBox
            # also: remove preceding "SR12ID01H" from label and display file No. only
            checklist_items = self.m_checkList_Spectra.GetItems()
            if checklist_items and (checklist_items[0] == 'file'):
                self.m_checkList_Spectra.Delete(0)
            listBoxEntry = self.fname.split('.mda')[0]
            listBoxEntry = listBoxEntry.split('SR12ID01H')[1]
            self.m_checkList_Spectra.Insert(listBoxEntry, 0)

            # check if fluorescence detector panels are hidden (sbSizer6);
            #   if so, unhide
            if not self.bSizer_Controls.IsShown(self.sbSizer6):
                self.bSizer_Controls.Show(self.sbSizer6)

            # Set step or netCDF mode based on the 'rank' entry in the mda file
            if self.reader is None:
                if self._mdaIsSelfContained(self.fname):
                    self.reader = gmda
                else:
                    self.reader = gnc

            # process data (dead time correction; weighting; averaging; etc)
            print 'processing file', self.fname
            self.processData(self.fname)

            # keep track of which file has been loaded/processed by storing filenames in
            # a list; insert items at the beginning of the list (because in corresponding
            # GUI CheckBoxList; newest item is listed up the top (i.e., FIFO)
            self.whichProcessed.insert(0, self.fname)
            print self.whichProcessed

            # in the __init__ function of this Class MainFrame, we generated a list of
            #   'results' objects (empty there)
            # start to fill this list now one by one; to do so, add the latest results
            #    at position 0 (i.e., LIFO)
            # (this list is structurally similar to the "det" list of "pixel" objects in
            #    library "GMDA")
            self.results.insert(0, Results())
            ##processIndex = len(self.whichProcessed)-1
            ##print 'process Index: ', processIndex
            self.results[0].fname = self.fname
            self.results[0].goodPixels = self.goodPixels
            self.results[0].averageMu = self.averageMu
            self.results[0].averageMu = self.averageMu
            self.results[0].averageChi = self.averageChi
            self.results[0].TCRaverage = self.TCRaverage
            self.results[0].ROIaverage = self.ROIaverage
            self.results[0].weights = self.weights
            self.results[0].correls = self.correls
            self.results[0].trans = self.trans
            self.results[0].det = self.det
            self.results[0].k = self.k
            self.results[0].e = self.e

            # we also have an attribute "self.specSelec" to consider; this attribute
            # tracks which spectrum is selected in the "self.m_checkList_Spectra"
            # checkList box by default, set this to zero (0) here; useful to always have
            # the latest spectrum loaded as the one that is active and displayed
            self.specSelec = 0

            # now send processed data to plot window(s)
            # 1. send averaged mu(E) to plot
            canvasID = self.plotSpectrum(
                self.results[0].e, self.results[0].averageMu,
                'E  /  eV', 'mu(E)*d  /  a.u.',
                self.canvasMuAverage)
            self.canvasID_panelMuAverage = canvasID

            # 2. send averaged chi(k)*k^2 to plot
            canvasID = self.plotSpectrum(self.results[0].k,
                                         self.results[0].averageChi
                                         * np.square(self.results[0].k),
                                         'k  /  A^-1', 'k^2 * chi(k)  /  a.u.',
                                         self.canvasChiAverage)
            self.canvasID_panelChiAverage = canvasID

            # lastly, enable the "Unload" button and the edge and file selector list boxes
            #   to enable user choices and interaction
            if len(self.whichProcessed) - 1 == 0:
                self.m_button_Unload.Enable()
                self.m_listBox_Edge.Enable()
                self.m_checkList_Spectra.Enable()

        #clean-up
        dialog.Destroy()

    def OnClick_Save(self, event):
        # test1 = event.GetId()
        # test = wx.FindWindowById(test1)
        print 'Saving data...'

        try:
            print 'selected: ', self.spectraChecked
            for i in self.spectraChecked:
                print '  --> saving: ', self.results[i].fname
                print self.results[i].goodPixels
                gmda.writeAverages(
                    self.results[i].fname, self.results[i].goodPixels,
                    self.results[i].correls, self.results[i].k,
                    self.results[i].e, self.results[i].trans,
                    self.results[i].weights,
                    self.results[i].averageMu, self.results[i].averageChi)
        except AttributeError:
            print 'Save Error: Please tick processed spectra you want to save.'

        #gmda.writeAverages(self.mda_out_fname, self.goodPixels, self.correls,
        #           self.k, self.e, self.trans, self.det,
        #           self.averageMu, self.averageChi)

    # def OnClick_SaveAll( self, event ):
    #    self.bSizer_Controls.Show(self.sbSizer6)

    def OnClick_Unload(self, event):
        """clear all plot canvasses, hide detector panels and "Unload" button.

        """
        self.bSizer_Controls.Hide(self.sbSizer6)
        self.m_button_Unload.Disable()
        self.m_listBox_Edge.Disable()
        self.m_checkList_Spectra.Disable()

        self.canvasMuAverage.Clear()
        self.canvasChiAverage.Clear()
        for i in range(len(self.panel_ids)):
            self.canvasSingleSpectra[i].Clear()

        # remove top file entry from File Listbox (NB: top one was last one loaded; LIFO)
        self.m_checkList_Spectra.Clear()

        # restore top file entry to initial state
        self.m_checkList_Spectra.Insert('file', 0)

        # clear from memory the data from last processed dataset
        del self.det, self.detSize,
        del self.averageMu, self.averageChi
        del self.TCRaverage, self.ROIaverage
        del self.weights, self.correls
        del self.trans, self.t, self.e, self.e0, self.i0, self.edges, self.scanSize

        # clear from memory all 'results' entries in 'results list'
        self.results = []
        self.whichProcessed = []

        # Reset step or netCDF reader mode, allowing it to be changed on the next load
        self.reader = None

    def OnClick_Exit(self, event):
        # writeParameters()
        # TODO: function that writes user params to disk to remember next session
        #       will also require "readParams" at end of MainFrame.__init__
            self.Destroy()

    def OnCheckList_SpecSelect(self, event):
        """Spectrum and Edge choice box events (in controls area).

        """
        self.specSelec = self.m_checkList_Spectra.GetSelection()
        print 'Spectrum selected: ', self.specSelec
        print 'fname: ', self.results[self.specSelec].fname

        # get previously processed data from memory and:
        # 1. send averaged mu(E) to plot
        canvasID = self.plotSpectrum(
            self.results[self.specSelec].e, self.results[
                self.specSelec].averageMu,
            'E  /  eV', 'mu(E)*d  /  a.u.',
            self.canvasMuAverage)
        self.canvasID_panelMuAverage = canvasID

        # 2. send averaged chi(k)*k^2 to plot
        canvasID = self.plotSpectrum(self.results[self.specSelec].k,
                                     self.results[self.specSelec].averageChi
                                     * np.square(self.results[self.specSelec].k),
                                     'k  /  A^-1', 'k^2 * chi(k)  /  a.u.',
                                     self.canvasChiAverage)
        self.canvasID_panelChiAverage = canvasID

    def OnCheckList_SpecToggle(self, event):
        self.spectraChecked = self.m_checkList_Spectra.GetChecked()

    def OnWheel_SpecSelect(self, event):
        event.Skip()

    def OnList_EdgeSelect(self, event):
        select = self.m_listBox_Edge.GetStringSelection()
        parts = select.split('-')
        element = parts[0]
        transition = parts[1]
        transitionIndex = np.where(
            np.asarray(etab.QNTransition) == transition)[0]
        self.e0 = etab.edgeEnergy[element][transitionIndex]

        print 'new E0 = ', self.e0, 'eV'

        print 're-computing weight factors...'
        # Clear weight factors, re-compute, and re-apply
        print self.weights[0]
        self.weights = None
        self.weights = gmda.getWeightFactors(
            self.det, self.e, self.e0, self.goodPixels)
        gmda.applyWeights(self.det, self.goodPixels)
        print self.weights[0]

        print 're-computing averages...'
        # Clear variables and compute average:
        self.averageMu = None
        self.averageChi = None
        averages = gmda.getAverage(self.goodPixels, self.det)
        self.averageMu = averages[0]
        self.averageChi = averages[1]

        print 'updating plot displays...'
        canvasID = self.plotSpectrum(self.e, self.averageMu,
                                     'E  /  eV', 'mu(E)*d  /  a.u.',
                                     self.canvasMuAverage)
        self.canvasID_panelMuAverage = canvasID

        self.k = self.det[0].k
        canvasID = self.plotSpectrum(
            self.k, self.averageChi * np.square(self.k),
            'k  /  A^-1', 'k^2 * chi(k)  /  a.u.',
                          self.canvasChiAverage)

    def OnWheel_EdgeSelect(self, event):
        event.Skip()

    def OnRightDownPixel(self, event):
        """Detector pixel events (in controls area)
        right mouse button down --> select / unselect pixel
        --- structure of "OnLeftDownPixel" and "OnLeave/EnterPixel" very similar
        --- comments on code are primarily here

        """
        #pixelId = event.GetId()
        #clickedPixel = wx.FindWindowById(pixelId)
        #clickedPixel = event.GetEventObject()

        # get ID of the pixel that triggered the event
        #   then get the actual window (object), since we need to manipulate
        #   the object's properties upon right click
        #   (=exclude from GoodPixels and visualise this by changing colour to grey)
        pixelID = event.GetId()
        clickedPixel = wx.FindWindowById(pixelID)

        # since we have two detector panels displayed, find the corresponding pixel on
        # the other panel (here called "linkedPixel")
        if pixelID in self.pixel_ids1:
            index = np.where(self.pixel_ids1 == pixelID)[0][0]
            linkedID = self.pixel_ids2[np.where(self.pixel_ids1 == pixelID)]
            linkedPixel = wx.FindWindowById(linkedID)
        elif pixelID in self.pixel_ids2:
            index = np.where(self.pixel_ids2 == pixelID)[0][0]
            linkedID = self.pixel_ids1[np.where(self.pixel_ids2 == pixelID)]
            linkedPixel = wx.FindWindowById(linkedID)
        else:
            print 'Error in colour routine: pixel ID not in detector pixel ID lists.'
            # the error message should never be enacted upon as we are strictly within
            #    a self-contained variable space
            #    -- "self.pixel_ids1/2" are defined when the widgets are created and
            #       then treated as global 'read-only' variables without any user
            #       input or changes;
            #    this primarily for debugging purposes

        # if pixel was previously excluded (=index set to -1; marked grey), then
        # re-include now, otherwise exclude (by setting to -1)
        if self.results[self.specSelec].goodPixels[index] > -1:
            # exclude = set to '-1'; can be undone by user
            self.results[self.specSelec].goodPixels[index] = -1
            clickedPixel.SetBackgroundColour('grey')        # wx.Colour( 255, 0, 0 )
            linkedPixel.SetBackgroundColour('grey')
        elif self.results[self.specSelec].goodPixels[index] == -1:
            self.results[self.specSelec].goodPixels[index] = index
            clickedPixel.SetBackgroundColour('blue')
            linkedPixel.SetBackgroundColour('blue')
            # re-paint the pixels in the detector panels (because one was clicked on
            # again and is still grey)
            self.colourPixels(1, self.results[self.specSelec].ROIaverage,
                              self.results[self.specSelec].goodPixels, scale=True)
            # TODO:  self.colourPixels(2, self.DEPENDSonRADIObutton, self.goodPixels, scale=RADIObutton***)

        # Since a pixel was included/excluded, the average mu & chi will have changed;
        # re-compute now ("getAverage()" returns a list of arrays, i.e. [averageMu, averageChi])
        averages = gmda.getAverage(self.results[self.specSelec].goodPixels,
                                   self.results[self.specSelec].det)
        self.results[self.specSelec].averageMu = averages[0]
        self.results[self.specSelec].averageChi = averages[1]

        # Send averaged mu(E) to corrsponding plot canvas
        temp = self.plotSpectrum(
            self.results[self.specSelec].e, self.results[
                self.specSelec].averageMu,
            'E  /  eV', 'mu(E)*d  /  a.u.',
            self.canvasMuAverage)
            #self.m_panelMuAverage)

        # Send averaged chi(k) to corresponding plot canvas
        #self.k = self.det[0].k
        temp = self.plotSpectrum(self.results[self.specSelec].k,
                                 self.results[self.specSelec].averageChi
                                 * np.square(self.results[self.specSelec].k),
                                 'k  /  A^-1', 'chi(k)*k^2  /  a.u.',
                                 self.canvasChiAverage)
            #self.m_panelChiAverage)

        #currentColour = clickedPixel.GetBackgroundColour()
        #if currentColour.GetAsString() == 'grey' : pass
        # refresh objects (=redraw)
        clickedPixel.Refresh()
        linkedPixel.Refresh()

    def OnLeftDownPixel(self, event):
        """left mouse button down --> display spectrum of corresponding pixel
        --- structure similar to "OnRightDownPixel"
        --- see there for more detailed comments

        """
        pixelID = event.GetId()
        clickedPixel = wx.FindWindowById(pixelID)

        if pixelID in self.pixel_ids1:
            index = np.where(self.pixel_ids1 == pixelID)[0]
            linkedID = self.pixel_ids2[index]
            linkedPixel = wx.FindWindowById(linkedID)
        elif pixelID in self.pixel_ids2:
            index = np.where(self.pixel_ids2 == pixelID)[0]
            linkedID = self.pixel_ids1[index]
            linkedPixel = wx.FindWindowById(linkedID)
        else:
            print 'Error in plot routine: pixel ID not in detector pixel ID lists.'

        # further action only for pixels that are not forever
        # excluded (forever excluded = -2)
        if self.results[self.specSelec].goodPixels[index] >= -1:
            # get info of current font used to label the pixel of interest
            #   and set BOLD to show that this pixel spectrum is being plotted
            currentFont = clickedPixel.GetFont()
            currentFont.SetWeight(wx.BOLD)
            clickedPixel.SetFont(currentFont)
            linkedPixel.SetFont(currentFont)
            
            if self.index_lastPixelLeftClicked != None :
                lastPixel1 = wx.FindWindowById( self.pixel_ids1[self.index_lastPixelLeftClicked] )
                lastPixel2 = wx.FindWindowById( self.pixel_ids2[self.index_lastPixelLeftClicked] )
                lastFont = lastPixel1.GetFont()
                lastFont.SetWeight(wx.NORMAL)
                lastPixel1.SetFont(lastFont)
                lastPixel2.SetFont(lastFont)
                lastPixel1.SetForegroundColour('black')
                lastPixel2.SetForegroundColour('black')
                lastPixel1.Refresh()
                lastPixel2.Refresh()

            # Refresh pixels
            clickedPixel.Refresh()
            linkedPixel.Refresh()

            # define 'x' and 'y' for plotting depending on toggle button state (mu/chi)
            if self.m_toggleBtn_MuChi.GetValue() == True:  # if toggled, display chi(k)
                x = self.results[self.specSelec].k
                y = self.results[self.specSelec].det[index].chi
                xlabel = 'k  /  A^-1'
                ylabel = 'chi(k)  /  a.u.'
            else:
                x = self.results[self.specSelec].e
                y = np.reshape(self.results[self.specSelec]
                               .det[index].roiCorr, self.scanSize)
                ##y = zip(y,self.results[self.specSelec].averageMu)
                xlabel = 'E  /  eV'
                ylabel = 'mu(E)*d  /  a.u.'
            # send to second plot panel canvas used to display single detector channels
            ##destination = wx.FindWindowById(self.panel_ids[1])
            destination = self.canvasSingleSpectra[1]
            canvasID = self.plotSpectrum(x, y, xlabel, ylabel, destination,
                                         self.results[self.specSelec].averageMu)
            self.canvasID_selectedSingleSpec = canvasID

            # lastly, write the index of the pixel left-clicked into an attribute
            #   (need to know when changing plot output between mu(E) and chi(k))
            self.index_lastPixelLeftClicked = index

    def OnEnterPixel(self, event):
        """mouse entering pixel --> display pixel values in status bar
        --> highlight pixel label
        --- structure similar to "OnRightDownPixel"
        --- see there for more detailed comments

        """
        # identify which pixel triggered event
        pixelID = event.GetEventObject().GetId()
        pixelEntered = wx.FindWindowById(pixelID)
        # identify which pixel number (index) belongs to the triggering pixel
        if pixelID in self.pixel_ids1:
            index = np.where(self.pixel_ids1 == pixelID)[0]
            linkedID = self.pixel_ids2[index]
            linkedPixel = wx.FindWindowById(linkedID)
        elif pixelID in self.pixel_ids2:
            index = np.where(self.pixel_ids2 == pixelID)[0]
            linkedID = self.pixel_ids1[index]
            linkedPixel = wx.FindWindowById(linkedID)
        else:
            print 'Error in enter_window routine: pixel ID not in detector pixel ID lists.'

        # read values of interest and write into status bar
        self.m_statusBar.SetStatusText(''.join([\
            'ROI average: {roi_average} cts/sec  --  ',
            'Correlation: {correlation:0.2%}  --  ',
            'TCR average: {tcr_average} cts/sec  --  ',
            'Weight: {weight:0.2f}',
            ]).format(
                roi_average=int(self.results[self.specSelec].ROIaverage[index]),
                correlation=self.results[self.specSelec].correls[index][0],
                tcr_average=int(self.results[self.specSelec].TCRaverage[index]),
                weight=self.results[self.specSelec].det[index].weightFactor,
            ),
            0,
        )

        # further action only for pixels that are not forever excluded (i.e., =-2)
        if self.results[self.specSelec].goodPixels[index] >= -1:
            # highlight font of pixel entered as "yellow"; then refresh (redraw) pixel
            pixelEntered.SetForegroundColour('yellow')
            linkedPixel.SetForegroundColour('yellow')
            pixelEntered.Refresh()
            linkedPixel.Refresh()
            # dynamically update the plot left panel for individual detector channels
            #   define 'x' and 'y' for plotting, depending on whether mu(E) or chi(k)
            #   is to be plotted
            if self.m_toggleBtn_MuChi.GetValue() == True:  # if toggled display chi(k)
                x = self.results[self.specSelec].k
                y = self.results[self.specSelec].det[index].chi
                xlabel = 'k  /  A^-1'
                ylabel = 'chi(k)  /  a.u.'
            else:
                x = self.e
                y = np.reshape(self.det[index].roiCorr, self.scanSize)
                xlabel = 'E  /  eV'
                ylabel = 'mu(E)*d  /  a.u.'

            # send plot to canvas in corresponding panel
            ##destination = wx.FindWindowById(self.panel_ids[0])
            destination = self.canvasSingleSpectra[0]
            canvasID = self.plotSpectrum(x, y, xlabel, ylabel, destination)
            self.canvasID_enteredSingleSpec = canvasID

        # lastly, write the index of the pixel entered into an attribute
        #   (need to know when changing plot output between mu(E) and chi(k))
        self.index_lastPixelEntered = index

    def OnLeavePixel(self, event):
        """mouse leaving pixel --> revert pixel label to default colour
        --- structure similar to "OnRightDownPixel"
        --- see there for more detailed comments

        """
        pixelID = event.GetEventObject().GetId()
        pixelLeft = wx.FindWindowById(pixelID)
        if pixelID in self.pixel_ids1:
            index = np.where(self.pixel_ids1 == pixelID)[0]
            linkedID = self.pixel_ids2[index]
            linkedPixel = wx.FindWindowById(linkedID)
        elif pixelID in self.pixel_ids2:
            index = np.where(self.pixel_ids2 == pixelID)[0]
            linkedID = self.pixel_ids1[index]
            linkedPixel = wx.FindWindowById(linkedID)
        else:
            print 'Error in leave_window routine: pixel ID not in detector pixel ID lists.'

        if self.results[self.specSelec].goodPixels[index] >= -1:
            # get info of current font used to label the pixel of interest
            currentFont = pixelLeft.GetFont()
            currentWeight = currentFont.GetWeightString()
            # if NOT set in NORMAL (e.g. BOLD face) then pixel spectrum currently
            #    displayed; do not change
            if currentWeight == 'wxNORMAL':
                pixelLeft.SetForegroundColour('black')
                linkedPixel.SetForegroundColour('black')
                pixelLeft.Refresh()
                linkedPixel.Refresh()

    def OnRadioBtn_TCR(self, event):
        """radio button events (in controls panels)"""
        self.colourPixels(2, self.results[self.specSelec].TCRaverage,
                          self.results[self.specSelec].goodPixels, scale=True)
        # display average TCR scaled to range of colour scale (256 colours)

    def OnRadioBtn_Correl(self, event):
        self.colourPixels(2, self.results[self.specSelec].correls,
                          self.results[self.specSelec].goodPixels, scale=False)
        # display correlation coefficients [0...1]; not scaled to help identify bad outliers

    def OnRadioBtn_Weights(self, event):
        self.colourPixels(2, self.results[self.specSelec].weights,
                          self.results[self.specSelec].goodPixels, scale=False)
        # display weight factors ([0...1]); not scaled to help identify bad spectra

    def OnToggleMuChi(self, event):
        """Mu(E) / Chi(k) toggle button events (in display area)
        initial state is 'False' (not pressed); label = u"chi(k)"
        allows user to switch between displaying chi(k) and mu(k) in the single spectrum
        displays
        (if button label = "chi(k)"), then pressing would display chi(k))

        """
        if self.m_toggleBtn_MuChi.GetValue() == True:
            # switch label to read "mu(E)"...
            self.m_toggleBtn_MuChi.SetLabel(u"mu(E)")
            # ... then plot chi(k):
            #
            # only take action if pixel is not "forever bad (=-2)";
            #   thus even unselected spectra may be displayed
            if self.results[self.specSelec].goodPixels[self.index_lastPixelEntered] >= -1:
                wx.FindWindowById(self.canvasID_enteredSingleSpec).Clear()
                y = self.results[self.specSelec].det[
                    self.index_lastPixelEntered].chi
                ##destination = wx.FindWindowById(self.panel_ids[0])
                destination = self.canvasSingleSpectra[0]
                temp = self.plotSpectrum(self.results[self.specSelec].k, y,
                                         'k  /  A^-1', 'chi(k)  /  a.u.', destination)

            # again, only do an action if not "forever bad (='-2')"
            if (self.results[self.specSelec].goodPixels[self.index_lastPixelLeftClicked]
                >= -1):
                wx.FindWindowById(self.canvasID_selectedSingleSpec).Clear
                # destination = wx.FindWindowById(self.panel_ids[1])
                y = self.results[self.specSelec].det[self.index_lastPixelLeftClicked].chi
                destination = self.canvasSingleSpectra[1]
                temp = self.plotSpectrum(self.results[self.specSelec].k, y,
                                         'k  /  A^-1', 'chi(k)  /  a.u.', destination)

        elif self.m_toggleBtn_MuChi.GetValue() == False:
            # switch label to read "chi(k)"...
            self.m_toggleBtn_MuChi.SetLabel(u"chi(k)")
            # ... then plot mu(E):

            # only take action if pixel is not "forever bad (=-2)";
            #   thus even unselected spectra may be displayed
            if self.results[self.specSelec].goodPixels[self.index_lastPixelEntered] >= -1:
                wx.FindWindowById(self.canvasID_enteredSingleSpec).Clear()
                y = self.results[self.specSelec].det[
                    self.index_lastPixelEntered].roiCorr
                ##destination = wx.FindWindowById(self.panel_ids[0])
                destination = self.canvasSingleSpectra[0]
                temp = self.plotSpectrum(self.results[self.specSelec].e, y,
                                         'E  /  eV', 'mu(E)*d  /  a.u.', destination)

            # again, only action if not "forever bad (='-2')"
            if self.goodPixels[self.index_lastPixelLeftClicked] >= -1:
                wx.FindWindowById(self.canvasID_selectedSingleSpec).Clear
                y = np.reshape(
                    self.results[self.specSelec].det[
                        self.index_lastPixelLeftClicked].roiCorr,
                    self.scanSize)
                ##destination = wx.FindWindowById(self.panel_ids[1])
                destination = self.canvasSingleSpectra[1]
                temp = self.plotSpectrum(self.results[self.specSelec].e, y,
                                         'E  /  eV', 'mu(E)*d  /  a.u.', destination)

        # Spectrum Select Spin Control (in display area)
        #
        #def OnSpinControl( self, event ) :
        ## chane spectrum displayed upon clicking arrow button
        #event.Skip()
        #def OnSpinControlText( self, event ) :
        ## change spectrum displayed upon entering number
        #event.Skip()
##
## ==== MAIN ====
##
if __name__ == '__main__':
    app = wx.App(False)
    frame = MainFrame(None)
    app.MainLoop()
