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
import json
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
        self.statusbar = self.CreateStatusBar()
        self.SetPosition(position)
        self.Bind(wx.EVT_CLOSE, self.onCloseWindow)
        self.Show()

    #-----------------------------------------------------------------------------
    def buidUISizer(self):
        """ Build the UI and return the wx.sizer hold all the UI components. """
        sizer = wx.BoxSizer(wx.VERTICAL)
        #elemSize= (40,20)
        # build the upper panel.
        self.upPnl = wx.Panel(self, size=(400, 50))
        self.upPnl.SetBackgroundColour(wx.Colour('Gray'))
        self.vkBt = wx.Button(self.upPnl, wx.ID_ANY, 'Vk [0.0]', style=wx.BU_LEFT,size=(90,20), pos=(5, 15))
        self.vkBt.Bind(wx.EVT_BUTTON, self.onParmChange)
        self.vkBt.SetToolTip('Voltage measurement: k ')

        self.swBt = wx.CheckBox(
            self.upPnl, wx.ID_ANY, label='Switch', pos=(100, 25))
        self.swBt.SetValue(1)
        self.swBt.Bind(wx.EVT_CHECKBOX, self.turnSw)
        self.tkmBt = wx.Button(self.upPnl, wx.ID_ANY, 'Tkm [0.0]', style=wx.BU_LEFT, pos=(200, 15))
        self.tkmBt.Bind(wx.EVT_BUTTON, self.onParmChange)
        self.vmBt = wx.Button(self.upPnl, wx.ID_ANY, 'Vm [0.0]',style=wx.BU_LEFT, pos=(300, 15))
        self.vmBt.Bind(wx.EVT_BUTTON, self.onParmChange)
        self.vmBt.SetToolTip('Voltage measurement: m ')

        sizer.Add(self.upPnl, flag=wx.CENTER, border=2)

        # build the display area.
        gv.iPerSImgPnl = PanelSub(self)
        sizer.Add(gv.iPerSImgPnl, flag=wx.CENTER, border=2)

        # build the bottum panel.
        self.downPnl = wx.Panel(self, size=(400, 80))
        self.downPnl.SetBackgroundColour(wx.Colour('Gray'))
        self.InjBt = wx.Button(self.downPnl, wx.ID_ANY, 'Pk:0\nQk:0',style=wx.BU_LEFT, size=(100,40), pos=(5, 2))
        self.InjBt.Bind(wx.EVT_BUTTON, self.onParmChange)
        self.InjBt.SetToolTip('Injection measurement : \nInj_I = Ing-P[k],Q[k]')

        self.FmjBt = wx.Button(self.downPnl, wx.ID_ANY, 'Pkm:0 Qkm:0\nPmk:0 Qmk:0', style=wx.BU_LEFT,size=(160,40), pos=(120, 2))
        self.FmjBt.Bind(wx.EVT_BUTTON, self.onParmChange)
        self.FmjBt.SetToolTip('Flow measurements: \n P[km], P[mk]\n,Q[km], Q[mk]')

        self.Inj2Bt = wx.Button(self.downPnl, wx.ID_ANY, 'Pm: 0\nQm:0', style=wx.BU_LEFT, size=(90,40),  pos=(300, 2))
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

    def parseMemStr(self, memStr):
        """[summary]
        Args:
            memStr ([type]): [description]
        """
        memDict = json.loads(memStr)
        self.statusbar.SetStatusText("M:%s" %str(memDict))
        # Check whether the display switch state is same as the data.
        #if(bool(memDict['ff02']) != gv.iPerSImgPnl.swOn):
        #    self.swBt.SetValue(bool(memDict['ff02']))
        #    gv.iPerSImgPnl.setElement('Sw', bool(memDict['ff02']))
        self.vkBt.SetLabel("Vk:%.7s" %memDict['ff08'])
        self.InjBt.SetLabel("Pk:%.7s\nQk:%.7s" %(memDict['ff04'], memDict['ff05']))
        self.tkmBt.SetLabel("Tkm: - ")
        if gv.iPerSImgPnl.swOn:
            self.vmBt.SetLabel("Vm:%.7s" %memDict['ff09'])
            self.FmjBt.SetLabel("Pkm:%.5s Pmk:%.6s\nQkm:%.5s Qmk:%.6s" %(memDict['ff00'], memDict['ff03'], memDict['ff01'], memDict['ff04']))
            #self.InjBt.SetLabel("Inj_I \n -P[k]:%s\n-Q[k]:%s" %(memDict['ff04'], memDict['ff05']))
            self.Inj2Bt.SetLabel("Pm:%.7s\nQm:%.7s" %(memDict['ff06'], memDict['ff07']))
        else: 
            self.vmBt.SetLabel("Vm:%s" % '0')
            self.FmjBt.SetLabel("Pkm:%s Pmk:%s\nQkm:%s Qmk:%s" % ('0', '0', '0', '0'))
            #self.InjBt.SetLabel("Inj_I \n -P[k]:%s\n-Q[k]:%s" % ('0', '0'))
            self.Inj2Bt.SetLabel("Pm:%s\n-Qm:%s" % ('0', '0'))

    #-----------------------------------------------------------------------------
    def turnSw(self, event):
        """ Handle the switch on/off check box pressed by user.
        Args:
            event ([wx.EVT_CHECKBOX]): [description]
        """
        gv.iPerSImgPnl.setElement('Sw',self.swBt.IsChecked())
        if gv.iMainFrame:
            val = 'on' if self.swBt.IsChecked() else 'off'
            plcDict = {'Mpwr':val}
            gv.iMainFrame.connectReq('SetPLC', parm=plcDict)

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
        self.swOn = True
        self.toggleF = True #display toggle flag.
        self.flowCount = 0  #flow animation count
        # Setup the paint display function.
        self.Bind(wx.EVT_PAINT, self.onPaint)
        self.SetDoubleBuffered(True)

#-----------------------------------------------------------------------------
    def setElement(self, tag, val):
        """ Update the substaion' component state.
        Args:
            tag ([String]): [String tag] example:tag= Sw, val: true-switch on, flase - switch off.
            val ([]): [description]
        """
        if tag == "Sw":
            self.swOn = val
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

        lineStyle = wx.PENSTYLE_SOLID
        # Draw the background.
        dc.SetPen(wx.Pen('Green', width=2, style=lineStyle))
        dc.DrawLine(40, 0, 40, 80)
        dc.DrawLine(0, 40, 100, 40)

        #pts = ((f))

        # Switch
        color = 'Green' if self.swOn else 'White'
        dc.SetPen(wx.Pen(color, width=2, style=lineStyle))
        dc.DrawCircle(100, 40, 3)
        swY = 40 if self.swOn else 30
        dc.DrawLine(100, 40, 140, swY)

        # translater L
        dc.DrawLine(140, 40, 185, 40)
        #dc.DrawLines(self.getTransIcon(220, 6))
        gc.SetPen(wx.Pen(color, width=2, style=lineStyle))
        path.AddCircle(200, 40, 15)

        # translater R
        color = 'Blue' if self.swOn else 'White'
        dc.SetPen(wx.Pen(color, width=2, style=lineStyle))
        dc.DrawLine(235, 40, 400, 40)
        #dc.DrawLines(self.getTransIcon(240, 10))
        gc.SetPen(wx.Pen(color, width=2, style=lineStyle))
        path.AddCircle(220, 40, 15)

        dc.DrawLine(360, 0, 360, 80)

        # Reference line
        dc.SetPen(wx.Pen('White', width=1, style=wx.PENSTYLE_DOT_DASH))
        dc.DrawLine(100, 40, 100, 0)
        dc.DrawLine(250, 40, 250, 80)

        path.CloseSubpath()
        gc.DrawPath(path,0)

        dc.SetPen(wx.Pen('Black', width=1, style=wx.PENSTYLE_SOLID))
        dc.DrawText("Inj_I:", 10, 60)
        dc.DrawText("Flow:", 130, 60)
        dc.DrawText("Inj_O:", 310, 60)
        # change the display toggle flag
        self.toggleF = not self.toggleF

        # draw the pwr flow arrow
        limit = 400 if self.swOn else 100
        if self.flowCount > limit: self.flowCount = 0

        dc.SetPen(wx.Pen('black', width=1, style=lineStyle))
        #dc.DrawLine(self.flowCount+10, 40, self.flowCount, 45)
        #dc.DrawLine(self.flowCount+10, 40, self.flowCount, 35)
        #dc.DrawRectangle(self.flowCount, 36, 8, 8)
        for i in range(self.flowCount//40+1):
            posX = max(0,self.flowCount - i*40)
            color = 'Green' if posX < 210 else 'Blue'
            dc.SetBrush(wx.Brush(color))
            dc.DrawRectangle(posX, 36, 8, 8)
        
        self.flowCount += 10

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

        self.memDict = {
            'ff00': 0,  #
            'ff01': 0,
            'ff02': 0,
            'ff03': 0,
            'ff04': 0,
            'ff05': 0,
            'ff06': 0,
            'ff07': 0,
            'ff08': 0,
            'ff09': 0,
            'ff10': 0,
            'ff11': 0,
            'ff12': 0,
            'ff13': 0,
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
