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

DEF_POS = (100, 100)    # default show up position on the screen

#-----------------------------------------------------------------------------
#-----------------------------------------------------------------------------
class GenDisplayFrame(wx.Frame):
    """ Power generator module display frame."""

    def __init__(self, parent, width, height, position=DEF_POS):
        wx.Frame.__init__(self, parent, title="GenDisplay",
                          style=wx.MINIMIZE_BOX | wx.STAY_ON_TOP)
        self.SetBackgroundColour(wx.Colour('BLACK'))
        self.alphaValue = 155   # transparent control
        self.updateFlag = False # display update flag.
        # Build the main UI.
        self.SetSizerAndFit(self.buidUISizer())
        self.SetTransparent(self.alphaValue)
        self.SetPosition(position)
        self.Bind(wx.EVT_CLOSE, self.onCloseWindow)
        self.Show()

#-----------------------------------------------------------------------------
    def buidUISizer(self):
        """ Build the UI and the return the wx.sizer. """
        sizer = wx.BoxSizer(wx.VERTICAL)
        gv.iPerGImgPnl = PanelGen(self)
        sizer.Add(gv.iPerGImgPnl, flag=wx.CENTER, border=2)
        return sizer

#-----------------------------------------------------------------------------
    def updateData(self, dataDictStr):
        """ Update the display panel data.
        Args:
            dataDictStr ([str]): [data dict json string]
        """
        resultDict = json.loads(dataDictStr)
        gv.iPerGImgPnl.updateData(resultDict)
        self.updateFlag = True # Set the update flag to true for update.

#-----------------------------------------------------------------------------
    def updateDisplay(self):
        """ Call the panel update function to update the display."""
        if self.updateFlag:
            gv.iPerGImgPnl.updateDisplay()
        self.updateFlag = False  # reset the update flag after display updated.

#-----------------------------------------------------------------------------
    def onCloseWindow(self, evt):
        """ Stop the timer and close the window."""
        gv.iPerGImgPnl = None
        self.Destroy()
        gv.iDisFrame = None

#-----------------------------------------------------------------------------
#-----------------------------------------------------------------------------
class PanelGen(wx.Panel):
    """ Panel to show the power generator components situation. """
    def __init__(self, parent, panelSize=(400, 240)):
        wx.Panel.__init__(self, parent, size=panelSize)
        self.SetBackgroundColour(wx.Colour(200, 200, 200))
        self.panelSize = panelSize
        self.bmp = wx.Bitmap(gv.PGIMG_PATH, wx.BITMAP_TYPE_ANY)     # back ground
        self.smkOnBm = wx.Bitmap(gv.SMKOIMG_PATH, wx.BITMAP_TYPE_ANY)  # smoke on indicator
        self.smkOffBm = wx.Bitmap(gv.SMKFIMG_PATH, wx.BITMAP_TYPE_ANY)  # smoke off indicator
        self.sirBm = wx.Bitmap(gv.SIRIMG_PATH, wx.BITMAP_TYPE_ANY)  # siren indicator
        self.toggle = True  # display toggle flash flag
        self.genDict = {'Freq': '50.00',    # frequence (dd.dd)
                        'Volt': '11.00',    # voltage (dd.dd)
                        'Fled': 'green',    # frequence led (green/amber/off)
                        'Vled': 'green',    # voltage led (green/amber/off)
                        'Mled': 'green',    # motor led (green/amber/off)
                        'Pled': 'green',    # pump led (green/amber/off)
                        'Smok': 'slow',     # smoke indicator (fast/slow/off)
                        'Pspd': 'off',      # pump speed (high/low/off)
                        'Mspd': 'off',      # moto speed (high/low/off)
                        'Sirn': 'on',       # siren (on/off)
                        }
        # Setup the paint display functino.
        self.Bind(wx.EVT_PAINT, self.onPaint)
        self.SetDoubleBuffered(True)

#--PanelGen--------------------------------------------------------------------
    def onPaint(self, evt):
        """ Main draw function by using wx.PaintDC."""
        dc = wx.PaintDC(self)
        colorDict = {'green': 'Green', 'amber': 'Yellow', 'red': 'Red',
                     'low': 'Yellow', 'high': 'Green', 'on': 'Green', 'off': 'Black',
                     'slow': 'Yellow', 'fast': 'Red'}
        # display back ground.
        w, h = self.panelSize
        dc.DrawBitmap(self._scaleBitmap(self.bmp, w, h), 0, 0)
       # draw moto and pump speed text.
        dc.SetBrush(wx.Brush(wx.Colour('Gray')))
        dc.DrawRectangle(15, 205, 225, 25)
        dc.SetPen(wx.Pen('Black', width=1, style=wx.PENSTYLE_SOLID))
        dc.SetTextForeground(wx.Colour(colorDict[self.genDict['Pspd']]))
        dc.DrawText("Pump Speed: %s" % self.genDict['Pspd'], 20, 208)
        dc.SetTextForeground(wx.Colour(colorDict[self.genDict['Mspd']]))
        dc.DrawText("Moto Speed: %s" % self.genDict['Mspd'], 140, 208)
        # draw the pump LED
        dc.SetBrush(wx.Brush(colorDict[self.genDict['Pled']]))
        dc.DrawCircle(35, 50, 7)
        # draw the moto LED
        dc.SetBrush(wx.Brush(colorDict[self.genDict['Mled']]))
        dc.DrawCircle(250, 105, 7)
        # draw the smoke indicator.
        if self.genDict['Smok'] != 'off':
            bm = self.smkOnBm if self.toggle else self.smkOffBm
            dc.DrawBitmap(self._scaleBitmap(bm, 80, 100), 140, 20)
        # draw the siren indiactor.
        if self.genDict['Sirn'] != 'off' and self.toggle:
            dc.DrawBitmap(self._scaleBitmap(self.sirBm, 60, 50), 310, 30)

        dc.SetTextForeground(wx.Colour('White'))
        # Draw the voltage part
        dc.DrawText("Voltage", 260, 135)
        dc.SetPen(wx.Pen('BLACK'))
        for i in range(1, 10):
            dc.SetBrush(wx.Brush(colorDict[self.genDict['Vled']]))
            dc.DrawRectangle(265, i*6+150, 50, 8)
        dc.DrawText("%s KV" % self.genDict['Volt'], 265, 215)

        # Draw the frequence part.
        dc.DrawText("Frequency", 330, 135)
        dc.SetPen(wx.Pen('BLACK'))
        for i in range(1, 10):
            dc.SetBrush(wx.Brush(colorDict[self.genDict['Fled']]))
            dc.DrawRectangle(330, i*6+150, 50, 8)
        dc.DrawText("%s HZ" % self.genDict['Freq'], 335, 215)

        
#--PanelGen--------------------------------------------------------------------
    def _scaleBitmap(self, bitmap, width, height):
        """ Resize a input bitmap.(bitmap-> image -> resize image -> bitmap)"""
        #image = wx.ImageFromBitmap(bitmap) # used below 2.7
        image = bitmap.ConvertToImage()
        image = image.Scale(width, height, wx.IMAGE_QUALITY_HIGH)
        #result = wx.BitmapFromImage(image) # used below 2.7
        result = wx.Bitmap(image, depth=wx.BITMAP_SCREEN_DEPTH)
        return result

#--PanelGen--------------------------------------------------------------------
    def _scaleBitmap2(self, bitmap, width, height):
        """ Resize a input bitmap.(bitmap-> image -> resize image -> bitmap)"""
        image = wx.ImageFromBitmap(bitmap) # used below 2.7
        image = image.Scale(width, height, wx.IMAGE_QUALITY_HIGH)
        result = wx.BitmapFromImage(image) # used below 2.7
        return result

#--PanelGen--------------------------------------------------------------------
    def updateBitmap(self, bitMap):
        """ Update the panel bitmap image."""
        if not bitMap: return
        self.bmp = bitMap

#--PanelGen--------------------------------------------------------------------
    def updateData(self, inputDict):
        """ Called by parent object to update the display panel data.
        Args:
            dataDictStr ([str]): [data dict json string]
        """
        for key in self.genDict.keys():
            self.genDict[key] = inputDict[key]

#--PanelGen--------------------------------------------------------------------
    def updateDisplay(self, updateFlag=None):
        """ Set/Update the display: if called as updateDisplay() the function will 
            update the panel, if called as updateDisplay(updateFlag=?) the function
            will set the self update flag.
        """
        self.toggle = not self.toggle # change the toggle flag every time we updated display
        self.Refresh(False)
        self.Update()


#-----------------------------------------------------------------------------
#-----------------------------------------------------------------------------
if __name__ == "__main__":
    app = wx.App()
    f = GenDisplayFrame(None, 410, 230)
    app.MainLoop()
