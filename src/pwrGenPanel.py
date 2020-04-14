#!/usr/bin/python
#-----------------------------------------------------------------------------
# Name:        uiPanel.py
#
# Purpose:     This module is used to create different function panels.
# Author:      Yuancheng Liu
#
# Created:     2020/01/10
# Copyright:   YC @ Singtel Cyber Security Research & Development Laboratory
# License:     YC
#-----------------------------------------------------------------------------
import wx
from math import sin, cos, radians, pi


from datetime import datetime
import pwrGenGobal as gv

#-----------------------------------------------------------------------------
#-----------------------------------------------------------------------------
class PanelMoto(wx.Panel):
    """ Panel to display image. """

    def __init__(self, parent, panelSize=(120, 120)):
        wx.Panel.__init__(self, parent, size=panelSize)
        self.SetBackgroundColour(wx.Colour(200, 200, 200))
        self.panelSize = panelSize
        self.bmp = wx.Bitmap(gv.MOIMG_PATH, wx.BITMAP_TYPE_ANY)
        self.Bind(wx.EVT_PAINT, self.onPaint)
        self.SetDoubleBuffered(True)
        self.angle = 0 

#--PanelImge--------------------------------------------------------------------
    def onPaint(self, evt):
        """ Draw the map on the panel."""
        dc = wx.PaintDC(self)
        w, h = self.panelSize
        dc.DrawBitmap(self._scaleBitmap(self.bmp, w, h), 0, 0)
        motoSp = 30 # gv.iGnMgr.getMotorSp()
        color = 'GREEN'
        if motoSp < 50 : 
            color = 'YELLOW'
        elif motoSp > 50: 
            color = 'RED'
        
        dc.SetPen(wx.Pen(color, width=5, style=wx.PENSTYLE_SOLID))
        dc.DrawText(str(motoSp), 5, 5)
        dc.DrawLine(w//2, h//2, int(w//2+60*sin(radians(self.angle))), 
                     int(h//2-60*cos(radians(self.angle))))
        
        # dc.DrawLine(int(w//2+60*sin(radians(self.angle))), 
        #             int(h//2-60*cos(radians(self.angle))),
        #             int(w//2+60*sin(radians(self.angle+180))), 
        #             int(h//2-60*cos(radians(self.angle+180))),
        #             )

        # dc.DrawLine(int(w//2+60*sin(radians(self.angle+90))), 
        #     int(h//2-60*cos(radians(self.angle+90))),
        #     int(w//2+60*sin(radians(self.angle+270))), 
        #     int(h//2-60*cos(radians(self.angle+270))),
        #     )

#--PanelImge--------------------------------------------------------------------
    def _scaleBitmap(self, bitmap, width, height):
        """ Resize a input bitmap.(bitmap-> image -> resize image -> bitmap)"""
        #image = wx.ImageFromBitmap(bitmap) # used below 2.7
        image = bitmap.ConvertToImage()
        image = image.Scale(width, height, wx.IMAGE_QUALITY_HIGH)
        #result = wx.BitmapFromImage(image) # used below 2.7
        result = wx.Bitmap(image, depth=wx.BITMAP_SCREEN_DEPTH)
        return result

#--PanelImge--------------------------------------------------------------------
    def _scaleBitmap2(self, bitmap, width, height):
        """ Resize a input bitmap.(bitmap-> image -> resize image -> bitmap)"""
        image = wx.ImageFromBitmap(bitmap) # used below 2.7
        image = image.Scale(width, height, wx.IMAGE_QUALITY_HIGH)
        result = wx.BitmapFromImage(image) # used below 2.7
        return result

#--PanelImge--------------------------------------------------------------------
    def updateBitmap(self, bitMap):
        """ Update the panel bitmap image."""
        if not bitMap: return
        self.bmp = bitMap

#--PanelMap--------------------------------------------------------------------
    def updateDisplay(self, updateFlag=None):
        """ Set/Update the display: if called as updateDisplay() the function will 
            update the panel, if called as updateDisplay(updateFlag=?) the function
            will set the self update flag.
        """
        ang = 30 + (30-50)*5
        self.angle += ang 
        self.angle = self.angle%360
        self.Refresh(False)
        self.Update()

#-----------------------------------------------------------------------------
#-----------------------------------------------------------------------------
class PanelPump(wx.Panel):
    """ Panel to display image. """

    def __init__(self, parent, panelSize=(120, 120)):
        wx.Panel.__init__(self, parent, size=panelSize)
        self.SetBackgroundColour(wx.Colour(200, 200, 200))
        self.panelSize = panelSize
        self.bmp = wx.Bitmap(gv.PUIMG_PATH, wx.BITMAP_TYPE_ANY)
        self.Bind(wx.EVT_PAINT, self.onPaint)
        self.SetDoubleBuffered(True)
        self.maxVal = 50
        self.pos = 50

#--PanelImge--------------------------------------------------------------------
    def onPaint(self, evt):
        """ Draw the map on the panel."""
        dc = wx.PaintDC(self)
        w, h = self.panelSize
        dc.DrawBitmap(self._scaleBitmap(self.bmp, w, h), 0, 0)
        dc.SetPen(wx.Pen('BLACK'))
        textList = ('Neutral', 'Lower', 'Medium', 'Higher')
        dc.DrawText(textList[1], 5, 5)
        colorList = ('GRAy','YELLOW', '#36ff27', 'RED')
        rect = self.pos / 5
        for i in range(1, 21):
            if i < rect:
                dc.SetBrush(wx.Brush('#075100'))
                dc.DrawRectangle(88, i*3+27, 25, 4)
            else:
                dc.SetBrush(wx.Brush(colorList[1]))
                dc.DrawRectangle(88, i*3+27, 25, 4)

#--PanelImge--------------------------------------------------------------------
    def _scaleBitmap(self, bitmap, width, height):
        """ Resize a input bitmap.(bitmap-> image -> resize image -> bitmap)"""
        #image = wx.ImageFromBitmap(bitmap) # used below 2.7
        image = bitmap.ConvertToImage()
        image = image.Scale(width, height, wx.IMAGE_QUALITY_HIGH)
        #result = wx.BitmapFromImage(image) # used below 2.7
        result = wx.Bitmap(image, depth=wx.BITMAP_SCREEN_DEPTH)
        return result

#--PanelImge--------------------------------------------------------------------
    def _scaleBitmap2(self, bitmap, width, height):
        """ Resize a input bitmap.(bitmap-> image -> resize image -> bitmap)"""
        image = wx.ImageFromBitmap(bitmap) # used below 2.7
        image = image.Scale(width, height, wx.IMAGE_QUALITY_HIGH)
        result = wx.BitmapFromImage(image) # used below 2.7
        return result

#--PanelImge--------------------------------------------------------------------
    def updateBitmap(self, bitMap):
        """ Update the panel bitmap image."""
        if not bitMap: return
        self.bmp = bitMap

#--PanelMap--------------------------------------------------------------------
    def updateDisplay(self, updateFlag=None):
        """ Set/Update the display: if called as updateDisplay() the function will 
            update the panel, if called as updateDisplay(updateFlag=?) the function
            will set the self update flag.
        """
        maxValList = (10,30, 50, 80)
        addValList = (5, 5, 10, 15) 
        self.maxVal = maxValList[gv.iGnMgr.getPumpSp()]
        addVal = addValList[gv.iGnMgr.getPumpSp()]
        if self.pos < 100 - self.maxVal:
            self.pos = 100
        else:
            self.pos -= addVal
        self.Refresh(False)
        self.Update()

#-----------------------------------------------------------------------------
class PanelLoad(wx.Panel):
    """ Panel to show the load situation."""

    def __init__(self, parent):
        wx.Panel.__init__(self, parent)
        self.SetBackgroundColour(wx.Colour(200, 210, 200))
        self.loadBtDict = {   'Indu': None,      # Industry area
                            'Airp': None,      # Air port
                            'Resi': None,      # Residential area
                            'Stat': None,      # Stataion power
                            'TrkA': None,      # Track A power
                            'TrkB': None,      # Track B power
                            'City': None,      # City power
                         }

        self.SetSizer(self._buidUISizer())

#-----------------------------------------------------------------------------
    def _buidUISizer(self):
        """ build the control panel sizer. """
        flagsR = wx.RIGHT | wx.ALIGN_CENTER_VERTICAL
        sizerAll = wx.BoxSizer(wx.VERTICAL)
        sizerAll.Add(wx.StaticText(self, -1, 'System Load Indicators:'), flag=flagsR, border=2)
        sizerAll.AddSpacer(10)
        #sizer = wx.GridSizer(8, 2, 4, 4)
        sizer = wx.FlexGridSizer(7, 2, 4, 4)
        lbStrList = ('Inductrial Area [PLC1] : ', 
                    'Airport Area [PLC1] : ',
                    'Residential Area [PLC2] : ',
                    'Train Station [PLC2] : ',
                    'Railway Track A [PLC3] : ',
                    'Railway Track B [PLC3] : ',
                    'City Area Power [PLC3] : ')
        btKeyList = ('Indu', 'Airp', 'Resi', 'Stat', 'TrkA', 'TrkB', 'City')
        for i in range(7):
            sizer.Add(wx.StaticText(self, -1, lbStrList[i]))
            self.loadBtDict[btKeyList[i]] = wx.Button(self, label='OFF', size=(60, 21))
            self.loadBtDict[btKeyList[i]].SetBackgroundColour(wx.Colour('GRAY'))
            sizer.Add(self.loadBtDict[btKeyList[i]])
        sizerAll.Add(sizer, flag=flagsR, border=2)
        return sizerAll 

#-----------------------------------------------------------------------------
    def setLoadIndicator(self, loadDict):
        """ Set the load indicators.
        """
        for keyStr in loadDict.keys():
            if keyStr in self.loadBtDict.keys():
                (btLb, btColor) = ('ON ', 'GREEN') if loadDict[keyStr] else ('OFF', 'GRAY')
                self.loadBtDict[keyStr].SetLabel(btLb)
                self.loadBtDict[keyStr].SetBackgroundColour(wx.Colour(btColor))
        self.Refresh(False)

#-----------------------------------------------------------------------------
#-----------------------------------------------------------------------------
class PanelCtrl(wx.Panel):
    """ Function control panel."""

    def __init__(self, parent):
        wx.Panel.__init__(self, parent)
        self.SetBackgroundColour(wx.Colour(200, 210, 200))
        self.gpsPos = None
        self.SetSizer(self._buidUISizer())

#--PanelCtrl-------------------------------------------------------------------
    def _buidUISizer(self):
        """ build the control panel sizer. """
        flagsR = wx.RIGHT 
        ctSizer = wx.BoxSizer(wx.VERTICAL)
        ctSizer.AddSpacer(10)
        # Row idx 0: show the search key and map zoom in level.
        ctSizer.Add(wx.StaticText(self, label=" System Power".ljust(15)),
                  flag=flagsR, border=2)

        ctSizer.AddSpacer(10)
        self.smkIdc = wx.Button(self, label='All Sensor Pwr  ', size=(120, 30))
        self.smkIdc.SetBackgroundColour(wx.Colour('GRAY'))
        ctSizer.Add(self.smkIdc, flag=flagsR, border=2)
        ctSizer.AddSpacer(10)

        self.sirenIdc = wx.Button(self, label='System Main Pwr ', size=(120, 30))
        self.sirenIdc.SetBackgroundColour(wx.Colour('RED'))
        ctSizer.Add(self.sirenIdc, flag=flagsR, border=2)
        ctSizer.AddSpacer(10)
        
        self.debugBt = wx.Button(self, label='Debug Panel >> ', size=(120, 30))
        ctSizer.Add(self.debugBt, flag=flagsR, border=2)
        
        return ctSizer
