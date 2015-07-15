# -*- coding: utf-8 -*- 

###########################################################################
## Python code generated with wxFormBuilder (version Jun  5 2014)
## http://www.wxformbuilder.org/
##
## PLEASE DO "NOT" EDIT THIS FILE!
###########################################################################

import wx
import wx.xrc

id_load = 1000
id_save = 1001
id_unload = 1002
id_exit = 1003

###########################################################################
## Class MainFrame
###########################################################################

class MainFrame ( wx.Frame ):
	
	def __init__( self, parent ):
		wx.Frame.__init__ ( self, parent, id = wx.ID_ANY, title = u"-- Sakura --", pos = wx.DefaultPosition, size = wx.Size( 1018,910 ), style = wx.DEFAULT_FRAME_STYLE|wx.TAB_TRAVERSAL )
		
		self.SetSizeHintsSz( wx.DefaultSize, wx.DefaultSize )
		
		bMainSizer = wx.BoxSizer( wx.VERTICAL )
		
		self.m_MainPanel = wx.Panel( self, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.TAB_TRAVERSAL )
		bMainFrameSizer = wx.BoxSizer( wx.HORIZONTAL )
		
		self.m_LeftPanel = wx.Panel( self.m_MainPanel, wx.ID_ANY, wx.DefaultPosition, wx.Size( -1,-1 ), wx.TAB_TRAVERSAL )
		bLeftPanelSizer = wx.BoxSizer( wx.VERTICAL )
		
		self.m_ToolPanel = wx.Panel( self.m_LeftPanel, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.TAB_TRAVERSAL )
		fgSizer1 = wx.FlexGridSizer( 0, 3, 0, 0 )
		fgSizer1.AddGrowableCol( 1 )
		fgSizer1.SetFlexibleDirection( wx.HORIZONTAL )
		fgSizer1.SetNonFlexibleGrowMode( wx.FLEX_GROWMODE_SPECIFIED )
		
		self.m_toolBar1 = wx.ToolBar( self.m_ToolPanel, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.TB_HORIZONTAL )
		self.m_toolBar1.SetToolBitmapSize( wx.Size( 16,16 ) )
		self.m_LoadTool = self.m_toolBar1.AddLabelTool( id_load, u"Load", wx.Bitmap( u"resources/folder_vertical_open.png", wx.BITMAP_TYPE_ANY ), wx.NullBitmap, wx.ITEM_NORMAL, u"Load", wx.EmptyString, None )
		
		self.m_SaveTool = self.m_toolBar1.AddLabelTool( id_save, u"Save", wx.Bitmap( u"resources/disk.png", wx.BITMAP_TYPE_ANY ), wx.NullBitmap, wx.ITEM_NORMAL, u"Save", wx.EmptyString, None )
		
		self.m_UnloadTool = self.m_toolBar1.AddLabelTool( id_unload, u"Unload", wx.Bitmap( u"resources/folder_vertical_torn.png", wx.BITMAP_TYPE_ANY ), wx.NullBitmap, wx.ITEM_NORMAL, u"Unload", wx.EmptyString, None )
		
		self.m_toolBar1.Realize() 
		
		fgSizer1.Add( self.m_toolBar1, 0, wx.EXPAND, 5 )
		
		self.m_toolBar2 = wx.ToolBar( self.m_ToolPanel, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.TB_HORIZONTAL )
		self.m_toolBar2.SetToolBitmapSize( wx.Size( 16,16 ) )
		self.m_toolBar2.AddSeparator()
		
		self.m_toolBar2.Realize() 
		
		fgSizer1.Add( self.m_toolBar2, 0, wx.EXPAND, 5 )
		
		self.m_toolBar3 = wx.ToolBar( self.m_ToolPanel, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.TB_HORIZONTAL )
		self.m_toolBar3.SetToolBitmapSize( wx.Size( 16,16 ) )
		self.m_ExitTool = self.m_toolBar3.AddLabelTool( id_exit, u"Exit", wx.Bitmap( u"resources/door_in.png", wx.BITMAP_TYPE_ANY ), wx.NullBitmap, wx.ITEM_NORMAL, u"Exit", wx.EmptyString, None )
		
		self.m_toolBar3.Realize() 
		
		fgSizer1.Add( self.m_toolBar3, 0, wx.EXPAND, 5 )
		
		
		self.m_ToolPanel.SetSizer( fgSizer1 )
		self.m_ToolPanel.Layout()
		fgSizer1.Fit( self.m_ToolPanel )
		bLeftPanelSizer.Add( self.m_ToolPanel, 0, wx.ALL|wx.EXPAND, 0 )
		
		self.m_FormPanel = wx.Panel( self.m_LeftPanel, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.TAB_TRAVERSAL )
		bSizer6 = wx.BoxSizer( wx.HORIZONTAL )
		
		m_checkList_SpectraChoices = []
		self.m_checkList_Spectra = wx.CheckListBox( self.m_FormPanel, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, m_checkList_SpectraChoices, 0 )
		bSizer6.Add( self.m_checkList_Spectra, 1, wx.ALL, 5 )
		
		m_listBox_EdgeChoices = [ u"edge" ]
		self.m_listBox_Edge = wx.ListBox( self.m_FormPanel, wx.ID_ANY, wx.DefaultPosition, wx.Size( -1,-1 ), m_listBox_EdgeChoices, 0 )
		self.m_listBox_Edge.SetFont( wx.Font( wx.NORMAL_FONT.GetPointSize(), 70, 90, 90, False, wx.EmptyString ) )
		
		bSizer6.Add( self.m_listBox_Edge, 1, wx.ALL, 5 )
		
		
		self.m_FormPanel.SetSizer( bSizer6 )
		self.m_FormPanel.Layout()
		bSizer6.Fit( self.m_FormPanel )
		bLeftPanelSizer.Add( self.m_FormPanel, 0, wx.EXPAND |wx.ALL, 5 )
		
		self.m_DetectorPanel = wx.Panel( self.m_LeftPanel, wx.ID_ANY, wx.DefaultPosition, wx.Size( -1,-1 ), wx.TAB_TRAVERSAL )
		sbFluoroDetectorSizer = wx.StaticBoxSizer( wx.StaticBox( self.m_DetectorPanel, wx.ID_ANY, u"Detector" ), wx.VERTICAL )
		
		self.m_FluoroUpperPanel = wx.Panel( self.m_DetectorPanel, wx.ID_ANY, wx.DefaultPosition, wx.Size( 220,220 ), wx.TAB_TRAVERSAL )
		sbFluoroDetectorSizer.Add( self.m_FluoroUpperPanel, 0, wx.EXPAND |wx.ALL, 5 )
		
		self.m_staticline1 = wx.StaticLine( self.m_DetectorPanel, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.LI_HORIZONTAL )
		sbFluoroDetectorSizer.Add( self.m_staticline1, 0, wx.EXPAND |wx.ALL, 5 )
		
		self.m_FluoroLowerPanel = wx.Panel( self.m_DetectorPanel, wx.ID_ANY, wx.DefaultPosition, wx.Size( 220,220 ), wx.TAB_TRAVERSAL )
		sbFluoroDetectorSizer.Add( self.m_FluoroLowerPanel, 0, wx.EXPAND |wx.ALL, 5 )
		
		self.m_FluoroRBGroupPanel = wx.Panel( self.m_DetectorPanel, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.TAB_TRAVERSAL )
		bSizer10 = wx.BoxSizer( wx.HORIZONTAL )
		
		self.m_radioBtn_Correl = wx.RadioButton( self.m_FluoroRBGroupPanel, wx.ID_ANY, u"Correlation", wx.DefaultPosition, wx.DefaultSize, wx.RB_GROUP )
		self.m_radioBtn_Correl.SetValue( True ) 
		bSizer10.Add( self.m_radioBtn_Correl, 0, wx.ALL, 2 )
		
		self.m_radioBtn_Weights = wx.RadioButton( self.m_FluoroRBGroupPanel, wx.ID_ANY, u"Weights", wx.DefaultPosition, wx.DefaultSize, 0 )
		bSizer10.Add( self.m_radioBtn_Weights, 0, wx.ALL, 2 )
		
		self.m_radioBtn_DetInt = wx.RadioButton( self.m_FluoroRBGroupPanel, wx.ID_ANY, u"TCR (avg)", wx.DefaultPosition, wx.DefaultSize, 0 )
		bSizer10.Add( self.m_radioBtn_DetInt, 0, wx.ALL, 2 )
		
		
		self.m_FluoroRBGroupPanel.SetSizer( bSizer10 )
		self.m_FluoroRBGroupPanel.Layout()
		bSizer10.Fit( self.m_FluoroRBGroupPanel )
		sbFluoroDetectorSizer.Add( self.m_FluoroRBGroupPanel, 0, wx.EXPAND |wx.ALL, 5 )
		
		
		self.m_DetectorPanel.SetSizer( sbFluoroDetectorSizer )
		self.m_DetectorPanel.Layout()
		sbFluoroDetectorSizer.Fit( self.m_DetectorPanel )
		bLeftPanelSizer.Add( self.m_DetectorPanel, 0, wx.EXPAND |wx.ALL, 5 )
		
		self.m_WeightFactorPanel = wx.Panel( self.m_LeftPanel, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.TAB_TRAVERSAL )
		bSizer18 = wx.BoxSizer( wx.HORIZONTAL )

		m_radioBox1Choices = [ u"Edge step", u"TCR", u"=1" ]
		self.m_radioBox1 = wx.RadioBox( self.m_WeightFactorPanel, wx.ID_ANY, u"Weight Factor", wx.DefaultPosition, wx.DefaultSize, m_radioBox1Choices, 3, wx.RA_SPECIFY_COLS )
		self.m_radioBox1.SetSelection( 2 )
		bSizer18.Add( self.m_radioBox1, 0, wx.ALL, 5 )


		self.m_WeightFactorPanel.SetSizer( bSizer18 )
		self.m_WeightFactorPanel.Layout()
		bSizer18.Fit( self.m_WeightFactorPanel )
		bLeftPanelSizer.Add( self.m_WeightFactorPanel, 0, wx.EXPAND |wx.ALL, 5 )

		self.m_DeadTimePanel = wx.Panel( self.m_LeftPanel, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.TAB_TRAVERSAL )
		bSizer17 = wx.BoxSizer( wx.HORIZONTAL )

		m_radioBox2Choices = [ u"ICR_corr / OCR", u"( ICR / OCR )" ]
		self.m_radioBox2 = wx.RadioBox( self.m_DeadTimePanel, wx.ID_ANY, u"Dead-Time Correction", wx.DefaultPosition, wx.DefaultSize, m_radioBox2Choices, 2, wx.RA_SPECIFY_COLS )
		self.m_radioBox2.SetSelection( 0 )
		bSizer17.Add( self.m_radioBox2, 0, wx.ALL, 5 )


		self.m_DeadTimePanel.SetSizer( bSizer17 )
		self.m_DeadTimePanel.Layout()
		bSizer17.Fit( self.m_DeadTimePanel )
		bLeftPanelSizer.Add( self.m_DeadTimePanel, 0, wx.EXPAND |wx.ALL, 5 )


		self.m_LeftPanel.SetSizer( bLeftPanelSizer )
		self.m_LeftPanel.Layout()
		bLeftPanelSizer.Fit( self.m_LeftPanel )
		bMainFrameSizer.Add( self.m_LeftPanel, 0, wx.ALL|wx.EXPAND, 0 )
		
		self.m_RightPanel = wx.Panel( self.m_MainPanel, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.TAB_TRAVERSAL )
		bRightPanelSizer = wx.BoxSizer( wx.VERTICAL )
		
		self.m_splitter1 = wx.SplitterWindow( self.m_RightPanel, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.SP_3D )
		self.m_splitter1.Bind( wx.EVT_IDLE, self.m_splitter1OnIdle )
		self.m_splitter1.SetMinimumPaneSize( 200 )
		
		self.m_UpperRightPanel = wx.Panel( self.m_splitter1, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.TAB_TRAVERSAL )
		bSizer61 = wx.BoxSizer( wx.VERTICAL )
		
		self.m_UpperNotebook = wx.Notebook( self.m_UpperRightPanel, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.NB_LEFT )
		self.m_AvgsPanel = wx.Panel( self.m_UpperNotebook, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.TAB_TRAVERSAL, u"m_AvgsPanel" )
		bAvgsSizer = wx.BoxSizer( wx.HORIZONTAL )
		
		self.m_panelTopLeft = wx.Panel( self.m_AvgsPanel, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.TAB_TRAVERSAL )
		bAvgsSizer.Add( self.m_panelTopLeft, 1, wx.EXPAND |wx.ALL, 5 )
		
		self.m_panelTopRight = wx.Panel( self.m_AvgsPanel, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.TAB_TRAVERSAL )
		bAvgsSizer.Add( self.m_panelTopRight, 1, wx.EXPAND |wx.ALL, 5 )
		
		
		self.m_AvgsPanel.SetSizer( bAvgsSizer )
		self.m_AvgsPanel.Layout()
		bAvgsSizer.Fit( self.m_AvgsPanel )
		self.m_UpperNotebook.AddPage( self.m_AvgsPanel, u"Avg", True )
		self.m_SpectrumPanel = wx.Panel( self.m_UpperNotebook, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.TAB_TRAVERSAL, u"m_SpectrumPanel" )
		bSizer11 = wx.BoxSizer( wx.VERTICAL )
		
		self.m_SpectrumPlotPanel = wx.Panel( self.m_SpectrumPanel, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.TAB_TRAVERSAL )
		bSizer11.Add( self.m_SpectrumPlotPanel, 1, wx.EXPAND |wx.ALL, 5 )
		
		self.m_RoiPanel = wx.Panel( self.m_SpectrumPanel, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.TAB_TRAVERSAL )
		bSizer13 = wx.BoxSizer( wx.HORIZONTAL )
		
		self.m_staticText1 = wx.StaticText( self.m_RoiPanel, wx.ID_ANY, u"ROI", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_staticText1.Wrap( -1 )
		bSizer13.Add( self.m_staticText1, 0, wx.ALIGN_CENTER|wx.ALL, 2 )
		
		self.m_RoiLowSlider = wx.Slider( self.m_RoiPanel, wx.ID_ANY, 50, 0, 100, wx.DefaultPosition, wx.DefaultSize, wx.SL_HORIZONTAL|wx.SL_TOP, wx.DefaultValidator, u"m_RoiLowSlider" )
		self.m_RoiLowSlider.SetToolTipString( u"ROI Low" )
		
		bSizer13.Add( self.m_RoiLowSlider, 4, wx.ALL, 0 )
		
		self.m_RoiLowSpinCtrl = wx.SpinCtrl( self.m_RoiPanel, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.DefaultSize, wx.SP_ARROW_KEYS, 0, 10, 0, u"m_RoiLowSpinCtrl" )
		self.m_RoiLowSpinCtrl.SetToolTipString( u"ROI Low" )
		
		bSizer13.Add( self.m_RoiLowSpinCtrl, 1, wx.ALL, 2 )
		
		self.m_RoiHighSlider = wx.Slider( self.m_RoiPanel, wx.ID_ANY, 50, 0, 100, wx.DefaultPosition, wx.DefaultSize, wx.SL_HORIZONTAL|wx.SL_TOP, wx.DefaultValidator, u"m_RoiHighSlider" )
		self.m_RoiHighSlider.SetToolTipString( u"ROI High" )
		
		bSizer13.Add( self.m_RoiHighSlider, 4, wx.ALL, 0 )
		
		self.m_RoiHighSpinCtrl = wx.SpinCtrl( self.m_RoiPanel, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.DefaultSize, wx.SP_ARROW_KEYS, 0, 10, 0, u"m_RoiHighSpinCtrl" )
		self.m_RoiHighSpinCtrl.SetToolTipString( u"ROI High" )
		
		bSizer13.Add( self.m_RoiHighSpinCtrl, 1, wx.ALL, 2 )
		
		self.m_bpRefreshButton = wx.BitmapButton( self.m_RoiPanel, wx.ID_ANY, wx.Bitmap( u"resources/arrow_refresh_small.png", wx.BITMAP_TYPE_ANY ), wx.DefaultPosition, wx.DefaultSize, wx.BU_AUTODRAW )
		self.m_bpRefreshButton.SetToolTipString( u"Reprocess" )
		
		bSizer13.Add( self.m_bpRefreshButton, 0, wx.ALL, 2 )
		
		self.m_bpLogLinButton = wx.BitmapButton( self.m_RoiPanel, wx.ID_ANY, wx.Bitmap( u"resources/to_log.png", wx.BITMAP_TYPE_ANY ), wx.DefaultPosition, wx.DefaultSize, wx.BU_AUTODRAW, wx.DefaultValidator, u"to_log" )
		self.m_bpLogLinButton.SetToolTipString( u"Toggle Log/Lin scaling" )
		
		bSizer13.Add( self.m_bpLogLinButton, 0, wx.ALL, 2 )
		
		
		self.m_RoiPanel.SetSizer( bSizer13 )
		self.m_RoiPanel.Layout()
		bSizer13.Fit( self.m_RoiPanel )
		bSizer11.Add( self.m_RoiPanel, 0, wx.ALL|wx.EXPAND, 0 )
		
		self.m_SpectrumSelectionPanel = wx.Panel( self.m_SpectrumPanel, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.SUNKEN_BORDER|wx.TAB_TRAVERSAL )
		bSizer12 = wx.BoxSizer( wx.HORIZONTAL )
		
		self.m_staticText2 = wx.StaticText( self.m_SpectrumSelectionPanel, wx.ID_ANY, u"Energy Step", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_staticText2.Wrap( -1 )
		bSizer12.Add( self.m_staticText2, 0, wx.ALIGN_CENTER|wx.ALL, 2 )
		
		self.m_StepSlider = wx.Slider( self.m_SpectrumSelectionPanel, wx.ID_ANY, 1, 1, 100, wx.DefaultPosition, wx.DefaultSize, wx.SL_BOTH|wx.SL_HORIZONTAL )
		self.m_StepSlider.SetToolTipString( u"Energy Step" )
		
		bSizer12.Add( self.m_StepSlider, 8, wx.ALL, 0 )
		
		self.m_StepSpinCtrl = wx.SpinCtrl( self.m_SpectrumSelectionPanel, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.DefaultSize, wx.SP_ARROW_KEYS, 1, 100, 1 )
		self.m_StepSpinCtrl.SetToolTipString( u"Energy Step" )
		
		bSizer12.Add( self.m_StepSpinCtrl, 1, wx.ALIGN_CENTER|wx.ALL, 2 )
		
		
		self.m_SpectrumSelectionPanel.SetSizer( bSizer12 )
		self.m_SpectrumSelectionPanel.Layout()
		bSizer12.Fit( self.m_SpectrumSelectionPanel )
		bSizer11.Add( self.m_SpectrumSelectionPanel, 0, wx.ALL|wx.EXPAND, 2 )
		
		
		self.m_SpectrumPanel.SetSizer( bSizer11 )
		self.m_SpectrumPanel.Layout()
		bSizer11.Fit( self.m_SpectrumPanel )
		self.m_UpperNotebook.AddPage( self.m_SpectrumPanel, u"Spectrum", False )
		
		bSizer61.Add( self.m_UpperNotebook, 1, wx.EXPAND |wx.ALL, 0 )
		
		
		self.m_UpperRightPanel.SetSizer( bSizer61 )
		self.m_UpperRightPanel.Layout()
		bSizer61.Fit( self.m_UpperRightPanel )
		self.m_LowerRightPanel = wx.Panel( self.m_splitter1, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.TAB_TRAVERSAL )
		bSizer7 = wx.BoxSizer( wx.VERTICAL )
		
		self.m_MuChiNotebook = wx.Notebook( self.m_LowerRightPanel, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.NB_LEFT )
		self.m_MuPanel = wx.Panel( self.m_MuChiNotebook, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.TAB_TRAVERSAL, u"m_MuPanel" )
		bSizer101 = wx.BoxSizer( wx.HORIZONTAL )
		
		self.m_MuLeftPanel = wx.Panel( self.m_MuPanel, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.TAB_TRAVERSAL )
		bSizer101.Add( self.m_MuLeftPanel, 1, wx.EXPAND |wx.ALL, 5 )
		
		self.m_MuRightPanel = wx.Panel( self.m_MuPanel, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.TAB_TRAVERSAL )
		bSizer101.Add( self.m_MuRightPanel, 1, wx.EXPAND |wx.ALL, 5 )
		
		
		self.m_MuPanel.SetSizer( bSizer101 )
		self.m_MuPanel.Layout()
		bSizer101.Fit( self.m_MuPanel )
		self.m_MuChiNotebook.AddPage( self.m_MuPanel, u"Mu(E)", True )
		self.m_ChiPanel = wx.Panel( self.m_MuChiNotebook, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.TAB_TRAVERSAL, u"m_ChiPanel" )
		bSizer14 = wx.BoxSizer( wx.HORIZONTAL )
		
		self.m_ChiLeftPanel = wx.Panel( self.m_ChiPanel, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.TAB_TRAVERSAL )
		bSizer14.Add( self.m_ChiLeftPanel, 1, wx.EXPAND |wx.ALL, 5 )
		
		self.m_ChiRightPanel = wx.Panel( self.m_ChiPanel, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.TAB_TRAVERSAL )
		bSizer14.Add( self.m_ChiRightPanel, 1, wx.EXPAND |wx.ALL, 5 )
		
		
		self.m_ChiPanel.SetSizer( bSizer14 )
		self.m_ChiPanel.Layout()
		bSizer14.Fit( self.m_ChiPanel )
		self.m_MuChiNotebook.AddPage( self.m_ChiPanel, u"Chi(k)", False )
		self.m_OverplotPanel = wx.Panel( self.m_MuChiNotebook, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.TAB_TRAVERSAL, u"m_OverplotPanel" )
		bSizer141 = wx.BoxSizer( wx.HORIZONTAL )

		self.m_OverplotLeftPanel = wx.Panel( self.m_OverplotPanel, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.TAB_TRAVERSAL )
		bSizer141.Add( self.m_OverplotLeftPanel, 1, wx.EXPAND |wx.ALL, 5 )

		self.m_OverplotRightPanel = wx.Panel( self.m_OverplotPanel, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.TAB_TRAVERSAL )
		bSizer141.Add( self.m_OverplotRightPanel, 1, wx.EXPAND |wx.ALL, 5 )


		self.m_OverplotPanel.SetSizer( bSizer141 )
		self.m_OverplotPanel.Layout()
		bSizer141.Fit( self.m_OverplotPanel )
		self.m_MuChiNotebook.AddPage( self.m_OverplotPanel, u"MultiPlot", False )

		bSizer7.Add( self.m_MuChiNotebook, 1, wx.EXPAND |wx.ALL, 0 )
		
		
		self.m_LowerRightPanel.SetSizer( bSizer7 )
		self.m_LowerRightPanel.Layout()
		bSizer7.Fit( self.m_LowerRightPanel )
		self.m_splitter1.SplitHorizontally( self.m_UpperRightPanel, self.m_LowerRightPanel, 300 )
		bRightPanelSizer.Add( self.m_splitter1, 1, wx.EXPAND, 0 )
		
		
		self.m_RightPanel.SetSizer( bRightPanelSizer )
		self.m_RightPanel.Layout()
		bRightPanelSizer.Fit( self.m_RightPanel )
		bMainFrameSizer.Add( self.m_RightPanel, 1, wx.EXPAND |wx.ALL, 5 )
		
		
		self.m_MainPanel.SetSizer( bMainFrameSizer )
		self.m_MainPanel.Layout()
		bMainFrameSizer.Fit( self.m_MainPanel )
		bMainSizer.Add( self.m_MainPanel, 1, wx.EXPAND |wx.ALL, 0 )
		
		
		self.SetSizer( bMainSizer )
		self.Layout()
		self.m_statusBar = self.CreateStatusBar( 1, wx.ST_SIZEGRIP, wx.ID_ANY )
		
		self.Centre( wx.BOTH )
		
		# Connect Events
		self.Bind( wx.EVT_CLOSE, self.OnClick_Exit )
		self.Bind( wx.EVT_TOOL, self.OnClick_Load, id = self.m_LoadTool.GetId() )
		self.Bind( wx.EVT_TOOL, self.OnClick_Save, id = self.m_SaveTool.GetId() )
		self.Bind( wx.EVT_TOOL, self.OnClick_Unload, id = self.m_UnloadTool.GetId() )
		self.Bind( wx.EVT_TOOL, self.OnClick_Exit, id = self.m_ExitTool.GetId() )
		self.m_checkList_Spectra.Bind( wx.EVT_LISTBOX, self.OnCheckList_SpecSelect )
		self.m_checkList_Spectra.Bind( wx.EVT_CHECKLISTBOX, self.OnCheckList_SpecToggle )
		self.m_listBox_Edge.Bind( wx.EVT_LISTBOX, self.OnList_EdgeSelect )
		self.m_radioBtn_Correl.Bind( wx.EVT_RADIOBUTTON, self.OnRadioBtn_Correl )
		self.m_radioBtn_Weights.Bind( wx.EVT_RADIOBUTTON, self.OnRadioBtn_Weights )
		self.m_radioBtn_DetInt.Bind( wx.EVT_RADIOBUTTON, self.OnRadioBtn_TCR )
		self.m_radioBox1.Bind( wx.EVT_RADIOBOX, self.OnRadioBoxBtn_WeightFactor )
		self.m_radioBox2.Bind( wx.EVT_RADIOBOX, self.OnRadioBoxBtn_DeadTime )
		self.m_UpperNotebook.Bind( wx.EVT_NOTEBOOK_PAGE_CHANGING, self.OnChanging_UpperNotebook )
		self.m_panelTopLeft.Bind( wx.EVT_SIZE, self.OnSize_MuAverageCanvas )
		self.m_panelTopRight.Bind( wx.EVT_SIZE, self.OnSize_ChiAverageCanvas )
		self.m_SpectrumPlotPanel.Bind( wx.EVT_SIZE, self.OnSize_SpectrumPlotCanvas )
		self.m_RoiLowSlider.Bind( wx.EVT_SCROLL, self.OnSetRoi )
		self.m_RoiLowSpinCtrl.Bind( wx.EVT_SPINCTRL, self.OnSetRoi )
		self.m_RoiHighSlider.Bind( wx.EVT_SCROLL, self.OnSetRoi )
		self.m_RoiHighSpinCtrl.Bind( wx.EVT_SPINCTRL, self.OnSetRoi )
		self.m_bpRefreshButton.Bind( wx.EVT_BUTTON, self.OnClick_RefreshButton )
		self.m_bpLogLinButton.Bind( wx.EVT_BUTTON, self.OnClick_LogLinButton )
		self.m_StepSlider.Bind( wx.EVT_SCROLL, self.OnScroll_StepSlider )
		self.m_StepSpinCtrl.Bind( wx.EVT_SPINCTRL, self.OnSpinCtrl_StepSpinCtrl )
		self.m_MuLeftPanel.Bind( wx.EVT_SIZE, self.OnSize_MuLeftCanvas )
		self.m_MuRightPanel.Bind( wx.EVT_SIZE, self.OnSize_MuRightCanvas )
		self.m_ChiLeftPanel.Bind( wx.EVT_SIZE, self.OnSize_ChiLeftCanvas )
		self.m_ChiRightPanel.Bind( wx.EVT_SIZE, self.OnSize_ChiRightCanvas )
		self.m_OverplotLeftPanel.Bind( wx.EVT_SIZE, self.OnSize_OverplotLeftCanvas )
		self.m_OverplotRightPanel.Bind( wx.EVT_SIZE, self.OnSize_OverplotRightCanvas )

	def __del__( self ):
		pass
	
	
	# Virtual event handlers, overide them in your derived class
	def OnClick_Exit( self, event ):
		event.Skip()
	
	def OnClick_Load( self, event ):
		event.Skip()
	
	def OnClick_Save( self, event ):
		event.Skip()
	
	def OnClick_Unload( self, event ):
		event.Skip()
	
	
	def OnCheckList_SpecSelect( self, event ):
		event.Skip()
	
	def OnCheckList_SpecToggle( self, event ):
		event.Skip()
	
	def OnList_EdgeSelect( self, event ):
		event.Skip()
	
	def OnRadioBtn_Correl( self, event ):
		event.Skip()
	
	def OnRadioBtn_Weights( self, event ):
		event.Skip()
	
	def OnRadioBtn_TCR( self, event ):
		event.Skip()
	
	def OnRadioBoxBtn_WeightFactor( self, event ):
		event.Skip()

	def OnRadioBoxBtn_DeadTime( self, event ):
		event.Skip()

	def OnChanging_UpperNotebook( self, event ):
		event.Skip()
	
	def OnSize_MuAverageCanvas( self, event ):
		event.Skip()
	
	def OnSize_ChiAverageCanvas( self, event ):
		event.Skip()
	
	def OnSize_SpectrumPlotCanvas( self, event ):
		event.Skip()
	
	def OnSetRoi( self, event ):
		event.Skip()
	
	
	
	
	def OnClick_RefreshButton( self, event ):
		event.Skip()
	
	def OnClick_LogLinButton( self, event ):
		event.Skip()
	
	def OnScroll_StepSlider( self, event ):
		event.Skip()
	
	def OnSpinCtrl_StepSpinCtrl( self, event ):
		event.Skip()
	
	def OnSize_MuLeftCanvas( self, event ):
		event.Skip()
	
	def OnSize_MuRightCanvas( self, event ):
		event.Skip()
	
	def OnSize_ChiLeftCanvas( self, event ):
		event.Skip()
	
	def OnSize_ChiRightCanvas( self, event ):
		event.Skip()
	
	def OnSize_OverplotLeftCanvas( self, event ):
		event.Skip()

	def OnSize_OverplotRightCanvas( self, event ):
		event.Skip()

	def m_splitter1OnIdle( self, event ):
		self.m_splitter1.SetSashPosition( 300 )
		self.m_splitter1.Unbind( wx.EVT_IDLE )
	

