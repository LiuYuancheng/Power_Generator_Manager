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
    def updateDisplay(self):
        gv.iPerGImgPnl.updateDisplay()

#-----------------------------------------------------------------------------
    def onCloseWindow(self, evt):
        """ Stop the timeer and close the window."""
        gv.iPerGImgPnl = None
        self.Destroy()

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
        #dc.SetBrush(wx.Brush(wx.Colour('Black')))
        #dc.DrawRectangle(270, 1505, 50, 15)
        #dc.SetPen(wx.Pen(color, width=5, style=wx.PENSTYLE_SOLID))
        #dc.SetTextForeground(wx.Colour(color))
        #dc.DrawText(str(self.pumpSpd), 5, 5)
        # draw pump motion indicator.

        dc.SetPen(wx.Pen('Black', width=1, style=wx.PENSTYLE_SOLID))
        # draw the LED
        dc.SetBrush(wx.Brush('Yellow'))
        dc.DrawCircle(35, 50, 7)
        dc.DrawCircle(250, 105, 7)

        dc.DrawBitmap(self._scaleBitmap(self.smkBm, 80, 100), 140, 20)


        # Draw the frequence part.
        
        dc.SetTextForeground(wx.Colour('White'))
        dc.DrawText("Frequency", 260, 135)
        dc.SetPen(wx.Pen('BLACK'))
        for i in range(1, 10):
            brushColor = 'Green'
            dc.SetBrush(wx.Brush(brushColor))
            dc.DrawRectangle(265, i*6+150, 50, 8)
        dc.DrawText("50.00 HZ", 260, 215)
        
        # Draw the voltage part
        dc.DrawText("Voltage", 330, 135)
        dc.SetPen(wx.Pen('BLACK'))
        for i in range(1, 10):
            brushColor = 'Green'
            dc.SetBrush(wx.Brush(brushColor))
            dc.DrawRectangle(330, i*6+150, 50, 8)
        dc.DrawText("11.00 KV", 330, 215)




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


if __name__ == "__main__":
    app = wx.App()
    f = GenDisplayFrame(None, 410, 230)
    app.MainLoop()
