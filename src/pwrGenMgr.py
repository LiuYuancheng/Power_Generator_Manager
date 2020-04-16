#!/usr/bin/python
#-----------------------------------------------------------------------------
# Name:        pwrGenMgr.py
#
# Purpose:     Power generator auto-control manager.
#              GUI -> UDP -> controler-> ModeBus TCP-> PLC               
#                               +-> Serial Comm-> Power station Arduino
# Author:       Yuancheng Liu
#
# Created:     2020/02/17
# Copyright:   YC @ Singtel Cyber Security Research & Development Laboratory
# License:     YC
#--------------------------------------------------------------------------

import time
import json
import re

import udpCom
import serialCom
import M2PLC221 as m221
import S7PLC1200 as s71200

UDP_PORT = 5005
TEST_MODE = True    # Local test mode flag.
PLC1_IP = '192.168.10.72'
PLC2_IP = '192.168.10.73'
PLC3_IP = '192.168.10.71'

#--------------------------------------------------------------------------
#--------------------------------------------------------------------------
class pwrGenClient(object):
    """ Client program running on Raspberry PI or nomral computer to connect
        to PLC and Arduino. A UDP echo server will also be inited to response
        the UI control's request. 
    """
    def __init__(self, parent, debug=False):
        # Set the load number.
        self.parent = parent
        self.loadNum = 0
        self.debug = debug  # debug mode flag.
        # try to connect to the arduino by serial port.
        self.serialComm = serialCom.serialCom(None, baudRate=115200)
        # try to connect to the PLCs.
        self.plc1 = m221.M221(PLC1_IP)
        self.plc2 = s71200.S7PLC1200(PLC2_IP)
        self.plc3 = m221.M221(PLC3_IP)
        # Init the UDP server.
        self.server = udpCom.udpServer(None, UDP_PORT)
        # Init the state manager.
        self.stateMgr = stateManager()
        print('Init finished [Test mode:%s], connection state :\n' %str(TEST_MODE))
        print('Arduino connection : %s' %str(self.serialComm.connected))
        print('PLC 1 [%s] connection: %s' %(PLC1_IP, self.plc1.connected))
        print('PLC 2 [%s] connection: %s' %(PLC2_IP, self.plc2.connected))
        print('PLC 3 [%s] connection: %s' %(PLC3_IP, self.plc3.connected))

#--------------------------------------------------------------------------
    def mainLoop(self):
        """ Controler request handling loop.
        """
        print("UDP echo-server main loop start")
        self.server.serverStart(handler=self.msgHandler)
        print("UDP echo-server main loop end")

#--------------------------------------------------------------------------
    def msgHandler(self, msg):
        """ Generator request message handler function.
            incomming message sample:
            msg = { 'Cmd': str(***),
                    'Parm': {}}
        """
        if self.debug: print("Incomming message: %s" %str(msg))
        respStr = json.dumps({'Cmd': 'Set', 'Param': 'Done'}) # response string.
        msgDict = json.loads(msg.decode('utf-8'))
        if msgDict['Cmd'] == 'Get':
            # state get request.
            if msgDict['Parm'] == 'Con':
                # connection state fetch request.
                fbDict = {'Serial': self.serialComm.connected,
                          'Plc1': self.plc1.connected,
                          'Plc2': self.plc2.connected,
                          'Plc3': self.plc3.connected
                          }
                respStr = json.dumps(fbDict)
            elif msgDict['Parm'] == 'Gen':
                # Generator's Ardurino controller state.
                respStr = self.stateMgr.getGenInfo()
            elif msgDict['Parm'] == 'Load':
                if not TEST_MODE: self.getLoadState()
                respStr = self.stateMgr.getLoadInfo()
            else:
                print('msgHandler : can not handle the un-expect cmd: %s' %str(msgDict['Parm']))
        elif msgDict['Cmd'] == 'SetGen':
            # Generator set request.
            msgStr = self.stateMgr.updateGenSerState(msgDict['Parm'])
            # Send the control cmd to COMM if not under test mode.
            if self.serialComm.connected and (not TEST_MODE):
                if self.debug: print('Write message <%s> to Ardurino' %msgStr)
                self.serialComm.write(msgStr.encode('utf-8'))
            respStr = self.stateMgr.getGenInfo()
        elif msgDict['Cmd'] == 'SetPLC':
            # PLC  set request.
            # Main power
            if 'Mpwr' in msgDict['Parm'].keys():
                self.setMainPwr(msgDict['Parm']['Mpwr'])
            # TrackA and B all sensor power
            if 'Spwr' in msgDict['Parm'].keys():
                self.setSensorPwr(msgDict['Parm']['Spwr'])
            # Pump speed.
            if 'Pspd' in msgDict['Parm'].keys():
                self.setPumpSpeed(msgDict['Parm']['Pspd'])
            # Moto speed.
            if 'Mspd' in msgDict['Parm'].keys():
                self.setMotoSpeed(msgDict['Parm']['Pspd'])
            # Updaste the state manager
            self.stateMgr.updateGenPlcState(msgDict['Parm'])
            respStr = self.stateMgr.getGenInfo()
        # Send back the response string.
        return respStr

#--------------------------------------------------------------------------
    def getLoadState(self):
        """" Connect to PLC to get the current load state. <m221_plc_modbus.txt>"""
        loadDict = {'Indu': 0,      # Industry area
                    'Airp': 0,      # Air port
                    'Resi': 0,      # Residential area
                    'Stat': 0,      # Stataion power
                    'TrkA': 0,      # Track A power
                    'TrkB': 0,      # Track B power
                    'City': 0,      # City power
                    }
        # get the PLC 1 state:
        s1resp = re.findall('..', str(self.plc1.readMem())[-16:])
        loadDict['Indu'] = 1 if s1resp[7] == '00' else 0
        loadDict['Airp'] = 1 if s1resp[2] == '04' else 0
        # get PLC 2 state:
        loadDict['Resi'] = 1 if self.plc2.getMem('qx0.2', True) else 0
        loadDict['Stat'] = 1 if self.plc2.getMem('qx0.0', True) else 0
        # get PLC 3 state
        s3resp = re.findall('..', str(self.plc3.readMem())[-16:])
        loadDict['TrkA'] = 1 if s3resp[2] == '04' else 0
        loadDict['TrkB'] = 1 if s3resp[3] == '10' else 0
        loadDict['City'] = 1 if s3resp[8] == '00' else 0
        self.stateMgr.updateLoadPlcState(loadDict)       

#--------------------------------------------------------------------------
    def setMainPwr(self, val):
        """ Set the system main power PLC3[M6]. 0-off, 1-on."""
        if not self.plc3.connected:
            if self.debug: print('PLC3 not connected, can not set system main power.')
            return
        parm = 1 if val == 'on' else 0
        self.plc3.writeMem('M6', parm)

#--------------------------------------------------------------------------
    def setMotoSpeed(self, val):
        """ Set generator pump speed plc2 [Q3, Q3]. FF-off, FT-low, TF-high."""
        # change the plc state to do the action.
        if not self.plc2.connected:
            if self.debug: print('PLC2 not connected, can not set Moto speed.')
            return
        mSpeedDict = {'off': (False, False), 'low': (False, True), 'high': (True, False)}
        self.plc2.writeMem('qx0.3', mSpeedDict[val][0])
        time.sleep(0.01) # need we sleep a shot while for plc to response?
        self.plc2.writeMem('qx0.4', mSpeedDict[val][1])

#--------------------------------------------------------------------------
    def setPumpSpeed(self, val):
        """ Set generator pump speed plc1 [M4, M5]. 00-off, 01-low, 10-high."""
        if not self.plc1.connected:
            if self.debug: print('PLC1 not connected, can not set pump speed.')
            return
        # change the plc state to do the action.
        pSpeedDict = {'off': (0, 0), 'low': (0, 1), 'high': (1, 0)}
        self.plc1.writeMem('M4', pSpeedDict[val][0])
        time.sleep(0.01) # need we sleep a shot while for plc to response?
        self.plc1.writeMem('M5', pSpeedDict[val][1])

#--------------------------------------------------------------------------
    def setSensorPwr(self, val):
        """ Set all track sensor's power PLC3 [M4, M5]. 00-off, 11-on."""
        if not self.plc3.connected:
            if self.debug: print('PLC3 not connected, can not set all sensor power.')
            return
        parm = 1 if val == 'on' else 0
        self.plc3.writeMem('M4', parm)
        self.plc3.writeMem('M5', parm)

#--------------------------------------------------------------------------
#--------------------------------------------------------------------------
class stateManager(object):
    """ Manager module to save the current system state.""" 
    def __init__(self):
        # Serial cmd str sequence.
        self.serialSqu = ('Freq', 'Volt', 'Fled', 'Vled', 'Mled', 'Pled', 'Smok', 'Sirn')
        # Generator state dictionary.
        self.genDict = {    'Freq': '00.00',    # frequence (dd.dd)
                            'Volt': '00.00',    # voltage (dd.dd)
                            'Fled': 'green',    # frequence led (green/amber/off)
                            'Vled': 'green',    # voltage led (green/amber/off)
                            'Mled': 'green',    # motor led (green/amber/off)
                            'Pled': 'green',    # pump led (green/amber/off)
                            'Smok': 'off',      # smoke indicator (fast/slow/off)
                            'Pspd': 'off',      # pump speed (high/low/off)
                            'Mspd': 'off',      # moto speed (high/low/off)
                            'Sirn': 'off',      # siren (on/off)
                            'Spwr': 'off',      # sensor power (on/off)
                            'Mpwr': 'on'        # main power (on/off)
                        }
        # Power load state dictionary. 
        self.loadDict = {   'Indu': 0,      # Industry area
                            'Airp': 1,      # Air port
                            'Resi': 0,      # Residential area
                            'Stat': 1,      # Stataion power
                            'TrkA': 0,      # Track A power
                            'TrkB': 1,      # Track B power
                            'City': 0,      # City power
                         }

#--------------------------------------------------------------------------
    def getGenInfo(self):
        """ Return the generator state json string."""
        return json.dumps(self.genDict)

#--------------------------------------------------------------------------
    def getLoadInfo(self):
        """ Return the power load state json string."""
        return json.dumps(self.loadDict)

#--------------------------------------------------------------------------
    def getLoadNum(self):
        """ Return the number of loads """
        return sum(self.loadDict.value())

#--------------------------------------------------------------------------
    def updateGenSerState(self, changeDict):
        """ Passed in the changeDict and the function will return the Ardurino
            control string.
        """
        # first time init setting.
        if changeDict is None:
            return ':'.join([self.genDict[keyStr] for keyStr in self.serialSqu])
        valList = []
        for keyStr in self.serialSqu:
            if keyStr in changeDict.keys():
                self.genDict[keyStr] = changeDict[keyStr]
                valList.append(self.genDict[keyStr])
            else:
                valList.append('-') # append the ingore char if the value not change.
        return ':'.join(valList)

#--------------------------------------------------------------------------
    def updateGenPlcState(self, changeDict):
        """ Update the generator PLC state."""
        for keyStr in changeDict.keys():
            self.genDict[keyStr] = changeDict[keyStr]

#--------------------------------------------------------------------------
    def updateLoadPlcState(self, changeDict):
        """ Update the load PLc state. """
        for keyStr in changeDict.keys():
            self.loadDict[keyStr] = changeDict[keyStr]
#--------------------------------------------------------------------------
#--------------------------------------------------------------------------

def testCase():
    client = pwrGenClient(None, debug=True)
    client.mainLoop()

#-----------------------------------------------------------------------------
if __name__ == '__main__':
    testCase()
