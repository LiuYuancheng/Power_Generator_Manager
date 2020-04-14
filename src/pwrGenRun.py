#!/usr/bin/python
#-----------------------------------------------------------------------------
# Name:        uiRun.py
#
# Purpose:     This module is used to create the control panel to connect to the 
#              Raspberry PI generator control by UDP
#
# Author:      Yuancheng Liu
#
# Created:     2019/01/10
# Copyright:   YC @ Singtel Cyber Security Research & Development Laboratory
# License:     YC
#-----------------------------------------------------------------------------
import os, sys
import time
import json
import wx
import wx.gizmos as gizmos
import udpCom
import pwrGenGobal as gv
import pwrGenPanel as pl
import pwrGenMgr as gm

PERIODIC = 100      # update in every 500ms
UDP_PORT = 5005
RSP_IP = '127.0.0.1'

#-----------------------------------------------------------------------------
#-----------------------------------------------------------------------------
class AppFrame(wx.Frame):
    """ URL/IP gps position finder main UI frame."""
    def __init__(self, parent, id, title):
        """ Init the UI and parameters """
        wx.Frame.__init__(self, parent, id, title, size=(800, 340))
        self.SetBackgroundColour(wx.Colour(200, 210, 200))
        self.SetIcon(wx.Icon(gv.ICO_PATH))
        # build the UI.
        self.SetSizer(self._buildUISizer())

        self.connector = udpCom.udpClient((RSP_IP, UDP_PORT))
        

        # Set the periodic call back
        self.lastPeriodicTime = time.time()
        self.timer = wx.Timer(self)
        self.updateLock = False
        self.Bind(wx.EVT_TIMER, self.periodic)
        self.timer.Start(PERIODIC)  # every 500 ms
        self.statusbar = self.CreateStatusBar()
        

        self.connectRsp('Login')

        self.connectRsp('Load')

        self.connectRsp('Gen')

        #self.statusbar.SetStatusText('COM Msg to Arduino: %s ' % str(self.parmList))
        self.Bind(wx.EVT_CLOSE, self.onClose)

        self.Refresh(False)
        print("Program init finished.")

#-----------------------------------------------------------------------------
    def connectRsp(self, evnt, parm=None):
        """ try to connect to the raspberry pi and send cmd based on the 
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
            self.SetLoadsLed(result)
        elif evnt == 'Gen':
            msgStr = json.dumps({'Cmd': 'Get', 'Parm': 'Gen'})
            result = self.connector.sendMsg(msgStr, resp=True)
            self.SetGensLed(result)




#-----------------------------------------------------------------------------
    def setConnLED(self, resultStr):
        """ set and update the LED display in the connection state area
        """
        if resultStr is None:
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

#-----------------------------------------------------------------------------
    def SetLoadsLed(self, resultStr):
        if resultStr is None:
            print("no response")
        else:
            resultDict = json.loads(resultStr)
            self.loadPanel.setLoadIndicator(resultDict)

    def SetGensLed(self, resultStr):
        if resultStr is None:
            print("no response")
            return
        else:
            colorDict = {'green': 'Green', 'amber': 'Yellow', 'red': 'Red',
                         'on': 'Green', 'off': 'Gray', 'slow': 'Yellow', 'fast': 'Red'}
            resultDict = json.loads(resultStr)
            # frequence display
            if 'Freq' in resultDict.keys():
                self.feqLedDis.SetValue(str(resultDict['Freq']))
            # frequence led
            if 'Fled' in resultDict.keys():
                self.feqLedBt.SetBackgroundColour(wx.Colour(colorDict[resultDict['Fled']]))

            if 'Volt' in resultDict.keys():
                self.volLedDis.SetValue(str(resultDict['Volt']))
                
            if 'Vled' in resultDict.keys():
                self.volLedBt.SetBackgroundColour(wx.Colour(colorDict[resultDict['Vled']]))
        
            if 'Mled' in resultDict.keys():
                self.MotoLedBt.SetBackgroundColour(wx.Colour(colorDict[resultDict['Mled']]))

            if 'Pled' in resultDict.keys():
                self.pumpLedBt.SetBackgroundColour(wx.Colour(colorDict[resultDict['Pled']]))

            if 'Smok' in resultDict.keys():
                (lb, cl) = ('Smoke [ON ]', 'Red') if resultDict['Smok']=='on' else ('Smoke [OFF]', 'Gray')
                self.smkIdc.SetLabel(lb)
                self.smkIdc.SetBackgroundColour(wx.Colour(cl))

            if 'Sirn' in resultDict.keys():
                (lb, cl) = ('Siren [ON ]', 'Red') if resultDict['Sirn']=='on' else ('Siren [OFF]', 'Gray')
                self.sirenIdc.SetLabel(lb)
                self.sirenIdc.SetBackgroundColour(wx.Colour(cl))

            if 'Mspd' in resultDict.keys():
                gv.iMotoImgPnl.setMotoSpeed(resultDict['Mspd'])

            if 'Pspd' in resultDict.keys():
                gv.iPumpImgPnl.setPumpSpeed(resultDict['Mspd'])


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
        return uSizer

#-----------------------------------------------------------------------------
    def _buildConnSizer(self):
        """ build the components connection information display panel
        """

        sizer = wx.GridSizer(1, 6, 5, 5)
        sizer.Add(wx.StaticText(self, -1, 'Connection State : '), flag=wx.RIGHT | wx.ALIGN_CENTER_VERTICAL)
        # raspberry PI connection.
        self.rspLedBt = wx.Button(self, label='RsPI', size=(75, 30))
        self.rspLedBt.SetBackgroundColour(wx.Colour('Green'))
        sizer.Add(self.rspLedBt)
        # serial port connection led state.
        self.serialLedBt = wx.Button(self, label='COMM', size=(75, 30))
        self.serialLedBt.SetBackgroundColour(wx.Colour('GRAY'))
        sizer.Add(self.serialLedBt)
        # PLC 1
        self.plc1LedBt = wx.Button(self, label='PLC1', size=(75, 30))
        self.plc1LedBt.SetBackgroundColour(wx.Colour('GRAY'))
        sizer.Add(self.plc1LedBt)
        # PLC 2
        self.plc2LedBt = wx.Button(self, label='PLC1', size=(75, 30))
        self.plc2LedBt.SetBackgroundColour(wx.Colour('GRAY'))
        sizer.Add(self.plc2LedBt)
        # PLC 3
        self.plc3LedBt = wx.Button(self, label='PLC1', size=(75, 30))
        self.plc3LedBt.SetBackgroundColour(wx.Colour('GRAY'))
        sizer.Add(self.plc3LedBt)

        return sizer

#--AppFrame---------------------------------------------------------------------
    def _buildUISizer(self):
        """ Build the main UI Sizer. """
        flagsR = wx.RIGHT | wx.ALIGN_CENTER_VERTICAL
        sizerAll = wx.BoxSizer(wx.VERTICAL)
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
        genSizer.Add(wx.StaticText(self, -1, 'Generator Information:'), flag=flagsR, border=2)
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
        vbox = wx.BoxSizer(wx.VERTICAL)
        self.pumpLedBt = wx.Button(self, label='Pump', size=(80, 30))
        self.pumpLedBt.SetBackgroundColour(wx.Colour('GRAY'))
        vbox.Add(self.pumpLedBt, flag=wx.ALIGN_CENTER_HORIZONTAL, border=2)
        vbox.AddSpacer(10)
        vbox.Add(wx.StaticText(self, label="PumpSpeed"), flag=wx.ALIGN_CENTER_HORIZONTAL, border=2)
        vbox.AddSpacer(10)
        self.pumpSPCB = wx.ComboBox(self, -1, choices=['off', 'low', 'high'], size=(80, 30))
        self.pumpSPCB.SetSelection(0)
        self.pumpSPCB.Bind(wx.EVT_COMBOBOX, self.onPumpSpdChange)
        vbox.Add(self.pumpSPCB, flag=wx.ALIGN_CENTER_HORIZONTAL, border=2)
        mSizer.Add(vbox, flag=wx.ALIGN_CENTER_HORIZONTAL, border=2)
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
        
        sizerAll.AddSpacer(5)
        sizerAll.Add(wx.StaticLine(self, wx.ID_ANY, size=(800, -1),
                    style=wx.LI_HORIZONTAL), flag=flagsR, border=2)
        sizerAll.AddSpacer(5)


        return sizerAll

#-----------------------------------------------------------------------------
    def onCheck(self, evnt):
        cb = evnt.GetEventObject()
        idx = int(cb.GetLabel().split('[')[-1][0])
        val = 1 if cb.GetValue() else 0
        gv.iGnMgr.setLoad([idx],[val])


#--AppFrame---------------------------------------------------------------------
    def periodic(self, event):
        """ Call back every periodic time."""
        now = time.time()
        return
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
        #gv.iGnMgr.stop()
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
