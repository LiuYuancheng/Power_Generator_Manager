#!/usr/bin/python
#-----------------------------------------------------------------------------
# Name:        pwGenDisplay.py
#
# Purpose:     This module is used to create a transparent, no window board live 
#              situation display frame show overlay on top of the CSI OT-Platform 
#              HMI program.
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

DEF_POS = (300, 300)    # default show up position on screen used for local test.
#-----------------------------------------------------------------------------
#-----------------------------------------------------------------------------
class GenDisplayFrame(wx.Frame):
    """ Power generator module live situation display frame."""

    def __init__(self, parent, width, height, position=DEF_POS):
        wx.Frame.__init__(self, parent, title="GenLiveDisplay",
                          style=wx.MINIMIZE_BOX | wx.STAY_ON_TOP)
        self.SetBackgroundColour(wx.Colour('BLACK'))
        self.updateFlag = False  # flag to identify whether the panel need update.
        # Build the main UI.
        self.SetSizerAndFit(self.buidUISizer())
        self.SetTransparent(gv.gTranspPct*255//100)
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
        self.updateFlag = True  # Set the update flag to true for update.

#-----------------------------------------------------------------------------
    def updateDisplay(self):
        """ Call the panel update function to update the display."""
        if self.updateFlag:
            gv.iPerGImgPnl.updateDisplay()
            self.updateFlag = False  # reset the update flag after display updated.

#-----------------------------------------------------------------------------
    def onCloseWindow(self, evt):
        """ Close the window and reset the gv parameters."""
        gv.iPerGImgPnl = None
        self.Destroy()
        #gv.iDisFrame = None

#-----------------------------------------------------------------------------
#-----------------------------------------------------------------------------
class PanelGen(wx.Panel):
    """ Panel to draw the power generator components live situation. """
    def __init__(self, parent, panelSize=(400, 240)):
        wx.Panel.__init__(self, parent, size=panelSize)
        self.SetBackgroundColour(wx.Colour(200, 200, 200))
        self.panelSize = panelSize
        self.toggle = True  # display indicator/led toggle flash flag
        #Used bitmaps:
        self.bgBm = wx.Bitmap(gv.PGIMG_PATH, wx.BITMAP_TYPE_ANY)         # back ground img
        self.smkOnBm = wx.Bitmap(gv.SMKOIMG_PATH, wx.BITMAP_TYPE_ANY)   # smoke on indicator img
        self.smkOffBm = wx.Bitmap(gv.SMKFIMG_PATH, wx.BITMAP_TYPE_ANY)  # smoke off indicator img
        self.sirBm = wx.Bitmap(gv.SIRIMG_PATH, wx.BITMAP_TYPE_ANY)      # siren indicator img
        # default display data dict: 
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
        # Setup the paint display function.
        self.Bind(wx.EVT_PAINT, self.onPaint)
        self.SetDoubleBuffered(True)

#--PanelGen--------------------------------------------------------------------
    def onPaint(self, evt):
        """ Main draw function by using wx.PaintDC."""
        dc = wx.PaintDC(self)
        colorDict = {'green': 'Green', 'amber': 'Yellow', 'red': 'Red',
                     'low': 'Yellow', 'high': 'Green', 'on': 'Green', 
                     'off': 'Black', 'slow': 'Yellow', 'fast': 'Red'} # color code.
        # display back ground.
        w, h = self.panelSize
        dc.DrawBitmap(self._scaleBitmap(self.bgBm, w, h), 0, 0)
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
        
        # Draw the voltage display part.
        dc.DrawText("Voltage", 260, 135)
        dc.SetPen(wx.Pen('BLACK'))
        for i in range(1, 10):
            dc.SetBrush(wx.Brush(colorDict[self.genDict['Vled']]))
            dc.DrawRectangle(265, i*6+150, 50, 8)
        dc.DrawText("%s KV" % self.genDict['Volt'], 265, 215)

        # Draw the frequence display part.
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
        self.bgBm = bitMap

#--PanelGen--------------------------------------------------------------------
    def updateData(self, inputDict):
        """ Called by parent object to update the display panel data dict<genDict>.
        Args:
            dataDictStr ([Dict]): [data dict]
        """
        for key in self.genDict.keys():
            try:
                self.genDict[key] = inputDict[key]
            except Exception as e:
                print("Data set key missing exception: %s" %str(e))

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
def main():
    """ Main function used for local test. """
    app = wx.App()
    mainFrame = GenDisplayFrame(None, 410, 230)
    app.MainLoop()

if __name__ == "__main__":
    main()

