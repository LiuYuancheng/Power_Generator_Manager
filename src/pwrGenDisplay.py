#!/usr/bin/python
#-----------------------------------------------------------------------------
# Name:        pwGenDisplay.py
#
# Purpose:     This module is used to create the situation display frame show 
#              overlay on the CSI OT-Platform HMI program.
#
# Author:      Yuancheng Liu
#
# Created:     2020/07/22
# Copyright:   YC @ Singtel Cyber Security Research & Development Laboratory
# License:     YC
#-----------------------------------------------------------------------------

import wx
import time
import json
import pwrGenGobal as gv

#-----------------------------------------------------------------------------
#-----------------------------------------------------------------------------
class GenDisplayFrame(wx.Frame):
    """ Power gnera.
    """
    def __init__(self, parent, width, height, position=(100, 100)):
        wx.Frame.__init__(self, parent, title="GenDisplay", 
                          style=wx.MINIMIZE_BOX | wx.STAY_ON_TOP)
        self.SetBackgroundColour(wx.Colour('BLACK'))
        self.alphaValue = 155   # transparent control
        self.updateFlag = False
        # Build the main UI.
        self.SetTransparent(self.alphaValue)
        self.SetSizerAndFit(self.buidUISizer())
        self.SetPosition(position)
        self.Bind(wx.EVT_CLOSE, self.onCloseWindow)
        self.Show()

#-----------------------------------------------------------------------------
    def buidUISizer(self):
        """ Build the UI and the return the wx.sizer. """
        sizer = wx.BoxSizer(wx.VERTICAL)
        gv.iPerGImgPnl = PanelGen(self)
        sizer.Add(gv.iPerGImgPnl, flag= wx.CENTER, border=2)
        return sizer

#-----------------------------------------------------------------------------
    def updateData(self, dataDictStr):
        resultDict = json.loads(dataDictStr)
        gv.iPerGImgPnl.updateData(resultDict)
        self.updateFlag = True
        print("xxxxxxxxxxxxxxxxxxxxxxxxx")

#-----------------------------------------------------------------------------
    def updateDisplay(self):
        if self.updateFlag:
            gv.iPerGImgPnl.updateDisplay()
        self.updateFlag = False

#-----------------------------------------------------------------------------
    def onCloseWindow(self, evt):
        """ Stop the timeer and close the window."""
        gv.iPerGImgPnl = None
        self.Destroy()
        gv.iDisFrame = None

#-----------------------------------------------------------------------------
#-----------------------------------------------------------------------------
class PanelGen(wx.Panel):
    """ Panel to show the moto rotation rate.(Motor speed indicator)"""
    def __init__(self, parent, panelSize=(400, 240)):
        wx.Panel.__init__(self, parent, size=panelSize)
        self.SetBackgroundColour(wx.Colour(200, 200, 200))
        self.panelSize = panelSize
        self.bmp = wx.Bitmap(gv.PGIMG_PATH, wx.BITMAP_TYPE_ANY)
        self.smkBm = wx.Bitmap(gv.SMKIMG_PATH, wx.BITMAP_TYPE_ANY)
        self.sirBm = wx.Bitmap(gv.SIRIMG_PATH, wx.BITMAP_TYPE_ANY)
        self.Bind(wx.EVT_PAINT, self.onPaint)
        self.SetDoubleBuffered(True)
        self.toggle = True  # display toggle flash flag
        self.genDict = {'Freq': '50.00',    # frequence (dd.dd)
                        'Volt': '11.00',    # voltage (dd.dd)
                        # frequence led (green/amber/off)
                        'Fled': 'green',
                        'Vled': 'green',    # voltage led (green/amber/off)
                        'Mled': 'green',    # motor led (green/amber/off)
                        'Pled': 'green',    # pump led (green/amber/off)
                        # smoke indicator (fast/slow/off)
                        'Smok': 'slow',
                        'Pspd': 'off',      # pump speed (high/low/off)
                        'Mspd': 'off',      # moto speed (high/low/off)
                        'Sirn': 'on',      # siren (on/off)
                        }

#--PanelImge--------------------------------------------------------------------
    def onPaint(self, evt):
        """ Main draw function."""
        dc = wx.PaintDC(self)
        w, h = self.panelSize
        colorDict = {'green': 'Green', 'amber': 'Yellow', 'red': 'Red', 'low': 'Yellow',
                     'high': 'Green', 'on': 'Green', 'off': 'Black', 'slow': 'Yellow', 'fast': 'Red'}
        # display back ground.
        dc.DrawBitmap(self._scaleBitmap(self.bmp, w, h), 0, 0)
       # draw moto and pump speed text.
        dc.SetBrush(wx.Brush(wx.Colour('Gray')))
        dc.DrawRectangle(30, 205, 200, 25)
        dc.SetPen(wx.Pen('Black', width=1, style=wx.PENSTYLE_SOLID))
        dc.SetTextForeground(wx.Colour(colorDict[self.genDict['Pspd']]))
        dc.DrawText("Pump Speed: %s" %self.genDict['Pspd'], 32, 208)
        dc.SetTextForeground(wx.Colour(colorDict[self.genDict['Mspd']]))
        dc.DrawText("Moto Speed: %s" %self.genDict['Mspd'], 135, 208)

        # draw the pump LED
        dc.SetBrush(wx.Brush(colorDict[self.genDict['Pled']]))
        dc.DrawCircle(35, 50, 7)
        # draw the moto LED
        dc.SetBrush(wx.Brush(colorDict[self.genDict['Mled']]))
        dc.DrawCircle(250, 105, 7)

        if self.genDict['Smok'] != 'off':
            if self.toggle: dc.DrawBitmap(self._scaleBitmap(self.smkBm, 80, 100), 140, 20)
        
        if self.genDict['Sirn'] != 'off':
            if self.toggle: dc.DrawBitmap(self._scaleBitmap(self.sirBm, 60, 50), 310, 30)

        # Draw the frequence part.
        dc.SetTextForeground(wx.Colour('White'))
        dc.DrawText("Frequency", 260, 135)
        dc.SetPen(wx.Pen('BLACK'))
        for i in range(1, 10):
            dc.SetBrush(wx.Brush(colorDict[self.genDict['Fled']]))
            dc.DrawRectangle(265, i*6+150, 50, 8)
        dc.DrawText("%s HZ" %self.genDict['Freq'], 260, 215)
        
        # Draw the voltage part
        dc.DrawText("Voltage", 330, 135)
        dc.SetPen(wx.Pen('BLACK'))
        for i in range(1, 10):
            dc.SetBrush(wx.Brush(colorDict[self.genDict['Vled']]))
            dc.DrawRectangle(330, i*6+150, 50, 8)
        dc.DrawText("%s KV" %self.genDict['Volt'], 330, 215)
        
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

#--PanelImge--------------------------------------------------------------------
    def updateData(self, inputDict):
        for key in self.genDict.keys():
            self.genDict[key] = inputDict[key]

#--PanelMap--------------------------------------------------------------------
    def updateDisplay(self, updateFlag=None):
        """ Set/Update the display: if called as updateDisplay() the function will 
            update the panel, if called as updateDisplay(updateFlag=?) the function
            will set the self update flag.
        """
        self.toggle = not self.toggle
        self.Refresh(False)
        self.Update()

if __name__ == "__main__":
    app = wx.App()
    f = GenDisplayFrame(None, 410, 230)
    app.MainLoop()
