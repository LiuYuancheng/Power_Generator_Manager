#!/usr/bin/python
#-----------------------------------------------------------------------------
# Name:        pwSubDisplay.py
#
# Purpose:     This module is used to create a transparent, no window board live 
#              substation control parameter simulation display frame show overlay 
#              on top of the CSI OT-Platform HMI program.
#
# Author:      Yuancheng Liu
#
# Created:     2020/10/2
# Copyright:   Singtel Cyber Security Research & Development Laboratory
# License:     N.A
#-----------------------------------------------------------------------------

import wx
import time
import pwrGenGobal as gv

DEF_POS = (300, 300)    # default show up position on screen used for local test.

#-----------------------------------------------------------------------------
#-----------------------------------------------------------------------------
class SubDisplayFrame(wx.Frame):
    """ Power generator module live situation display frame."""

    def __init__(self, parent, width, height, position=DEF_POS):
        wx.Frame.__init__(self, parent, title="SubLiveDisplay",
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
        gv.iPerSImgPnl = PanelSub(self)
        sizer.Add(gv.iPerSImgPnl, flag=wx.CENTER, border=2)
        return sizer

    #-----------------------------------------------------------------------------
    def onCloseWindow(self, evt):
        """ Close the window and reset the gv parameters."""
        #gv.iPerSImgPnl = None
        self.Destroy()

#-----------------------------------------------------------------------------
#-----------------------------------------------------------------------------
class PanelSub(wx.Panel):
    """ Panel to draw the power generator components live situation. """
    def __init__(self, parent, panelSize=(400, 240)):
        wx.Panel.__init__(self, parent, size=panelSize)
        #self.SetBackgroundColour(wx.Colour(200, 200, 200))
        self.SetBackgroundColour(wx.Colour('BLACK'))
        self.panelSize = panelSize
        # Setup the paint display function.
        self.Bind(wx.EVT_PAINT, self.onPaint)
        self.SetDoubleBuffered(True)

    def onPaint(self, evt):
        dc = wx.PaintDC(self)
        print("In paint function.")
        dc.SetPen(wx.Pen('White', width=1, style=wx.PENSTYLE_SOLID))
        dc.SetTextForeground(wx.Colour('White'))
        dc.DrawText("[Under Development] Place Holder Panel for Substation Simulator.", 10, 100)

    def updateDisplay(self, updateFlag=None):
        """ Set/Update the display: if called as updateDisplay() the function will 
            update the panel, if called as updateDisplay(updateFlag=?) the function
            will set the self update flag.
        """
        #self.toggle = not self.toggle # change the toggle flag every time we updated display
        self.Refresh(False)
        self.Update()

#-----------------------------------------------------------------------------
#-----------------------------------------------------------------------------
def main():
    """ Main function used for local test. """
    app = wx.App()
    mainFrame = SubDisplayFrame(None, 410, 230)
    app.MainLoop()

if __name__ == "__main__":
    main()