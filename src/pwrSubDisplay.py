#!/usr/bin/python
#-----------------------------------------------------------------------------
# Name:        pwSubDisplay.py
#
# Purpose:     This module is used to create a transparent, no window board live 
#              substation control parameter simulation display frame show overlay 
#              on top of the CSI OT-Platform HMI program.
#
# Author:      Yuancheng Liu, Zhang Guihai
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
        elemSize= (40,20)
        # build the upper panel.
        self.upPnl = wx.Panel(self, size=(400, 50))
        self.upPnl.SetBackgroundColour(wx.Colour('GREEN'))
        self.vkBt = wx.Button(self.upPnl, wx.ID_ANY, 'Vk [0.0]', (5, 15))
        self.swBt = wx.CheckBox(
            self.upPnl, wx.ID_ANY, label='Switch', pos=(100, 25))
        self.swBt.Bind(wx.EVT_CHECKBOX, self.turnSw)

        self.tkmBt = wx.Button(self.upPnl, wx.ID_ANY, 'Tkm [0.0]', (200, 15))
        self.vmBt = wx.Button(self.upPnl, wx.ID_ANY, 'Vm [0.0]', (320, 15))
        sizer.Add(self.upPnl, flag=wx.CENTER, border=2)
        
        # build the display area.
        gv.iPerSImgPnl = PanelSub(self)
        sizer.Add(gv.iPerSImgPnl, flag=wx.CENTER, border=2)

        # build the bottum panel.
        self.downPnl = wx.Panel(self, size =(400, 50))
        self.downPnl.SetBackgroundColour(wx.Colour('RED'))
        self.InjBt = wx.Button(self.downPnl, wx.ID_ANY, 'Inj [0.0]', (5, 10))
        self.FmjBt = wx.Button(self.downPnl, wx.ID_ANY, 'Forms [0.0]', (200, 5))
        self.Inj2Bt = wx.Button(self.downPnl, wx.ID_ANY, 'Inj [0.0]', (320, 10))
        sizer.Add(self.downPnl, flag=wx.CENTER, border=2)

        return sizer

    def turnSw(self, event):
        gv.iPerSImgPnl.setSwitch(self.swBt.IsChecked())

    #-----------------------------------------------------------------------------
    def onCloseWindow(self, evt):
        """ Close the window and reset the gv parameters."""
        #gv.iPerSImgPnl = None
        self.Destroy()

#-----------------------------------------------------------------------------
#-----------------------------------------------------------------------------
class PanelSub(wx.Panel):
    """ Panel to draw the power generator components live situation. """
    def __init__(self, parent, panelSize=(400, 80)):
        wx.Panel.__init__(self, parent, size=panelSize)
        #self.SetBackgroundColour(wx.Colour(200, 200, 200))
        self.SetBackgroundColour(wx.Colour('BLACK'))
        self.panelSize = panelSize
        self.swOn = False

        # Setup the paint display function.
        self.Bind(wx.EVT_PAINT, self.onPaint)
        self.SetDoubleBuffered(True)

#-----------------------------------------------------------------------------
    def setSwitch(self, tag):
        self.swOn= tag
        self.updateDisplay()

#-----------------------------------------------------------------------------
    def getTransIcon(self, posX, n):
        ptList = []
        dlt = 30//n
        for i in range(2*n):
            px = posX+5 if i % 2 == 0 else posX
            py = 10 + dlt*i
            ptList.append((px, py))
        return ptList
        
#-----------------------------------------------------------------------------
    def onPaint(self, evt):
        dc = wx.PaintDC(self)
        print("In paint function.")

        # Draw the background.
        dc.SetPen(wx.Pen('Green', width=2, style=wx.PENSTYLE_SOLID))
        dc.DrawLine(40, 0, 40, 80)
        dc.DrawLine(0, 40, 100, 40)
        


        # Switch
        color = 'Green' if self.swOn else 'White'
        dc.SetPen(wx.Pen(color, width=2, style=wx.PENSTYLE_SOLID))
        dc.DrawCircle(100, 40, 3)
        swY = 40 if self.swOn else 30
        dc.DrawLine(100, 40, 140, swY)

        # translater L
        dc.DrawLine(140, 40, 220, 40)
        dc.DrawLines(self.getTransIcon(220, 6))
        # translater R
        color = 'Blue' if self.swOn else 'White'
        dc.SetPen(wx.Pen(color, width=2, style=wx.PENSTYLE_SOLID))
        dc.DrawLine(245, 40, 400, 40)
        dc.DrawLines(self.getTransIcon(240, 10))
        dc.DrawLine(360, 0, 360, 80)

        # Reference line
        dc.SetPen(wx.Pen('White', width=1, style=wx.PENSTYLE_DOT_DASH))
        dc.DrawLine(100, 40, 100, 0)
        dc.DrawLine(270, 40, 270, 80)


#-----------------------------------------------------------------------------
    def updateDisplay(self, updateFlag=None):
        """ Set/Update the display: if called as updateDisplay() the function will 
            update the panel, if called as updateDisplay(updateFlag=?) the function
            will set the self update flag.
        """
        #self.toggle = not self.toggle # change the toggle flag every time we updated display
        self.Refresh(True)
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
