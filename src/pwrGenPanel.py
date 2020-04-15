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
    """ Panel to show the moto rotation rate. """

    def __init__(self, parent, panelSize=(120, 120)):
        wx.Panel.__init__(self, parent, size=panelSize)
        self.SetBackgroundColour(wx.Colour(200, 200, 200))
        self.panelSize = panelSize
        self.bmp = wx.Bitmap(gv.MOIMG_PATH, wx.BITMAP_TYPE_ANY)
        self.Bind(wx.EVT_PAINT, self.onPaint)
        self.SetDoubleBuffered(True)
        self.angle = 0 # rotate indicator angle
        self.motoSpd = 'off'

    def setMotoSpeed(self, speed):
        if not (speed in ('off', 'slow', 'fast')): 
            print('PanelMoto : input speed value is invalid %s' %str(speed))
        else:
            self.motoSpd = speed

#--PanelImge--------------------------------------------------------------------
    def onPaint(self, evt):
        """ Draw the map on the panel."""
        dc = wx.PaintDC(self)
        w, h = self.panelSize
        # moto background.
        dc.DrawBitmap(self._scaleBitmap(self.bmp, w, h), 0, 0)
        dc.SetBrush(wx.Brush(wx.Colour('Black')))
        dc.DrawRectangle(1, 5, 30, 15)

        color = 'Gray'
        if self.motoSpd == 'slow':
            color = 'Green'
        elif self.motoSpd == 'fast':
            color = 'Yellow'        
        dc.SetPen(wx.Pen(color, width=5, style=wx.PENSTYLE_SOLID))
        dc.SetTextForeground(wx.Colour(color))
        #dc.SetFont(wx.Font(18, wx.DECORATIVE, wx.ITALIC, wx.NORMAL))
        
        dc.DrawText(str(self.motoSpd), 5, 5)
        dc.DrawLine(w//2, h//2, int(w//2+60*sin(radians(self.angle))), 
                     int(h//2-60*cos(radians(self.angle))))
        
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
        if self.motoSpd == 'off': return
        ang = 20 if self.motoSpd == 'slow' else 40
        self.angle = (self.angle + ang)%360
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
        self.maxVal = 50    # max pump line hight
        self.pos = 80       # pump line position (from top to buttom)
        self.pumpSpd = 'off'


    def setPumpSpeed(self, speed):
        if not (speed in ('off', 'slow', 'fast')): 
            print('PanelMoto : input speed value is invalid %s' %str(speed))
        else:
            self.pumpSpd = speed


#--PanelImge--------------------------------------------------------------------
    def onPaint(self, evt):
        """ Draw the map on the panel."""
        dc = wx.PaintDC(self)
        w, h = self.panelSize
        # pump back ground.
        dc.DrawBitmap(self._scaleBitmap(self.bmp, w, h), 0, 0)
        dc.SetBrush(wx.Brush(wx.Colour('Black')))
        dc.DrawRectangle(1, 5, 30, 15)

        color = 'Gray'
        if self.pumpSpd == 'slow':
            color = 'Green'
        elif self.pumpSpd == 'fast':
            color = 'Yellow'


        dc.SetPen(wx.Pen(color, width=5, style=wx.PENSTYLE_SOLID))
        dc.SetTextForeground(wx.Colour(color))
        dc.DrawText(str(self.pumpSpd), 5, 5)

        dc.SetPen(wx.Pen('BLACK'))

        rect = self.pos/5
        for i in range(1, 21):
            if i < rect:
                dc.SetBrush(wx.Brush('#075100'))
                dc.DrawRectangle(88, i*3+27, 25, 4)
            else:
                dc.SetBrush(wx.Brush(color))
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
        if self.pumpSpd == 'off':
            self.maxVal = 10
            return
        self.maxVal = 40 if self.pumpSpd == 'slow' else 80
        addVal = 10 if self.pumpSpd == 'slow' else 20
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
        self.debugFrame = None
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
        self.sensorPwBt = wx.Button(self, label='All Sensors Pwr  ', size=(120, 30))
        self.sensorPwBt.SetBackgroundColour(wx.Colour('Gray'))
        ctSizer.Add(self.sensorPwBt, flag=flagsR, border=2)
        ctSizer.AddSpacer(10)

        self.mainPwrBt = wx.Button(self, label='System Main Pwr ', size=(120, 30))
        self.mainPwrBt.SetBackgroundColour(wx.Colour('Gray'))
        ctSizer.Add(self.mainPwrBt, flag=flagsR, border=2)
        ctSizer.AddSpacer(10)
        
        self.debugBt = wx.Button(self, label='Debug Panel >> ', size=(120, 30))
        self.debugBt.Bind(wx.EVT_BUTTON, self.showDebug)
        ctSizer.Add(self.debugBt, flag=flagsR, border=2)
        return ctSizer

    def setPwrLed(self, name, colorStr):
        if name == 'Spwr':
            self.sensorPwBt.SetBackgroundColour(wx.Colour(colorStr))
        else:
            self.mainPwrBt.SetBackgroundColour(wx.Colour(colorStr))
        self.Refresh(False)

    def showDebug(self, evnt):
        if self.debugFrame == None: 
            posF = gv.iMainFrame.GetPosition()
            self.debugFrame = wx.MiniFrame(gv.iMainFrame, -1, 'Debug Panel', pos=(
                posF[0]+800, posF[1]), size=(240, 420), style=wx.DEFAULT_FRAME_STYLE)
            gv.iDetailPanel = PanelDebug(self.debugFrame)
            self.debugFrame.Bind(wx.EVT_CLOSE, self.infoWinClose)
            self.debugFrame.Show()

    def infoWinClose(self, event):
        """ Close the pop-up detail information window and clear paremeters."""
        if self.debugFrame:
            self.debugFrame.Destroy()
            self.debugFrame = gv.iDetailPanel = None


class PanelDebug(wx.Panel):
    """ Function control panel."""

    def __init__(self, parent):
        wx.Panel.__init__(self, parent)
        self.SetBackgroundColour(wx.Colour(200, 210, 200))
        self.dataList = ['0', '0', 'off', 'off', 'red', 'red', 'off', 'on']
        self.fieldlList = []
        self.SetSizer(self._buidUISizer())

#--UIFrame---------------------------------------------------------------------
    def _buidUISizer(self):
        """ Build the main UI Sizer. """
        flagsR = wx.RIGHT | wx.ALIGN_CENTER_VERTICAL
        mSizer = wx.BoxSizer(wx.HORIZONTAL)
        gs = wx.FlexGridSizer(13, 2, 5, 5)

        gs.Add(wx.StaticText(self, label=' Frequency : '), flag=flagsR, border=2)
        freText = wx.TextCtrl(self, -1, "0.0")
        self.fieldlList.append(freText)
        gs.Add(freText, flag=flagsR, border=2)

        gs.Add(wx.StaticText(self, label=' Voltage : '), flag=flagsR, border=2)
        volText = wx.TextCtrl(self, -1, "0.0")
        self.fieldlList.append(volText)
        gs.Add(volText, flag=flagsR, border=2)

        gs.Add(wx.StaticText(self, label=' Frequency LED : '), flag=flagsR, border=2)
        freLedCB= wx.ComboBox(self, -1, choices=['green', 'amber', 'red'])
        freLedCB.SetSelection(0)
        self.fieldlList.append(freLedCB)
        gs.Add(freLedCB, flag=flagsR, border=2)

        gs.Add(wx.StaticText(self, label=' Voltage LED : '), flag=flagsR, border=2)
        volLedCB= wx.ComboBox(self, -1, choices=['green', 'amber', 'red'])
        volLedCB.SetSelection(0)
        self.fieldlList.append(volLedCB)
        gs.Add(volLedCB, flag=flagsR, border=2)

        gs.Add(wx.StaticText(self, label=' Motor LED : '), flag=flagsR, border=2)
        motLedCB= wx.ComboBox(self, -1, choices=['green', 'amber', 'red'])
        motLedCB.SetSelection(0)
        self.fieldlList.append(motLedCB)
        gs.Add(motLedCB, flag=flagsR, border=2)

        gs.Add(wx.StaticText(self, label=' Pump LED : '), flag=flagsR, border=2)
        pumLedCB= wx.ComboBox(self, -1, choices=['green', 'amber', 'red'])
        pumLedCB.SetSelection(0)
        self.fieldlList.append(pumLedCB)
        gs.Add(pumLedCB, flag=flagsR, border=2)

        gs.Add(wx.StaticText(self, label=' Smoke : '), flag=flagsR, border=2)
        smokeCB= wx.ComboBox(self, -1, choices=['slow','fast', 'off'])
        smokeCB.SetSelection(0)
        self.fieldlList.append(smokeCB)
        gs.Add(smokeCB, flag=flagsR, border=2)

        gs.Add(wx.StaticText(self, label=' Siren : '), flag=flagsR, border=2)
        sirenCB= wx.ComboBox(self, -1, choices=['on', 'off'])
        sirenCB.SetSelection(0)
        self.fieldlList.append(sirenCB)
        gs.Add(sirenCB, flag=flagsR, border=2)


        gs.Add(wx.StaticText(self, label=' Pump speed : '), flag=flagsR, border=2)
        self.pumpSP= wx.ComboBox(self, -1, choices=['off', 'low', 'high'])
        self.pumpSP.SetSelection(0)
        gs.Add(self.pumpSP, flag=flagsR, border=2)


        gs.Add(wx.StaticText(self, label=' Moto speed : '), flag=flagsR, border=2)
        self.MotoSP= wx.ComboBox(self, -1, choices=['off', 'low', 'high'])
        self.MotoSP.SetSelection(0)
        gs.Add(self.MotoSP, flag=flagsR, border=2)


        gs.Add(wx.StaticText(self, label=' All sensor control : '), flag=flagsR, border=2)
        self.senPower= wx.ComboBox(self, -1, choices=['on', 'off'])
        self.senPower.SetSelection(0)
        gs.Add(self.senPower, flag=flagsR, border=2)


        gs.Add(wx.StaticText(self, label=' All power control : '), flag=flagsR, border=2)
        self.AllPower= wx.ComboBox(self, -1, choices=['on', 'off'])
        self.AllPower.SetSelection(0)
        gs.Add(self.AllPower, flag=flagsR, border=2)
        gs.AddSpacer(5)

        self.sendBt = wx.Button(self, label='Set')
        self.sendBt.Bind(wx.EVT_BUTTON, self.onSend)
        gs.Add(self.sendBt, flag=flagsR, border=2)
        
        mSizer.Add(gs, flag=flagsR, border=2)
        return mSizer


    def onSend(self, event):
        pass




