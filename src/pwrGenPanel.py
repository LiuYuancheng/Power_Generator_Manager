#!/usr/bin/python
#-----------------------------------------------------------------------------
# Name:        pwrGenPanel.py
#
# Purpose:     This module is used to create different function panels used for 
#              <pwrGenRun> program UI parts.
# Author:      Yuancheng Liu
#
# Created:     2020/01/10
# Copyright:   YC @ Singtel Cyber Security Research & Development Laboratory
# License:     YC
#-----------------------------------------------------------------------------
import wx
from math import sin, cos, radians, pi

import pwrGenGobal as gv
import pwrGenDisplay as gd
import pwrSubDisplay as sd

#-----------------------------------------------------------------------------
#-----------------------------------------------------------------------------
class PanelMoto(wx.Panel):
    """ Panel to show the moto rotation rate.(Motor speed indicator)"""
    def __init__(self, parent, panelSize=(120, 120)):
        wx.Panel.__init__(self, parent, size=panelSize)
        self.SetBackgroundColour(wx.Colour(200, 200, 200))
        self.panelSize = panelSize
        self.bmp = wx.Bitmap(gv.MOIMG_PATH, wx.BITMAP_TYPE_ANY)  # background
        self.Bind(wx.EVT_PAINT, self.onPaint)
        self.SetDoubleBuffered(True)
        self.angle = 0  # rotate indicator angle(degree)
        self.motoSpd = 'off'  # speed text.

#--PanelImge--------------------------------------------------------------------
    def onPaint(self, evt):
        """ Main draw function."""
        dc = wx.PaintDC(self)
        w, h = self.panelSize
        # draw background.
        dc.DrawBitmap(self._scaleBitmap(self.bmp, w, h), 0, 0)
        color = 'Gray'
        if self.motoSpd == 'low':
            color = 'Green'
        elif self.motoSpd == 'high':
            color = 'Yellow'
        # draw motor speed text.
        dc.SetBrush(wx.Brush(wx.Colour('Black')))
        dc.DrawRectangle(1, 5, 30, 15)
        dc.SetPen(wx.Pen(color, width=5, style=wx.PENSTYLE_SOLID))
        dc.SetTextForeground(wx.Colour(color))
        dc.DrawText(str(self.motoSpd), 5, 5)
        # draw speed motion indicator.
        dc.DrawLine(w//2, h//2, int(w//2+60*sin(radians(self.angle))),
                    int(h//2-60*cos(radians(self.angle))))

#-----------------------------------------------------------------------------
    def setMotoSpeed(self, speed):
        if speed in ('off', 'low', 'high'):
            self.motoSpd = speed
            self.updateDisplay(updateFlag=True)
        else:
            print('PanelMoto : input speed value is invalid %s' % str(speed))

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
        if self.motoSpd == 'off' and (not updateFlag):
            self.angle = 0
            return
        ang = 20 if self.motoSpd == 'low' else 40
        self.angle = (self.angle + ang) % 360
        self.Refresh(False)
        self.Update()

#-----------------------------------------------------------------------------
#-----------------------------------------------------------------------------
class PanelPump(wx.Panel):
    """ Panel to show the pump running speed.(pump speed indicator)"""
    def __init__(self, parent, panelSize=(120, 120)):
        wx.Panel.__init__(self, parent, size=panelSize)
        self.SetBackgroundColour(wx.Colour(200, 200, 200))
        self.panelSize = panelSize
        self.bmp = wx.Bitmap(gv.PUIMG_PATH, wx.BITMAP_TYPE_ANY)
        self.Bind(wx.EVT_PAINT, self.onPaint)
        self.SetDoubleBuffered(True)
        self.maxVal = 80    # max pump line hight
        self.pos = 80       # pump line position (from top to buttom)
        self.pumpSpd = 'off'

#--PanelImge--------------------------------------------------------------------
    def onPaint(self, evt):
        """ Main draw function."""
        dc = wx.PaintDC(self)
        w, h = self.panelSize
        # pump back ground.
        dc.DrawBitmap(self._scaleBitmap(self.bmp, w, h), 0, 0)
        color = 'Gray'
        if self.pumpSpd == 'low':
            color = 'Green'
        elif self.pumpSpd == 'high':
            color = 'Yellow'
       # draw pump speed text.
        dc.SetBrush(wx.Brush(wx.Colour('Black')))
        dc.DrawRectangle(1, 5, 30, 15)
        dc.SetPen(wx.Pen(color, width=5, style=wx.PENSTYLE_SOLID))
        dc.SetTextForeground(wx.Colour(color))
        dc.DrawText(str(self.pumpSpd), 5, 5)
        # draw pump motion indicator.
        dc.SetPen(wx.Pen('BLACK'))
        for i in range(1, 21):
            brushColor = '#075100' if i < self.pos/5 else color
            dc.SetBrush(wx.Brush(brushColor))
            dc.DrawRectangle(88, i*3+27, 25, 4)

#-----------------------------------------------------------------------------
    def setPumpSpeed(self, speed):
        if speed in ('off', 'low', 'high'):
            self.pumpSpd = speed
            self.updateDisplay(updateFlag=True)
        else:
            print('PanelMoto : input speed value is invalid %s' % str(speed))
        
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
        if self.pumpSpd == 'off' and (not updateFlag):
            self.maxVal = self.pos = 80
            return
        self.maxVal = 40 if self.pumpSpd == 'low' else 80
        addVal = 10 if self.pumpSpd == 'low' else 20
        if self.pos < 100 - self.maxVal:
            self.pos = 100
        else:
            self.pos -= addVal
        self.Refresh(False)
        self.Update()

#-----------------------------------------------------------------------------
#-----------------------------------------------------------------------------
class PanelLoad(wx.Panel):
    """ Panel to show the system power load situation."""
    def __init__(self, parent):
        wx.Panel.__init__(self, parent)
        self.SetBackgroundColour(wx.Colour(200, 210, 200))
        self.loadBtDict = {'Indu': None,      # Industry area
                           'Airp': None,      # Air port
                           'Resi': None,      # Residential area
                           'Stat': None,      # Stataion power
                           'TrkA': None,      # Track A power
                           'TrkB': None,      # Track B power
                           'City': None,      # City power
                           } # wx.Button indicator dict.
        self.SetSizer(self._buidUISizer())

#-----------------------------------------------------------------------------
    def _buidUISizer(self):
        """ build the control panel sizer. """
        flagsR = wx.RIGHT
        sizerAll = wx.BoxSizer(wx.VERTICAL)
        sizerAll.Add(wx.StaticText(
            self, -1, 'System Load Indicators:'), flag=flagsR, border=2)
        sizerAll.AddSpacer(10)

        #sizer = wx.GridSizer(8, 2, 4, 4)
        sizer = wx.FlexGridSizer(7, 2, 4, 4) # use flexable sizer.
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
            self.loadBtDict[btKeyList[i]] = wx.Button(
                self, label='OFF', size=(60, 21))
            self.loadBtDict[btKeyList[i]].SetBackgroundColour(
                wx.Colour('GRAY'))
            sizer.Add(self.loadBtDict[btKeyList[i]])
        sizerAll.Add(sizer, flag=flagsR, border=2)
        return sizerAll

#-----------------------------------------------------------------------------
    def setLoadIndicator(self, loadDict):
        """ Set the load indicators."""
        for keyStr in loadDict.keys():
            if keyStr in self.loadBtDict.keys():
                (btLb, btColor) = (
                    'ON ', 'GREEN') if loadDict[keyStr] else ('OFF', 'GRAY')
                self.loadBtDict[keyStr].SetLabel(btLb)
                self.loadBtDict[keyStr].SetBackgroundColour(wx.Colour(btColor))
        self.Refresh(False)

#-----------------------------------------------------------------------------
#-----------------------------------------------------------------------------
class PanelCtrl(wx.Panel):
    """ System function display and control panel. Show the all sensor power 
        and the system power provide manully control pop-up window.
    """
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
        ctSizer.AddSpacer(3)
        self.sensorPwBt = wx.Button(self, label='All Sensors Pwr  ', size=(120, 30))
        self.sensorPwBt.SetBackgroundColour(wx.Colour('Gray'))
        ctSizer.Add(self.sensorPwBt, flag=flagsR, border=2)
        ctSizer.AddSpacer(3)

        self.mainPwrBt = wx.Button(self, label='System Main Pwr ', size=(120, 30))
        self.mainPwrBt.SetBackgroundColour(wx.Colour('Gray'))
        ctSizer.Add(self.mainPwrBt, flag=flagsR, border=2)
        ctSizer.AddSpacer(10)
        
        #self.debugBt = wx.Button(self, label='Debug Panel >', size=(120, 30))
        #self.debugBt.Bind(wx.EVT_BUTTON, self.showDebug)
        self.debugBt = wx.CheckBox(self, label = 'Debug Panel')
        self.debugBt.Bind(wx.EVT_CHECKBOX, self.showDebug)
        ctSizer.Add(self.debugBt, flag=flagsR, border=2)
        ctSizer.AddSpacer(3)

        #self.displayBt = wx.Button(self, label='Gen Panel >', size=(120, 30))
        #self.displayBt.Bind(wx.EVT_BUTTON, self.showDisplay)
        self.genBt = wx.CheckBox(self, label = 'Generator Panel')
        self.genBt.Bind(wx.EVT_CHECKBOX, self.showGenDisplay)
        ctSizer.Add(self.genBt, flag=flagsR, border=2)        
        ctSizer.AddSpacer(3)

        self.subBt = wx.CheckBox(self, label = 'Substation Panel')
        self.subBt.Bind(wx.EVT_CHECKBOX, self.showSubDisplay)
        ctSizer.Add(self.subBt, flag=flagsR, border=2)

        return ctSizer

#--PanelCtrl-------------------------------------------------------------------
    def setPwrLED(self, name, colorStr):
        if name == 'Spwr':
            self.sensorPwBt.SetBackgroundColour(wx.Colour(colorStr))
        else:
            self.mainPwrBt.SetBackgroundColour(wx.Colour(colorStr))
        self.Refresh(False)

#--PanelCtrl------------------------------------------------------------------
    def showDebug(self, evnt):
        """ pop-up the debug window."""
        if self.debugFrame == None and self.debugBt.IsChecked():
            posF = gv.iMainFrame.GetPosition()
            self.debugFrame = wx.MiniFrame(gv.iMainFrame, -1, 'Debug Panel', pos=(
                posF[0]+800, posF[1]), size=(250, 800), style=wx.DEFAULT_FRAME_STYLE)
            gv.iDetailPanel = PanelDebug(self.debugFrame)
            self.debugFrame.Bind(wx.EVT_CLOSE, self.infoWinClose)
            self.debugFrame.Show()
        elif self.debugFrame:
            # close the debug window if the user unchecked the checkbox.
            self.debugFrame.Destroy()
            self.debugFrame = gv.iDetailPanel = None
        print("Triggered the check box event.\n")

#--PanelCtrl------------------------------------------------------------------
    def showGenDisplay(self, event):
        if gv.iDisFrame == None and self.genBt.IsChecked():
            gv.iDisFrame = gd.GenDisplayFrame(self, 410, 230, position=gv.gDisPnlPos)
        else:
            gv.iDisFrame.onCloseWindow(None)
            gv.iPerGImgPnl = None
            gv.iDisFrame = None

#--PanelCtrl------------------------------------------------------------------
    def showSubDisplay(self, event):
        if gv.iSubFrame == None and self.subBt.IsChecked():
            gv.iSubFrame = sd.SubDisplayFrame(self, 410, 230, position=gv.gSubPnlPos)
        else:
            gv.iSubFrame.onCloseWindow(None)
            gv.iPerSImgPnl = None
            gv.iSubFrame = None
            
#--PanelCtrl------------------------------------------------------------------
    def infoWinClose(self, event):
        """ Close the pop-up detail information window and clear paremeters."""
        if self.debugFrame:
            self.debugFrame.Destroy()
            self.debugFrame = gv.iDetailPanel = None
            if self.debugBt.IsChecked(): self.debugBt.SetValue(False)

#-----------------------------------------------------------------------------
#-----------------------------------------------------------------------------
class PanelDebug(wx.Panel):
    """ Manul system control panel used for debugging."""
    def __init__(self, parent):
        wx.Panel.__init__(self, parent)
        self.SetBackgroundColour(wx.Colour(200, 210, 200))
        self.genFieldlList = {}     # ardurino setting field list. 
        self.plcFieldList = {}      # plc setting field list.
        self.SetSizer(self._buidUISizer())

#-----------------------------------------------------------------------------
    def _buidUISizer(self):
        """ Build the main UI Sizer. """
        elemSize, flagsR = (80, 25), wx.RIGHT
        mSizer = wx.BoxSizer(wx.HORIZONTAL)
        gs = wx.FlexGridSizer(23, 2, 5, 5)
        # Generator setup:
        # row:0
        gs.Add(wx.StaticText(self, label=' [ Generator Setup ] '), flag=flagsR, border=2)
        gs.AddSpacer(5)
        # row:1
        gs.Add(wx.StaticText(self, label=' Frequency : '), flag=flagsR, border=2)
        self.genFieldlList['Freq'] = wx.TextCtrl(self, -1, "50.00", size=elemSize)
        gs.Add(self.genFieldlList['Freq'], flag=flagsR, border=2)
        # row:2
        gs.Add(wx.StaticText(self, label=' Voltage : '), flag=flagsR, border=2)
        self.genFieldlList['Volt'] = wx.TextCtrl(self, -1, "11.00", size=elemSize)
        gs.Add(self.genFieldlList['Volt'], flag=flagsR, border=2)
        # row:3
        gs.Add(wx.StaticText(self, label=' Frequency LED : '),
               flag=flagsR, border=2)
        self.genFieldlList['Fled'] = wx.ComboBox(
            self, -1, choices=['green', 'amber', 'red'], size=elemSize)
        self.genFieldlList['Fled'].SetSelection(0)
        gs.Add(self.genFieldlList['Fled'], flag=flagsR, border=2)
        # row:4
        gs.Add(wx.StaticText(self, label=' Voltage LED : '),
               flag=flagsR, border=2)
        self.genFieldlList['Vled'] = wx.ComboBox(
            self, -1, choices=['green', 'amber', 'red'], size=elemSize)
        self.genFieldlList['Vled'].SetSelection(0)
        gs.Add(self.genFieldlList['Vled'], flag=flagsR, border=2)
        # row:5
        gs.Add(wx.StaticText(self, label=' Motor LED : '), flag=flagsR, border=2)
        self.genFieldlList['Mled'] = wx.ComboBox(
            self, -1, choices=['green', 'amber', 'red'], size=elemSize)
        self.genFieldlList['Mled'].SetSelection(0)
        gs.Add(self.genFieldlList['Mled'], flag=flagsR, border=2)
        # row:6
        gs.Add(wx.StaticText(self, label=' Pump LED : '), flag=flagsR, border=2)
        self.genFieldlList['Pled'] = wx.ComboBox(
            self, -1, choices=['green', 'amber', 'red'], size=elemSize)
        self.genFieldlList['Pled'].SetSelection(0)
        gs.Add(self.genFieldlList['Pled'], flag=flagsR, border=2)
        # row:7
        gs.Add(wx.StaticText(self, label=' Smoke : '), flag=flagsR, border=2)
        self.genFieldlList['Smok'] = wx.ComboBox(
            self, -1, choices=['slow', 'fast', 'off'], size=elemSize)
        self.genFieldlList['Smok'].SetSelection(0)
        gs.Add(self.genFieldlList['Smok'], flag=flagsR, border=2)
        # row:8
        gs.Add(wx.StaticText(self, label=' Siren : '), flag=flagsR, border=2)
        self.genFieldlList['Sirn'] = wx.ComboBox(
            self, -1, choices=['on', 'off'], size=elemSize)
        self.genFieldlList['Sirn'].SetSelection(1)
        gs.Add(self.genFieldlList['Sirn'], flag=flagsR, border=2)
        # row:9
        gs.Add(wx.StaticText(self, label=' Pump speed : '), flag=flagsR, border=2)
        self.plcFieldList['Pspd'] = wx.ComboBox(
            self, -1, choices=['off', 'low', 'high'], size=elemSize)
        self.plcFieldList['Pspd'].SetSelection(0)
        gs.Add(self.plcFieldList['Pspd'], flag=flagsR, border=2)
        # row:10
        gs.Add(wx.StaticText(self, label=' Moto speed : '), flag=flagsR, border=2)
        self.plcFieldList['Mspd'] = wx.ComboBox(
            self, -1, choices=['off', 'low', 'high'], size=elemSize)
        self.plcFieldList['Mspd'].SetSelection(0)
        gs.Add(self.plcFieldList['Mspd'], flag=flagsR, border=2)
        # row:11
        gs.Add(wx.StaticText(self, label=' All sensor control : '),
               flag=flagsR, border=2)
        self.plcFieldList['Spwr'] = wx.ComboBox(
            self, -1, choices=['on', 'off'], size=elemSize)
        self.plcFieldList['Spwr'].SetSelection(0)
        gs.Add(self.plcFieldList['Spwr'], flag=flagsR, border=2)
        # row:12
        gs.Add(wx.StaticText(self, label=' All power control : '),
               flag=flagsR, border=2)
        self.plcFieldList['Mpwr'] = wx.ComboBox(
            self, -1, choices=['on', 'off'], size=elemSize)
        self.plcFieldList['Mpwr'].SetSelection(0)
        gs.Add(self.plcFieldList['Mpwr'], flag=flagsR, border=2)
        # row:13
        self.rstBt = wx.Button(self, label='Reset', size=elemSize)
        self.rstBt.Bind(wx.EVT_BUTTON, self.onReset)
        gs.Add(self.rstBt, flag=flagsR, border=2)
        self.sendBt = wx.Button(self, label='Set', size=elemSize)
        self.sendBt.Bind(wx.EVT_BUTTON, self.onSend)
        gs.Add(self.sendBt, flag=flagsR, border=2)
        # Display frame setup.
        # row:14
        gs.Add(wx.StaticText(self, label=' [ DisplayPanel Setup ] '), flag=flagsR, border=2)
        gs.AddSpacer(5)
        # row:15
        gs.Add(wx.StaticText(self, label=' GeneratorPnl Pos X : '), flag=flagsR, border=2)
        self.disPnlX = wx.TextCtrl(self, -1,str(gv.gDisPnlPos[0]), size=elemSize)
        gs.Add(self.disPnlX, flag=flagsR, border=2)
        # row:16
        gs.Add(wx.StaticText(self, label=' GeneratorPnl Pos Y : '), flag=flagsR, border=2)
        self.disPnlY = wx.TextCtrl(self, -1,str(gv.gDisPnlPos[1]), size=elemSize)
        gs.Add(self.disPnlY, flag=flagsR, border=2)
        # row:17
        gs.Add(wx.StaticText(self, label=' SubstationPnl Pos X : '), flag=flagsR, border=2)
        self.subPnlX = wx.TextCtrl(self, -1,str(gv.gSubPnlPos[0]), size=elemSize)
        gs.Add(self.subPnlX, flag=flagsR, border=2)
        # row 18
        gs.Add(wx.StaticText(self, label=' SubstationPnl Pos Y : '), flag=flagsR, border=2)
        self.subPnlY = wx.TextCtrl(self, -1,str(gv.gSubPnlPos[1]), size=elemSize)
        gs.Add(self.subPnlY, flag=flagsR, border=2)                
        # row:19
        gs.AddSpacer(5)
        self.disSetBt = wx.Button(self, label='Set', size=elemSize)
        self.disSetBt.Bind(wx.EVT_BUTTON, self.onSetDis)
        gs.Add(self.disSetBt, flag=flagsR, border=2)
        
        # Functino Ctrl Setup
        # row:20
        gs.Add(wx.StaticText(self, label=' [ Functino Ctrl Setup ] '), flag=flagsR, border=2)
        gs.AddSpacer(5)
        # row 21
        gs.Add(wx.StaticText(self, label=' Control Mode : '), flag=flagsR, border=2)
        self.ctrlMode = wx.ComboBox(self, -1, choices=['Manul', 'Auto'], size=elemSize)
        self.ctrlMode.Bind(wx.EVT_COMBOBOX, self.onModeChange)
        gs.Add(self.ctrlMode, flag=flagsR, border=2)
        # row 22
        gs.Add(wx.StaticText(self, label=' Atk Detection : '), flag=flagsR, border=2)
        self.detCtrl = wx.ComboBox(self, -1, choices=['on', 'off'], size=elemSize)
        self.detCtrl.Bind(wx.EVT_COMBOBOX, self.onDetectChange)
        gs.Add(self.detCtrl, flag=flagsR, border=2)

        mSizer.Add(gs, flag=flagsR, border=2)
        return mSizer

#-----------------------------------------------------------------------------
    def onReset(self, event):
        """ Reset the panel components to default value."""
        self.genFieldlList['Freq'].SetValue('50.00')
        self.genFieldlList['Volt'].SetValue('11.00')
        self.genFieldlList['Fled'].SetSelection(0)
        self.genFieldlList['Vled'].SetSelection(0)
        self.genFieldlList['Mled'].SetSelection(0)
        self.genFieldlList['Pled'].SetSelection(0)
        self.genFieldlList['Smok'].SetSelection(0)
        self.genFieldlList['Sirn'].SetSelection(1)
        self.plcFieldList['Pspd'].SetSelection(0)
        self.plcFieldList['Mspd'].SetSelection(0)
        self.plcFieldList['Spwr'].SetSelection(0)
        self.plcFieldList['Mpwr'].SetSelection(0)

#-----------------------------------------------------------------------------
    def onModeChange(self, event):
        """ Change the generator control mode.
        """
        genDict = {'Mode':self.ctrlMode.GetSelection()}
        print("Send the mode setting: %s" %str(genDict))
        gv.iMainFrame.connectReq('SetALC', parm=genDict)

#-----------------------------------------------------------------------------
    def onSend(self, event):
        """ Send the setting to the Raspberry PI"""
        print('Send Gen setting debug message')
        genDict = {key:self.genFieldlList[key].GetValue() for key in self.genFieldlList.keys()}
        gv.iMainFrame.connectReq('SetGen', parm=genDict)

        print('Send PLC setting deubg message')
        plcDict = {key:self.plcFieldList[key].GetValue() for key in self.plcFieldList.keys()}
        gv.iMainFrame.connectReq('SetPLC', parm=plcDict)

#-----------------------------------------------------------------------------
    def onSetDis(self ,event):
        """[Set the display panel pop-up position]
        Args:
            event ([wx.EVT_BUTTON]): [description]
        """
        posGX = int(self.disPnlX.GetValue())
        posGY = int(self.disPnlY.GetValue())
        gv.gDisPnlPos = (posGX, posGY)

        posSX = int(self.subPnlX.GetValue())
        posSY = int(self.subPnlY.GetValue())
        gv.gDisPnlPos = (posSX, posSY) 

#-----------------------------------------------------------------------------
    def onDetectChange(self, event):
        """[Set the auto detection on/off]
        Args:
            event ([type]): [description]
        """
        gv.gAutoDet = True if self.detCtrl.GetSelection() == 0 else False
        print("Func(onDetectChange): Auto detection %s" %str(gv.gAutoDet))
        #if gv.iSubFrame:
        #    gv.iSubFrame.onAlertCatch()


#-----------------------------------------------------------------------------
#-----------------------------------------------------------------------------
def main():
    """ Main function used for local test debug panel. """
    app = wx.App()
    mainFrame = wx.Frame(gv.iMainFrame, -1, 'Debug Panel', pos=(300, 300), size=(250, 800), style=wx.DEFAULT_FRAME_STYLE)
    gv.iDetailPanel = PanelDebug(mainFrame)
    mainFrame.Show()
    app.MainLoop()

if __name__ == "__main__":
    main()
