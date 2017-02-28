# -*- coding: utf-8 -*- 

###########################################################################
## Python code generated with wxFormBuilder (version Jun 17 2015)
## http://www.wxformbuilder.org/
##
## PLEASE DO "NOT" EDIT THIS FILE!
###########################################################################

import wx
import wx.xrc

###########################################################################
## Class MyFrame2
###########################################################################

class MyFrame2 ( wx.Frame ):
	
	def __init__( self, parent ):
		wx.Frame.__init__ ( self, parent, id = wx.ID_ANY, title = wx.EmptyString, pos = wx.DefaultPosition, size = wx.Size( 526,520 ), style = wx.DEFAULT_FRAME_STYLE|wx.TAB_TRAVERSAL )
		
		self.SetSizeHintsSz( wx.DefaultSize, wx.DefaultSize )
		
		bSizer12 = wx.BoxSizer( wx.VERTICAL )
		
		self.m_panel2 = wx.Panel( self, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.TAB_TRAVERSAL )
		bSizer13 = wx.BoxSizer( wx.VERTICAL )
		
		bSizer14 = wx.BoxSizer( wx.HORIZONTAL )
		
		bSizer15 = wx.BoxSizer( wx.VERTICAL )
		
		sbSizer3 = wx.StaticBoxSizer( wx.StaticBox( self.m_panel2, wx.ID_ANY, u"Component" ), wx.VERTICAL )
		
		fgSizer3 = wx.FlexGridSizer( 0, 2, 0, 0 )
		fgSizer3.SetFlexibleDirection( wx.BOTH )
		fgSizer3.SetNonFlexibleGrowMode( wx.FLEX_GROWMODE_SPECIFIED )
		
		self.m_staticText10 = wx.StaticText( sbSizer3.GetStaticBox(), wx.ID_ANY, u"Manufacturer", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_staticText10.Wrap( -1 )
		fgSizer3.Add( self.m_staticText10, 0, wx.ALL|wx.ALIGN_RIGHT, 5 )
		
		self.manufacturer_text = wx.TextCtrl( sbSizer3.GetStaticBox(), wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.DefaultSize, 0 )
		fgSizer3.Add( self.manufacturer_text, 1, wx.ALL|wx.EXPAND, 5 )
		
		self.m_staticText11 = wx.StaticText( sbSizer3.GetStaticBox(), wx.ID_ANY, u"Product Number", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_staticText11.Wrap( -1 )
		fgSizer3.Add( self.m_staticText11, 0, wx.ALL|wx.ALIGN_RIGHT, 5 )
		
		self.product_number_text = wx.TextCtrl( sbSizer3.GetStaticBox(), wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.DefaultSize, 0 )
		fgSizer3.Add( self.product_number_text, 1, wx.ALL|wx.EXPAND, 5 )
		
		self.m_staticText12 = wx.StaticText( sbSizer3.GetStaticBox(), wx.ID_ANY, u"Calibration Number", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_staticText12.Wrap( -1 )
		fgSizer3.Add( self.m_staticText12, 0, wx.ALL|wx.ALIGN_RIGHT, 5 )
		
		self.calibration_number_text = wx.TextCtrl( sbSizer3.GetStaticBox(), wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.DefaultSize, 0 )
		fgSizer3.Add( self.calibration_number_text, 1, wx.ALL|wx.EXPAND, 5 )
		
		self.m_staticText16 = wx.StaticText( sbSizer3.GetStaticBox(), wx.ID_ANY, u"Serial Number", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_staticText16.Wrap( -1 )
		fgSizer3.Add( self.m_staticText16, 0, wx.ALL|wx.ALIGN_RIGHT, 5 )
		
		self.serial_number_component_text = wx.TextCtrl( sbSizer3.GetStaticBox(), wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.DefaultSize, 0 )
		fgSizer3.Add( self.serial_number_component_text, 1, wx.ALL|wx.EXPAND, 5 )
		
		self.m_staticText17 = wx.StaticText( sbSizer3.GetStaticBox(), wx.ID_ANY, u"Firmware Version", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_staticText17.Wrap( -1 )
		fgSizer3.Add( self.m_staticText17, 0, wx.ALL|wx.ALIGN_RIGHT, 5 )
		
		self.firmware_text = wx.TextCtrl( sbSizer3.GetStaticBox(), wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.DefaultSize, 0 )
		fgSizer3.Add( self.firmware_text, 1, wx.ALL|wx.EXPAND, 5 )
		
		bSizer17 = wx.BoxSizer( wx.VERTICAL )
		
		
		fgSizer3.Add( bSizer17, 1, wx.EXPAND, 5 )
		
		bSizer19 = wx.BoxSizer( wx.HORIZONTAL )
		
		self.m_button9 = wx.Button( sbSizer3.GetStaticBox(), wx.ID_ANY, u"Submit", wx.DefaultPosition, wx.DefaultSize, 0 )
		bSizer19.Add( self.m_button9, 0, wx.ALL, 5 )
		
		self.m_button10 = wx.Button( sbSizer3.GetStaticBox(), wx.ID_ANY, u"Clear", wx.DefaultPosition, wx.DefaultSize, 0 )
		bSizer19.Add( self.m_button10, 0, wx.ALL, 5 )
		
		
		fgSizer3.Add( bSizer19, 1, wx.EXPAND, 5 )
		
		
		sbSizer3.Add( fgSizer3, 1, wx.EXPAND|wx.ALIGN_RIGHT, 5 )
		
		
		bSizer15.Add( sbSizer3, 1, wx.EXPAND, 5 )
		
		sbSizer4 = wx.StaticBoxSizer( wx.StaticBox( self.m_panel2, wx.ID_ANY, u"Tower" ), wx.VERTICAL )
		
		fgSizer4 = wx.FlexGridSizer( 0, 2, 0, 0 )
		fgSizer4.SetFlexibleDirection( wx.BOTH )
		fgSizer4.SetNonFlexibleGrowMode( wx.FLEX_GROWMODE_SPECIFIED )
		
		self.m_staticText13 = wx.StaticText( sbSizer4.GetStaticBox(), wx.ID_ANY, u"Name", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_staticText13.Wrap( -1 )
		fgSizer4.Add( self.m_staticText13, 0, wx.ALL|wx.ALIGN_RIGHT, 5 )
		
		self.tower_name_text = wx.TextCtrl( sbSizer4.GetStaticBox(), wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.DefaultSize, 0 )
		fgSizer4.Add( self.tower_name_text, 0, wx.ALL|wx.EXPAND, 5 )
		
		self.m_staticText14 = wx.StaticText( sbSizer4.GetStaticBox(), wx.ID_ANY, u"Serial Number", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_staticText14.Wrap( -1 )
		fgSizer4.Add( self.m_staticText14, 0, wx.ALL|wx.ALIGN_RIGHT, 5 )
		
		self.serial_number_tower_text = wx.TextCtrl( sbSizer4.GetStaticBox(), wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.DefaultSize, 0 )
		fgSizer4.Add( self.serial_number_tower_text, 0, wx.ALL|wx.EXPAND, 5 )
		
		self.m_staticText15 = wx.StaticText( sbSizer4.GetStaticBox(), wx.ID_ANY, u"ID In Company", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_staticText15.Wrap( -1 )
		fgSizer4.Add( self.m_staticText15, 0, wx.ALL|wx.ALIGN_RIGHT, 5 )
		
		self.id_tower_text = wx.TextCtrl( sbSizer4.GetStaticBox(), wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.DefaultSize, 0 )
		fgSizer4.Add( self.id_tower_text, 0, wx.ALL|wx.EXPAND, 5 )
		
		self.m_staticText18 = wx.StaticText( sbSizer4.GetStaticBox(), wx.ID_ANY, u"Geolocation", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_staticText18.Wrap( -1 )
		fgSizer4.Add( self.m_staticText18, 0, wx.ALL|wx.ALIGN_RIGHT, 5 )
		
		self.location_text = wx.TextCtrl( sbSizer4.GetStaticBox(), wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.DefaultSize, 0 )
		fgSizer4.Add( self.location_text, 0, wx.ALL|wx.EXPAND, 5 )
		
		self.m_staticText19 = wx.StaticText( sbSizer4.GetStaticBox(), wx.ID_ANY, u"Alias", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_staticText19.Wrap( -1 )
		fgSizer4.Add( self.m_staticText19, 0, wx.ALL|wx.ALIGN_RIGHT, 5 )
		
		self.tower_alias_text = wx.TextCtrl( sbSizer4.GetStaticBox(), wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.DefaultSize, 0 )
		fgSizer4.Add( self.tower_alias_text, 0, wx.ALL|wx.EXPAND, 5 )
		
		bSizer20 = wx.BoxSizer( wx.VERTICAL )
		
		
		fgSizer4.Add( bSizer20, 1, wx.EXPAND, 5 )
		
		bSizer21 = wx.BoxSizer( wx.HORIZONTAL )
		
		self.m_button7 = wx.Button( sbSizer4.GetStaticBox(), wx.ID_ANY, u"Submit", wx.DefaultPosition, wx.DefaultSize, 0 )
		bSizer21.Add( self.m_button7, 0, wx.ALL, 5 )
		
		self.m_button8 = wx.Button( sbSizer4.GetStaticBox(), wx.ID_ANY, u"Clear", wx.DefaultPosition, wx.DefaultSize, 0 )
		bSizer21.Add( self.m_button8, 0, wx.ALL, 5 )
		
		
		fgSizer4.Add( bSizer21, 1, wx.ALIGN_RIGHT, 5 )
		
		
		sbSizer4.Add( fgSizer4, 1, wx.ALIGN_RIGHT, 5 )
		
		
		bSizer15.Add( sbSizer4, 1, wx.EXPAND, 5 )
		
		
		bSizer14.Add( bSizer15, 1, wx.EXPAND, 5 )
		
		bSizer16 = wx.BoxSizer( wx.VERTICAL )
		
		self.tree_control = wx.TreeCtrl( self.m_panel2, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.TR_DEFAULT_STYLE )
		bSizer16.Add( self.tree_control, 1, wx.ALL|wx.EXPAND, 5 )
		
		
		bSizer14.Add( bSizer16, 1, wx.EXPAND, 5 )
		
		
		bSizer13.Add( bSizer14, 1, wx.EXPAND, 5 )
		
		
		self.m_panel2.SetSizer( bSizer13 )
		self.m_panel2.Layout()
		bSizer13.Fit( self.m_panel2 )
		bSizer12.Add( self.m_panel2, 1, wx.EXPAND |wx.ALL, 5 )
		
		
		self.SetSizer( bSizer12 )
		self.Layout()
		
		self.Centre( wx.BOTH )
		
		# Connect Events
		self.m_button9.Bind( wx.EVT_BUTTON, self.component_submit )
		self.m_button10.Bind( wx.EVT_BUTTON, self.component_clear )
		self.m_button7.Bind( wx.EVT_BUTTON, self.tower_submit )
		self.m_button8.Bind( wx.EVT_BUTTON, self.tower_clear )
	
	def __del__( self ):
		pass
	
	
	# Virtual event handlers, overide them in your derived class
	def component_submit( self, event ):
		event.Skip()
	
	def component_clear( self, event ):
		event.Skip()
	
	def tower_submit( self, event ):
		event.Skip()
	
	def tower_clear( self, event ):
		event.Skip()
	

