#!/usr/bin/python
#-----------------------------------------------------------------------------
# Name:        pwSubDisplay.py
#
# Purpose:     This module is used to create a transparent, no window board live 
#              substation control parameter simulation display frame show overlay 
#              on top of the CSI OT-Platform HMI program.
#
# Author:      Yuancheng Liu, Shantanu Chakrabarty, Zhang Guihai
#
# Created:     2020/10/2
# Copyright:   Singtel Cyber Security Research & Development Laboratory
# License:     N.A
#-----------------------------------------------------------------------------

import wx
import pwrGenGobal as gv

DEF_POS = (300, 300)    # default show up position on screen used for local test.

#-----------------------------------------------------------------------------
#-----------------------------------------------------------------------------
class SubDisplayFrame(wx.Frame):
    """ Power substation module live situation display frame."""

    def __init__(self, parent, width, height, position=DEF_POS):
        wx.Frame.__init__(self, parent, title="SubstationLiveDisplay",
                          style=wx.MINIMIZE_BOX | wx.STAY_ON_TOP)
        self.SetBackgroundColour(wx.Colour('BLACK'))
        # flag to identify whether can date the display panel.
        self.updateFlag = True
        self.parmDialog = None  # pop up dialog for change/select paramters.
        # Build the main UI.
        self.SetSizerAndFit(self.buidUISizer())
        self.SetTransparent(gv.gTranspPct*255//100)
        self.SetPosition(position)
        self.Bind(wx.EVT_CLOSE, self.onCloseWindow)
        self.Show()

    #-----------------------------------------------------------------------------
    def buidUISizer(self):
        """ Build the UI and return the wx.sizer hold all the UI components. """
        sizer = wx.BoxSizer(wx.VERTICAL)
        elemSize= (40,20)
        # build the upper panel.
        self.upPnl = wx.Panel(self, size=(400, 50))
        self.upPnl.SetBackgroundColour(wx.Colour('Gray'))
        self.vkBt = wx.Button(self.upPnl, wx.ID_ANY, 'Vk [0.0]', pos=(5, 15))
        self.vkBt.Bind(wx.EVT_BUTTON, self.onParmChange)
        self.vkBt.SetToolTip('Voltage measurement: k ')

        self.swBt = wx.CheckBox(
            self.upPnl, wx.ID_ANY, label='Switch', pos=(100, 25))
        self.swBt.Bind(wx.EVT_CHECKBOX, self.turnSw)
        self.tkmBt = wx.Button(self.upPnl, wx.ID_ANY, 'Tkm [0.0]',  pos=(200, 15))
        self.tkmBt.Bind(wx.EVT_BUTTON, self.onParmChange)
        self.vmBt = wx.Button(self.upPnl, wx.ID_ANY, 'Vm [0.0]',  pos=(320, 15))
        self.vmBt.Bind(wx.EVT_BUTTON, self.onParmChange)
        self.vmBt.SetToolTip('Voltage measurement: m ')

        sizer.Add(self.upPnl, flag=wx.CENTER, border=2)

        # build the display area.
        gv.iPerSImgPnl = PanelSub(self)
        sizer.Add(gv.iPerSImgPnl, flag=wx.CENTER, border=2)

        # build the bottum panel.
        self.downPnl = wx.Panel(self, size=(400, 50))
        self.downPnl.SetBackgroundColour(wx.Colour('Gray'))
        self.InjBt = wx.Button(self.downPnl, wx.ID_ANY, 'Inj_I [0.0]',  pos=(5, 10))
        self.InjBt.Bind(wx.EVT_BUTTON, self.onParmChange)
        self.InjBt.SetToolTip('Injection measurement : \nInj_I = Ing-P[k],Q[k]')

        self.FmjBt = wx.Button(self.downPnl, wx.ID_ANY, 'Flows [0.0]',  pos=(200, 5))
        self.FmjBt.Bind(wx.EVT_BUTTON, self.onParmChange)
        self.FmjBt.SetToolTip('Flow measurements: \n P[km], Q[km] \n P[mk], Q[mk]')

        self.Inj2Bt = wx.Button(self.downPnl, wx.ID_ANY, 'Inj_O [0.0]',  pos=(320, 10))
        self.Inj2Bt.Bind(wx.EVT_BUTTON, self.onParmChange)
        self.Inj2Bt.SetToolTip('Injection measurement : \nInj_O = Ing-P[m],Q[m]')
        sizer.Add(self.downPnl, flag=wx.CENTER, border=2)

        return sizer

    #-----------------------------------------------------------------------------
    def onParmChange(self, event):
        """ Stop the mail frame update and pop-up the paramenter change dialog.
        Args:
            event ([wx.EVT_BUTTON]): [button press event]
        """
        btObj = event.GetEventObject()
        lb = btObj.GetLabel().split(' ')[0]
        if self.parmDialog:
            self.parmDialog.Destroy()
            self.parmDialog = None
        self.updateFlag = False # disable display update
        self.parmDialog = wx.SingleChoiceDialog(self, lb, 'Value', ['0', '1'])
        resp = self.parmDialog.ShowModal()
        self.updateFlag = True # enable display update

    #-----------------------------------------------------------------------------
    def updateDisplay(self):
        """ update the diaplay panel."""
        if self.updateFlag:
            gv.iPerSImgPnl.updateDisplay()
    
        # update the parameter indicators.


    #-----------------------------------------------------------------------------
    def turnSw(self, event):
        """ Handle the switch on/off check box pressed by user.
        Args:
            event ([wx.EVT_CHECKBOX]): [description]
        """
        gv.iPerSImgPnl.setSwitch(self.swBt.IsChecked())

    #-----------------------------------------------------------------------------
    def onCloseWindow(self, evt):
        """ Close the window and reset the gv parameters."""
        #gv.iPerSImgPnl = None
        self.Destroy()

#-----------------------------------------------------------------------------
#-----------------------------------------------------------------------------
class PanelSub(wx.Panel):
    """ Panel to draw the substation grid circuit diagram live situation. """
    def __init__(self, parent, panelSize=(400, 80)):
        wx.Panel.__init__(self, parent, size=panelSize)
        #self.SetBackgroundColour(wx.Colour(200, 200, 200))
        self.SetBackgroundColour(wx.Colour('Gray'))
        self.panelSize = panelSize
        self.swOn = False
        # Setup the paint display function.
        self.Bind(wx.EVT_PAINT, self.onPaint)
        self.SetDoubleBuffered(True)

#-----------------------------------------------------------------------------
    def setSwitch(self, tag):
        """ Update the substaion switch on/off state.
        Args:
            tag ([bool]): true-switch on, flase - switch off.
        """
        self.swOn= tag
        self.updateDisplay()

#-----------------------------------------------------------------------------
    def getTransIcon(self, posX, n):
        """ Draw the points of the transformer spring.(Currently not used.)
        Args:
            posX ([int]): horizontal position of the transformer spring.
            n ([int]): num of points in on side of the spring.

        Returns:
            [int list]: spring points list.
        """
        ptList = []
        dlt = 30//n
        for i in range(2*n):
            px = posX+5 if i % 2 == 0 else posX
            py = 10 + dlt*i
            ptList.append((px, py))
        return ptList
        
#-----------------------------------------------------------------------------
    def onPaint(self, evt):
        """ Paint the panel.
        Args:
            evt ([wx.EVT_PAINT]): [description]
        """
        # Add the Device context to draw the background.
        dc = wx.PaintDC(self)
        # Add the Graphics Context to draw the components.
        gc = wx.GraphicsContext.Create(dc)
        path = gc.CreatePath()
        
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
        #dc.DrawLines(self.getTransIcon(220, 6))
        gc.SetPen(wx.Pen(color, width=2, style=wx.PENSTYLE_SOLID))
        path.AddCircle(220, 40, 15)

        # translater R
        color = 'Blue' if self.swOn else 'White'
        dc.SetPen(wx.Pen(color, width=2, style=wx.PENSTYLE_SOLID))
        dc.DrawLine(245, 40, 400, 40)
        #dc.DrawLines(self.getTransIcon(240, 10))
        gc.SetPen(wx.Pen(color, width=2, style=wx.PENSTYLE_SOLID))
        path.AddCircle(240, 40, 15)

        dc.DrawLine(360, 0, 360, 80)

        # Reference line
        dc.SetPen(wx.Pen('White', width=1, style=wx.PENSTYLE_DOT_DASH))
        dc.DrawLine(100, 40, 100, 0)
        dc.DrawLine(270, 40, 270, 80)

        path.CloseSubpath()
        gc.DrawPath(path,0)

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
class stateManager(object):
    """ Manager module to save the current system state. Add the parameter calculation 
        formula in this class.
    """ 
    def __init__(self):
        self.parmDict = {
            'Vk':       0.0,
            'Inj_I':    0.0,
            'Switch':   0,
            'Tkm':      0.0,
            'Flows':    0.0,
            'Vm':       0.0,
            'Ing_O':    0.0
        }

#-----------------------------------------------------------------------------
    def getVal(self, keyStr):
        if keyStr in self.parmDict.keys():
            return self.parmDict[keyStr]

#-----------------------------------------------------------------------------
    def setVal(self, keyStr, value):
        if keyStr in self.parmDict.keys():
            self.parmDict[keyStr] = value

#-----------------------------------------------------------------------------
    def changeRelated(self):
        """ change the related parameter's value if on parameter is changed.
        """
        pass
        # TODO: Add Shantanu Chakrabarty's formular here.

#-----------------------------------------------------------------------------
#-----------------------------------------------------------------------------
def main():
    """ Main function used for local test. """
    app = wx.App()
    mainFrame = SubDisplayFrame(None, 410, 230)
    app.MainLoop()

if __name__ == "__main__":
    main()
