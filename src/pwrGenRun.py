#!/usr/bin/python
#-----------------------------------------------------------------------------
# Name:        uiRun.py
#
# Purpose:     This module is used to create the main wx frame.
#
# Author:      Yuancheng Liu
#
# Created:     2019/01/10
# Copyright:   YC @ Singtel Cyber Security Research & Development Laboratory
# License:     YC
#-----------------------------------------------------------------------------
import os, sys
import time
import wx
import wx.gizmos as gizmos
import udpCom
import pwrGenGobal as gv
import pwrGenPanel as pl
import pwrGenMgr as gm
PERIODIC = 100      # update in every 500ms
UDP_PORT = 5005

#-----------------------------------------------------------------------------
#-----------------------------------------------------------------------------
class UIFrame(wx.Frame):
    """ URL/IP gps position finder main UI frame."""
    def __init__(self, parent, id, title):
        """ Init the UI and parameters """
        wx.Frame.__init__(self, parent, id, title, size=(800, 300))
        self.SetBackgroundColour(wx.Colour(200, 210, 200))
        self.SetIcon(wx.Icon(gv.ICO_PATH))
        self.loadCbList = []
        self.ledList = []
        self.SetSizer(self._buidUISizer())


        # Set the periodic call back
        self.lastPeriodicTime = time.time()
        self.timer = wx.Timer(self)
        self.updateLock = False
        self.Bind(wx.EVT_TIMER, self.periodic)
        self.timer.Start(PERIODIC)  # every 500 ms
        
        self.statusbar = self.CreateStatusBar()
        #self.statusbar.SetStatusText('COM Msg to Arduino: %s ' % str(self.parmList))
        self.Bind(wx.EVT_CLOSE, self.onClose)

        print("Program init finished.")


#--UIFrame---------------------------------------------------------------------
    def _buidUISizer(self):
        """ Build the main UI Sizer. """
        flagsR = wx.RIGHT | wx.ALIGN_CENTER_VERTICAL
        sizerAll= wx.BoxSizer(wx.HORIZONTAL)
        # System load display panel.
        sizerAll.AddSpacer(5)
        self.loadPanel = pl.PanelLoad(self)
        sizerAll.Add(self.loadPanel, flag=flagsR, border=2)
        sizerAll.AddSpacer(5)
        sizerAll.Add(wx.StaticLine(self, wx.ID_ANY, size=(-1, 200),
                            style=wx.LI_VERTICAL), flag=flagsR, border=2)
        sizerAll.AddSpacer(5)
        
        genSizer = wx.BoxSizer(wx.VERTICAL)

        genSizer.Add(wx.StaticText(self, -1, 'Generator Information:'), flag=flagsR, border=2)
        genSizer.AddSpacer(10)
        # LED area
        uSizer = wx.BoxSizer(wx.HORIZONTAL)
        # Frequence LED
        self.feqLedBt = wx.Button(self, label='Frequency', size=(80, 30))
        self.feqLedBt.SetBackgroundColour(wx.Colour('GRAY'))
        uSizer.Add(self.feqLedBt, flag=flagsR, border=2)
        self.feqLedDis = gizmos.LEDNumberCtrl(self, -1, size = (80, 30), style=gizmos.LED_ALIGN_CENTER)
        uSizer.Add(self.feqLedDis, flag=flagsR, border=2)
        uSizer.AddSpacer(10)
        # Voltage LED
        self.volLedBt = wx.Button(self, label='Voltage', size=(80, 30))
        self.volLedBt.SetBackgroundColour(wx.Colour('GRAY'))
        uSizer.Add(self.volLedBt, flag=flagsR, border=2)
        self.volLedDis = gizmos.LEDNumberCtrl(self, -1, size = (80, 30), style=gizmos.LED_ALIGN_CENTER)
        uSizer.Add(self.volLedDis, flag=flagsR, border=2)
        uSizer.AddSpacer(10)
        # Smoke LED
        self.smkIdc = wx.Button(self, label='Smoke [OFF]', size=(100, 30), name='smoke')
        self.smkIdc.SetBackgroundColour(wx.Colour('GRAY'))
        uSizer.Add(self.smkIdc, flag=flagsR, border=2)
        uSizer.AddSpacer(10)
        # Siren LED
        self.sirenIdc = wx.Button(self, label='Siren [OFF] ', size=(100, 30), name='smoke')
        self.sirenIdc.SetBackgroundColour(wx.Colour('GRAY'))
        uSizer.Add(self.sirenIdc, flag=flagsR, border=2)
        uSizer.AddSpacer(10)
        

        genSizer.Add(uSizer, flag=flagsR, border=2)

        genSizer.AddSpacer(5)
        genSizer.Add(wx.StaticLine(self, wx.ID_ANY, size=(600, -1),
                    style=wx.LI_HORIZONTAL), flag=flagsR, border=2)
        genSizer.AddSpacer(5)


        mSizer = wx.BoxSizer(wx.HORIZONTAL)
        
        
        self.MotoLedBt = wx.Button(self, label='Moto', size=(80, 30))
        self.MotoLedBt.SetBackgroundColour(wx.Colour('GRAY'))
        mSizer.Add(self.MotoLedBt, flag=wx.ALIGN_CENTER_HORIZONTAL, border=2)
        
        mSizer.AddSpacer(5)
        gv.iMotoImgPnl = pl.PanelMoto(self)
        mSizer.Add(gv.iMotoImgPnl, flag=flagsR, border=2)
        mSizer.AddSpacer(5)
        mSizer.Add(wx.StaticLine(self, wx.ID_ANY, size=(-1, 140),
                                 style=wx.LI_VERTICAL), flag=flagsR, border=2)

        # Col 1: moto
        mSizer.AddSpacer(5)

        vbox = wx.BoxSizer(wx.VERTICAL)
        
        self.pumpLedBt = wx.Button(self, label='Pump', size=(80, 30))
        self.pumpLedBt.SetBackgroundColour(wx.Colour('GRAY'))
        vbox.Add(self.pumpLedBt, flag=wx.ALIGN_CENTER_HORIZONTAL, border=2)
        vbox.AddSpacer(10)

        vbox.Add(wx.StaticText(self, label="PumpSpeed"), flag=wx.ALIGN_CENTER_HORIZONTAL, border=2)
        vbox.AddSpacer(10)
        self.pumpSPCB= wx.ComboBox(self, -1, choices=['off', 'low', 'high'], size=(80, 30))
        self.pumpSPCB.SetSelection(0)
        self.pumpSPCB.Bind(wx.EVT_COMBOBOX, self.onPumpSpdChange)
        vbox.Add(self.pumpSPCB, flag=wx.ALIGN_CENTER_HORIZONTAL, border=2)
        mSizer.Add(vbox, flag=wx.ALIGN_CENTER_HORIZONTAL, border=2)
        mSizer.AddSpacer(10)
        gv.iPumpImgPnl = pl.PanelPump(self)
        mSizer.Add(gv.iPumpImgPnl, flag=flagsR, border=2)
        mSizer.AddSpacer(5)
        mSizer.Add(wx.StaticLine(self, wx.ID_ANY, size=(-1, 140),
                            style=wx.LI_VERTICAL), flag=flagsR, border=2)

        self.sysPnl = pl.PanelCtrl(self)
        mSizer.Add(self.sysPnl, flag=flagsR, border=2)



        genSizer.Add(mSizer, flag=flagsR, border=2)

        sizerAll.Add(genSizer, flag=flagsR, border=2)



        return sizerAll


    def onCheck(self, evnt):
        cb = evnt.GetEventObject()
        idx = int(cb.GetLabel().split('[')[-1][0])
        val = 1 if cb.GetValue() else 0
        gv.iGnMgr.setLoad([idx],[val])


#--UIFrame---------------------------------------------------------------------
    def periodic(self, event):
        """ Call back every periodic time."""
        now = time.time()
        if (not self.updateLock) and now - self.lastPeriodicTime >= gv.iUpdateRate:
            #print("main frame update at %s" % str(now))
            self.lastPeriodicTime = now

            gv.iMotoImgPnl.updateDisplay()
            gv.iPumpImgPnl.updateDisplay()

            result = self.client.sendMsg('Get', resp=True)
            result = result.decode('utf-8')
            freq, vol, smk, siren, ldNum = result.split(';')
            self.setLEDVal(0, str(freq))
            self.setLEDVal(1, str(vol))
            self.setLEDVal(2, ldNum)
            if smk != 'off':
                gv.iCtrlPanel.smkIdc.SetBackgroundColour(wx.Colour('RED'))
            else:
                gv.iCtrlPanel.smkIdc.SetBackgroundColour(wx.Colour('GRAY'))

            if siren != 'off':
                gv.iCtrlPanel.sirenIdc.SetBackgroundColour(wx.Colour('RED'))
            else:
                gv.iCtrlPanel.sirenIdc.SetBackgroundColour(wx.Colour('GRAY'))

            #self.parmList[5] = gv.iGnMgr.getMotorSp()
            #self.parmList[6] = gv.iGnMgr.getPumpSp()
            self.statusbar.SetStatusText('COM Msg to Arduino: %s ' % str(self.parmList))

    def onPumpSpdChange(self, event):
        result = self.client.sendMsg('Set;'+str(self.pumpLedBt.GetSelection()), resp=True)

    def setLEDVal(self, idx, val):
        self.ledList[idx].SetValue(str(val))

#--<telloFrame>----------------------------------------------------------------
    def onClose(self, event):
        """ Stop all the thread and close the UI."""
        gv.iGnMgr.stop()
        self.timer.Stop()
        self.Destroy()

#-----------------------------------------------------------------------------
#-----------------------------------------------------------------------------
class MyApp(wx.App):
    def OnInit(self):
        gv.iMainFrame = UIFrame(None, -1, gv.APP_NAME)
        gv.iMainFrame.Show(True)
        return True

app = MyApp(0)
app.MainLoop()
