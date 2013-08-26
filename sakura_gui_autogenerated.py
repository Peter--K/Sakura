# -*- coding: utf-8 -*- 

###########################################################################
## Python code generated with wxFormBuilder (version Oct  8 2012)
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
		wx.Frame.__init__ ( self, parent, id = wx.ID_ANY, title = u"-- Sakura --", pos = wx.DefaultPosition, size = wx.Size( 998,699 ), style = wx.DEFAULT_FRAME_STYLE|wx.TAB_TRAVERSAL )
		
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
		self.m_toolBar1.AddLabelTool( id_load, u"Load", wx.Bitmap( u"resources/folder_vertical_open.png", wx.BITMAP_TYPE_ANY ), wx.NullBitmap, wx.ITEM_NORMAL, u"Load", wx.EmptyString, None ) 
		
		self.m_toolBar1.AddLabelTool( id_save, u"Save", wx.Bitmap( u"resources/disk.png", wx.BITMAP_TYPE_ANY ), wx.NullBitmap, wx.ITEM_NORMAL, u"Save", wx.EmptyString, None ) 
		
		self.m_toolBar1.AddLabelTool( id_unload, u"Unload", wx.Bitmap( u"resources/folder_vertical_torn.png", wx.BITMAP_TYPE_ANY ), wx.NullBitmap, wx.ITEM_NORMAL, u"Unload", wx.EmptyString, None ) 
		
		self.m_toolBar1.Realize() 
		
		fgSizer1.Add( self.m_toolBar1, 0, wx.EXPAND, 5 )
		
		self.m_toolBar2 = wx.ToolBar( self.m_ToolPanel, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.TB_HORIZONTAL )
		self.m_toolBar2.SetToolBitmapSize( wx.Size( 16,16 ) )
		self.m_toolBar2.AddSeparator()
		
		self.m_toolBar2.Realize() 
		
		fgSizer1.Add( self.m_toolBar2, 0, wx.EXPAND, 5 )
		
		self.m_toolBar3 = wx.ToolBar( self.m_ToolPanel, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.TB_HORIZONTAL )
		self.m_toolBar3.SetToolBitmapSize( wx.Size( 16,16 ) )
		self.m_toolBar3.AddLabelTool( id_exit, u"Exit", wx.Bitmap( u"resources/door_in.png", wx.BITMAP_TYPE_ANY ), wx.NullBitmap, wx.ITEM_NORMAL, u"Exit", wx.EmptyString, None ) 
		
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
		bSizer6.Add( self.m_checkList_Spectra, 2, wx.ALL, 5 )
		
		m_listBox_EdgeChoices = [ u"V-K", u"Cr-K", u"Mn-K", u"Fe-K", u"Co-K", u"Ni-K", u"Cu-K", u"Zn-K", u"Au-L3", u"Au-L2", u"Au-L1" ]
		self.m_listBox_Edge = wx.ListBox( self.m_FormPanel, wx.ID_ANY, wx.DefaultPosition, wx.Size( -1,-1 ), m_listBox_EdgeChoices, 0 )
		self.m_listBox_Edge.SetFont( wx.Font( wx.NORMAL_FONT.GetPointSize(), 70, 90, 90, False, wx.EmptyString ) )
		
		bSizer6.Add( self.m_listBox_Edge, 1, wx.ALL, 5 )
		
		
		self.m_FormPanel.SetSizer( bSizer6 )
		self.m_FormPanel.Layout()
		bSizer6.Fit( self.m_FormPanel )
		bLeftPanelSizer.Add( self.m_FormPanel, 1, wx.EXPAND |wx.ALL, 5 )
		
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
		
		self.m_notebook6 = wx.Notebook( self.m_UpperRightPanel, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.NB_LEFT )
		self.m_AvgsPanel = wx.Panel( self.m_notebook6, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.TAB_TRAVERSAL )
		bAvgsSizer = wx.BoxSizer( wx.HORIZONTAL )
		
		self.m_panelMuAverage = wx.Panel( self.m_AvgsPanel, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.TAB_TRAVERSAL )
		bAvgsSizer.Add( self.m_panelMuAverage, 1, wx.EXPAND |wx.ALL, 5 )
		
		self.m_panelChiAverage = wx.Panel( self.m_AvgsPanel, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.TAB_TRAVERSAL )
		bAvgsSizer.Add( self.m_panelChiAverage, 1, wx.EXPAND |wx.ALL, 5 )
		
		
		self.m_AvgsPanel.SetSizer( bAvgsSizer )
		self.m_AvgsPanel.Layout()
		bAvgsSizer.Fit( self.m_AvgsPanel )
		self.m_notebook6.AddPage( self.m_AvgsPanel, u"Avg", True )
		self.m_SpectrumPanel = wx.Panel( self.m_notebook6, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.TAB_TRAVERSAL )
		self.m_notebook6.AddPage( self.m_SpectrumPanel, u"Spectrum", False )
		
		bSizer61.Add( self.m_notebook6, 1, wx.EXPAND |wx.ALL, 0 )
		
		
		self.m_UpperRightPanel.SetSizer( bSizer61 )
		self.m_UpperRightPanel.Layout()
		bSizer61.Fit( self.m_UpperRightPanel )
		self.m_LowerRightPanel = wx.Panel( self.m_splitter1, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.TAB_TRAVERSAL )
		bSizer7 = wx.BoxSizer( wx.VERTICAL )
		
		self.m_MuChiNotebook = wx.Notebook( self.m_LowerRightPanel, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.NB_LEFT )
		self.m_MuPanel = wx.Panel( self.m_MuChiNotebook, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.TAB_TRAVERSAL )
		bSizer101 = wx.BoxSizer( wx.HORIZONTAL )
		
		self.m_MuLeftPanel = wx.Panel( self.m_MuPanel, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.TAB_TRAVERSAL )
		bSizer101.Add( self.m_MuLeftPanel, 1, wx.EXPAND |wx.ALL, 5 )
		
		self.m_MuRightPanel = wx.Panel( self.m_MuPanel, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.TAB_TRAVERSAL )
		bSizer101.Add( self.m_MuRightPanel, 1, wx.EXPAND |wx.ALL, 5 )
		
		
		self.m_MuPanel.SetSizer( bSizer101 )
		self.m_MuPanel.Layout()
		bSizer101.Fit( self.m_MuPanel )
		self.m_MuChiNotebook.AddPage( self.m_MuPanel, u"Mu(E)", True )
		self.m_ChiPanel = wx.Panel( self.m_MuChiNotebook, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.TAB_TRAVERSAL )
		self.m_MuChiNotebook.AddPage( self.m_ChiPanel, u"Chi(k)", False )
		
		bSizer7.Add( self.m_MuChiNotebook, 1, wx.EXPAND |wx.ALL, 0 )
		
		
		self.m_LowerRightPanel.SetSizer( bSizer7 )
		self.m_LowerRightPanel.Layout()
		bSizer7.Fit( self.m_LowerRightPanel )
		self.m_splitter1.SplitHorizontally( self.m_UpperRightPanel, self.m_LowerRightPanel, 262 )
		bRightPanelSizer.Add( self.m_splitter1, 1, wx.EXPAND, 0 )
		
		self.m_toggleBtn_MuChi = wx.ToggleButton( self.m_RightPanel, wx.ID_ANY, u"chi(k)", wx.DefaultPosition, wx.DefaultSize, 0 )
		bRightPanelSizer.Add( self.m_toggleBtn_MuChi, 0, wx.ALL, 5 )
		
		
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
		self.Bind( wx.EVT_TOOL, self.OnClick_Load, id = id_load )
		self.Bind( wx.EVT_TOOL, self.OnClick_Save, id = id_save )
		self.Bind( wx.EVT_TOOL, self.OnClick_Unload, id = id_unload )
		self.Bind( wx.EVT_TOOL, self.OnClick_Exit, id = id_exit )
		self.m_checkList_Spectra.Bind( wx.EVT_LISTBOX, self.OnCheckList_SpecSelect )
		self.m_checkList_Spectra.Bind( wx.EVT_CHECKLISTBOX, self.OnCheckList_SpecToggle )
		self.m_listBox_Edge.Bind( wx.EVT_LISTBOX, self.OnList_EdgeSelect )
		self.m_radioBtn_Correl.Bind( wx.EVT_RADIOBUTTON, self.OnRadioBtn_Correl )
		self.m_radioBtn_Weights.Bind( wx.EVT_RADIOBUTTON, self.OnRadioBtn_Weights )
		self.m_radioBtn_DetInt.Bind( wx.EVT_RADIOBUTTON, self.OnRadioBtn_TCR )
		self.m_panelMuAverage.Bind( wx.EVT_SIZE, self.OnSize_MuAverageCanvas )
		self.m_panelChiAverage.Bind( wx.EVT_SIZE, self.OnSize_ChiAverageCanvas )
		self.m_MuLeftPanel.Bind( wx.EVT_SIZE, self.OnSize_MuLeftCanvas )
		self.m_MuRightPanel.Bind( wx.EVT_SIZE, self.OnSize_MuRightCanvas )
		self.m_toggleBtn_MuChi.Bind( wx.EVT_TOGGLEBUTTON, self.OnToggleMuChi )
	
	def __del__( self ):
		pass
	
	
	# Virtual event handlers, overide them in your derived class
	def OnClick_Load( self, event ):
		event.Skip()
	
	def OnClick_Save( self, event ):
		event.Skip()
	
	def OnClick_Unload( self, event ):
		event.Skip()
	
	def OnClick_Exit( self, event ):
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
	
	def OnSize_MuAverageCanvas( self, event ):
		event.Skip()
	
	def OnSize_ChiAverageCanvas( self, event ):
		event.Skip()
	
	def OnSize_MuLeftCanvas( self, event ):
		event.Skip()
	
	def OnSize_MuRightCanvas( self, event ):
		event.Skip()
	
	def OnToggleMuChi( self, event ):
		event.Skip()
	
	def m_splitter1OnIdle( self, event ):
		self.m_splitter1.SetSashPosition( 262 )
		self.m_splitter1.Unbind( wx.EVT_IDLE )
	

