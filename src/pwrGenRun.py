#!/usr/bin/python
#-----------------------------------------------------------------------------
# Name:        uiRun.py
#
# Purpose:     This module is used to create the control panel to connect to the
#              Raspberry PI generator control by UDP.
#
# Author:      Yuancheng Liu
#
# Created:     2019/01/10
# Copyright:   YC @ Singtel Cyber Security Research & Development Laboratory
# License:     YC
#-----------------------------------------------------------------------------

import time
import json
import wx
import wx.gizmos as gizmos

import udpCom
import pwrGenGobal as gv
import pwrGenPanel as pl

UDP_PORT = 5005
PERIODIC = 250  # main UI loop call back period.(ms)
TEST_MD = True
RSP_IP = '127.0.0.1' if TEST_MD else '192.168.10.245'

#-----------------------------------------------------------------------------
#-----------------------------------------------------------------------------
class AppFrame(wx.Frame):
    """ Applicaiton main UI frame."""
    def __init__(self, parent, id, title):
        """ Init the UI and parameters """
        wx.Frame.__init__(self, parent, id, title, size=(800, 340))
        self.SetBackgroundColour(wx.Colour(200, 210, 200))
        self.SetIcon(wx.Icon(gv.ICO_PATH))
        # build the UI.
        self.SetSizer(self._buildUISizer())
        # Set the raspberry pi UDP connector.
        self.connector = udpCom.udpClient((RSP_IP, UDP_PORT))
        # Set the periodic call back
        self.lastPeriodicTime = { 'UI':time.time(), 'Data':time.time()}
        self.timer = wx.Timer(self)
        self.updateLock = False
        self.Bind(wx.EVT_TIMER, self.periodic)
        self.timer.Start(PERIODIC)  # every 500 ms
        # login to the raspberry PI and fetch the running state.
        # Fetch the connection state from raspberry PI.
        self.connectRsp('Login')
        # Fetch the load state from the raspberry PI.
        self.connectRsp('Load')
        # Fetch the generator state from the raspberry PI.
        self.connectRsp('Gen')
        # Added the state bar.
        self.statusbar = self.CreateStatusBar()
        self.Bind(wx.EVT_CLOSE, self.onClose)
        self.Refresh(False)
        print("AppFrame init finished.")

#--AppFrame---------------------------------------------------------------------
    def _buildUISizer(self):
        """ Build the main UI Sizer. """
        flagsR = wx.RIGHT | wx.ALIGN_CENTER_VERTICAL
        sizerAll = wx.BoxSizer(wx.VERTICAL)
        # Connection state display area.
        sizerAll.AddSpacer(5)
        sizerAll.Add(self._buildConnSizer(), flag=flagsR, border=2)
        sizerAll.AddSpacer(5)
        sizerAll.Add(wx.StaticLine(self, wx.ID_ANY, size=(800, -1),
                                   style=wx.LI_HORIZONTAL), flag=flagsR, border=2)
        sizerAll.AddSpacer(5)

        sizerInfo = wx.BoxSizer(wx.HORIZONTAL)
        # System load display panel.
        sizerInfo.AddSpacer(5)
        self.loadPanel = pl.PanelLoad(self)
        sizerInfo.Add(self.loadPanel, flag=flagsR, border=2)
        sizerInfo.AddSpacer(5)
        sizerInfo.Add(wx.StaticLine(self, wx.ID_ANY, size=(-1, 200),
                                    style=wx.LI_VERTICAL), flag=flagsR, border=2)
        sizerInfo.AddSpacer(5)
        # Generator information display panel.
        genSizer = wx.BoxSizer(wx.VERTICAL)
        genSizer.Add(wx.StaticText(
            self, -1, 'Generator Information:'), flag=flagsR, border=2)
        genSizer.AddSpacer(10)
        # - add infomation display panel.
        genSizer.Add(self._buildGenInfoSizer(), flag=flagsR, border=2)
        genSizer.AddSpacer(5)
        genSizer.Add(wx.StaticLine(self, wx.ID_ANY, size=(600, -1),
                                   style=wx.LI_HORIZONTAL), flag=flagsR, border=2)
        genSizer.AddSpacer(5)
        # - add the moto display panel.
        mSizer = wx.BoxSizer(wx.HORIZONTAL)
        self.MotoLedBt = wx.Button(self, label='Moto', size=(80, 30))
        self.MotoLedBt.SetBackgroundColour(wx.Colour('GRAY'))
        mSizer.Add(self.MotoLedBt, flag=wx.ALIGN_CENTER_HORIZONTAL, border=2)
        mSizer.AddSpacer(5)
        gv.iMotoImgPnl = pl.PanelMoto(self)
        mSizer.Add(gv.iMotoImgPnl, flag=flagsR, border=2)
        # - add the split line
        mSizer.AddSpacer(5)
        mSizer.Add(wx.StaticLine(self, wx.ID_ANY, size=(-1, 140),
                                 style=wx.LI_VERTICAL), flag=flagsR, border=2)
        mSizer.AddSpacer(5)
        # - add the pump display panel.
        mSizer.Add(self._buildPumpCtrlSizer(), flag=wx.ALIGN_CENTER_HORIZONTAL, border=2)
        mSizer.AddSpacer(10)
        gv.iPumpImgPnl = pl.PanelPump(self)
        mSizer.Add(gv.iPumpImgPnl, flag=flagsR, border=2)
        # - add the split line
        mSizer.AddSpacer(5)
        mSizer.Add(wx.StaticLine(self, wx.ID_ANY, size=(-1, 140),
                                 style=wx.LI_VERTICAL), flag=flagsR, border=2)
        mSizer.AddSpacer(5)
        # Added the system debug and control panel.
        self.sysPnl = pl.PanelCtrl(self)
        mSizer.Add(self.sysPnl, flag=flagsR, border=2)
        genSizer.Add(mSizer, flag=flagsR, border=2)

        sizerInfo.Add(genSizer, flag=flagsR, border=2)
        sizerAll.Add(sizerInfo, flag=flagsR, border=2)
        # - add the split line
        sizerAll.AddSpacer(5)
        sizerAll.Add(wx.StaticLine(self, wx.ID_ANY, size=(800, -1),
                                   style=wx.LI_HORIZONTAL), flag=flagsR, border=2)
        sizerAll.AddSpacer(5)
        return sizerAll

#-----------------------------------------------------------------------------
    def _buildConnSizer(self):
        """ build the components connection information display panel"""
        sizer = wx.GridSizer(1, 7, 5, 5)
        sizer.Add(wx.StaticText(self, -1, 'Connection State : '),
                  flag=wx.RIGHT | wx.ALIGN_CENTER_VERTICAL)
        sizer.AddSpacer(5)
        # Raspberry PI connection.
        self.rspLedBt = wx.Button(self, label='RsPI', size=(75, 30))
        self.rspLedBt.SetBackgroundColour(wx.Colour('Green'))
        sizer.Add(self.rspLedBt)
        # Serial port connection led state.
        self.serialLedBt = wx.Button(self, label='COMM', size=(75, 30))
        self.serialLedBt.SetBackgroundColour(wx.Colour('GRAY'))
        sizer.Add(self.serialLedBt)
        # PLC 1.
        self.plc1LedBt = wx.Button(self, label='PLC1', size=(75, 30))
        self.plc1LedBt.SetBackgroundColour(wx.Colour('GRAY'))
        sizer.Add(self.plc1LedBt)
        # PLC 2.
        self.plc2LedBt = wx.Button(self, label='PLC1', size=(75, 30))
        self.plc2LedBt.SetBackgroundColour(wx.Colour('GRAY'))
        sizer.Add(self.plc2LedBt)
        # PLC 3.
        self.plc3LedBt = wx.Button(self, label='PLC1', size=(75, 30))
        self.plc3LedBt.SetBackgroundColour(wx.Colour('GRAY'))
        sizer.Add(self.plc3LedBt)
        return sizer

#-----------------------------------------------------------------------------
    def _buildPumpCtrlSizer(self):
        """ Build the pump control sizer."""
        vbox = wx.BoxSizer(wx.VERTICAL)
        self.pumpLedBt = wx.Button(self, label='Pump', size=(80, 30))
        self.pumpLedBt.SetBackgroundColour(wx.Colour('GRAY'))
        vbox.Add(self.pumpLedBt, flag=wx.ALIGN_CENTER_HORIZONTAL, border=2)
        vbox.AddSpacer(10)
        vbox.Add(wx.StaticText(self, label="PumpSpeed"),
                 flag=wx.ALIGN_CENTER_HORIZONTAL, border=2)
        vbox.AddSpacer(10)
        self.pumpSPCB = wx.ComboBox(
            self, -1, choices=['off', 'low', 'high'], size=(80, 30))
        self.pumpSPCB.SetSelection(0)
        self.pumpSPCB.Bind(wx.EVT_COMBOBOX, self.onPumpSpdChange)
        vbox.Add(self.pumpSPCB, flag=wx.ALIGN_CENTER_HORIZONTAL, border=2)
        return vbox

#-----------------------------------------------------------------------------
    def _buildGenInfoSizer(self):
        """ Build the generator information display panel."""
        # LED area
        uSizer = wx.BoxSizer(wx.HORIZONTAL)
        flagsR = wx.RIGHT | wx.ALIGN_CENTER_VERTICAL
        # Frequence LED
        self.feqLedBt = wx.Button(self, label='Frequency', size=(80, 30))
        self.feqLedBt.SetBackgroundColour(wx.Colour('GRAY'))
        uSizer.Add(self.feqLedBt, flag=flagsR, border=2)
        self.feqLedDis = gizmos.LEDNumberCtrl(
            self, -1, size=(80, 35), style=gizmos.LED_ALIGN_CENTER)
        uSizer.Add(self.feqLedDis, flag=flagsR, border=2)
        uSizer.AddSpacer(10)
        # Voltage LED
        self.volLedBt = wx.Button(self, label='Voltage', size=(80, 30))
        self.volLedBt.SetBackgroundColour(wx.Colour('GRAY'))
        uSizer.Add(self.volLedBt, flag=flagsR, border=2)
        self.volLedDis = gizmos.LEDNumberCtrl(
            self, -1, size=(80, 35), style=gizmos.LED_ALIGN_CENTER)
        uSizer.Add(self.volLedDis, flag=flagsR, border=2)
        uSizer.AddSpacer(10)
        # Smoke LED
        self.smkIdc = wx.Button(
            self, label='Smoke [OFF]', size=(100, 30), name='smoke')
        self.smkIdc.SetBackgroundColour(wx.Colour('GRAY'))
        uSizer.Add(self.smkIdc, flag=flagsR, border=2)
        uSizer.AddSpacer(10)
        # Siren LED
        self.sirenIdc = wx.Button(
            self, label='Siren [OFF]', size=(100, 30), name='smoke')
        self.sirenIdc.SetBackgroundColour(wx.Colour('GRAY'))
        uSizer.Add(self.sirenIdc, flag=flagsR, border=2)
        uSizer.AddSpacer(10)
        return uSizer

#-----------------------------------------------------------------------------
    def connectRsp(self, evnt, parm=None):
        """ Try to connect to the raspberry pi and send cmd based on the 
            evnt setting.
        """
        if evnt == 'Login':
            # Log in and get the connection state.
            msgStr = json.dumps({'Cmd': 'Get', 'Parm': 'Con'})
            result = self.connector.sendMsg(msgStr, resp=True)
            self.setConnLED(result)
        elif evnt == 'Load':
            msgStr = json.dumps({'Cmd': 'Get', 'Parm': 'Load'})
            result = self.connector.sendMsg(msgStr, resp=True)
            self.setLoadsLED(result)
        elif evnt == 'Gen':
            msgStr = json.dumps({'Cmd': 'Get', 'Parm': 'Gen'})
            result = self.connector.sendMsg(msgStr, resp=True)
            self.SetGensLED(result)
        elif evnt == 'SetGen':
            msgStr = json.dumps({'Cmd': 'SetGen', 'Parm': parm})
            result = self.connector.sendMsg(msgStr, resp=True)
            self.SetGensLED(result)
        elif evnt == 'SetPLC':
            msgStr = json.dumps({'Cmd': 'SetPLC', 'Parm': parm})
            result = self.connector.sendMsg(msgStr, resp=True)
            self.SetGensLED(result)
        else:
            self.statusbar.SetStatusText("Can not handle the user action: %s" %str(evnt))

#-----------------------------------------------------------------------------
    def setConnLED(self, resultStr):
        """ Set and update the LED display in the connection state display area."""
        if resultStr is None:
            # Raspberry PI offline.
            self.rspLedBt.SetBackgroundColour(wx.Colour('GRAY'))
            self.serialLedBt.SetBackgroundColour(wx.Colour('GRAY'))
            self.plc1LedBt.SetBackgroundColour(wx.Colour('GRAY'))
            self.plc2LedBt.SetBackgroundColour(wx.Colour('GRAY'))
            self.plc3LedBt.SetBackgroundColour(wx.Colour('GRAY'))
        else:
            resultDict = json.loads(resultStr)
            if 'Serial' in resultDict.keys():
                colorStr = 'Green' if resultDict['Serial'] else 'GRAY'
                self.serialLedBt.SetBackgroundColour(wx.Colour(colorStr))
            if 'Plc1' in resultDict.keys():
                colorStr = 'Green' if resultDict['Plc1'] else 'GRAY'
                self.plc1LedBt.SetBackgroundColour(wx.Colour(colorStr))
            if 'Plc2' in resultDict.keys():
                colorStr = 'Green' if resultDict['Plc2'] else 'GRAY'
                self.plc2LedBt.SetBackgroundColour(wx.Colour(colorStr))
            if 'Plc3' in resultDict.keys():
                colorStr = 'Green' if resultDict['Plc3'] else 'GRAY'
                self.plc3LedBt.SetBackgroundColour(wx.Colour(colorStr))
        self.Refresh(False)

#-----------------------------------------------------------------------------
    def setLoadsLED(self, resultStr):
        """ Set the power loads LED state."""
        if resultStr is None:
            print("setLoadsLED: no response")
            return None
        resultDict = json.loads(resultStr)
        self.loadPanel.setLoadIndicator(resultDict)
        return True

#-----------------------------------------------------------------------------
    def SetGensLED(self, resultStr):
        """ Set all the generator's LED and indiator's state."""
        if resultStr is None:
            print("SetGensLED: no response")
        else:
            #print(resultStr)
            colorDict = {'green': 'Green', 'amber': 'Yellow', 'red': 'Red',
                         'on': 'Green', 'off': 'Gray', 'slow': 'Yellow', 'fast': 'Red'}
            resultDict = json.loads(resultStr)
            # frequence number display.
            if 'Freq' in resultDict.keys():
                self.feqLedDis.SetValue(str(resultDict['Freq']))
            # frequence led light.
            if 'Fled' in resultDict.keys():
                self.feqLedBt.SetBackgroundColour(
                    wx.Colour(colorDict[resultDict['Fled']]))
            # voltage number display.
            if 'Volt' in resultDict.keys():
                self.volLedDis.SetValue(str(resultDict['Volt']))
            # voltage led light.
            if 'Vled' in resultDict.keys():
                self.volLedBt.SetBackgroundColour(
                    wx.Colour(colorDict[resultDict['Vled']]))
            # motor led light.
            if 'Mled' in resultDict.keys():
                self.MotoLedBt.SetBackgroundColour(
                    wx.Colour(colorDict[resultDict['Mled']]))
            # pump led light.
            if 'Pled' in resultDict.keys():
                self.pumpLedBt.SetBackgroundColour(
                    wx.Colour(colorDict[resultDict['Pled']]))
            # smoke indicator.
            if 'Smok' in resultDict.keys():
                lb = 'Smoke [OFF]'if resultDict['Smok'] == 'off' else 'Smoke [ON ]'
                self.smkIdc.SetLabel(lb)
                self.smkIdc.SetBackgroundColour(
                    wx.Colour(colorDict[resultDict['Smok']]))
            # siren indicator.
            if 'Sirn' in resultDict.keys():
                (lb, cl) = ('Siren [ON ]', 'Red') if resultDict['Sirn'] == 'on' else (
                    'Siren [OFF]', 'Gray')
                self.sirenIdc.SetLabel(lb)
                self.sirenIdc.SetBackgroundColour(wx.Colour(cl))
            # Motor speed indicator.
            if 'Mspd' in resultDict.keys():
                gv.iMotoImgPnl.setMotoSpeed(resultDict['Mspd'])
            # Pump speed indicator.
            if 'Pspd' in resultDict.keys():
                gv.iPumpImgPnl.setPumpSpeed(resultDict['Pspd'])
            # All sensor power indicator.
            if 'Spwr' in resultDict.keys():
                self.sysPnl.setPwrLed('Spwr', colorDict[resultDict['Spwr']])
            # Main power indicator.
            if 'Mpwr' in resultDict.keys():
                self.sysPnl.setPwrLed('Mpwr', colorDict[resultDict['Mpwr']])

            self.Refresh(False)

#-----------------------------------------------------------------------------
    def onPumpSpdChange(self, evnt):
        """ Handle user's pump speed change action from the dropdown menu."""
        msgStr = self.pumpSPCB.GetValue()
        print("AppFrame: Set pump speed to %s " % msgStr)
        self.connectRsp('SetPLC', parm={'Pspd': msgStr})

#--AppFrame---------------------------------------------------------------------
    def periodic(self, event):
        """ Call back every periodic time."""
        now = time.time()
        if not self.updateLock:
            if now - self.lastPeriodicTime['UI'] >= gv.iUpdateRate:
                #print("main frame update at %s" % str(now))
                self.lastPeriodicTime['UI'] = now
                gv.iMotoImgPnl.updateDisplay()
                gv.iPumpImgPnl.updateDisplay()
            if now - self.lastPeriodicTime['Data'] >= 2*gv.iUpdateRate:
                self.lastPeriodicTime['Data'] = now
                self.connectRsp('Load')
                self.connectRsp('Gen')

#-----------------------------------------------------------------------------
    def onClose(self, event):
        self.timer.Stop()
        self.Destroy()

#-----------------------------------------------------------------------------
#-----------------------------------------------------------------------------
class MyApp(wx.App):
    def OnInit(self):
        gv.iMainFrame = AppFrame(None, -1, gv.APP_NAME)
        gv.iMainFrame.Show(True)
        return True

app = MyApp(0)
app.MainLoop()
