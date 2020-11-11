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

import os
import time
import json
import re
import csv
import _thread # python2 thread is changed to '_thread' in python3
import threading    # create multi-thread test case.
from random import randint

import udpCom
import serialCom
import BgCtrl as bg
import M2PLC221 as m221
import S7PLC1200 as s71200

APP_NAME = "pwrGenMgr"
UDP_PORT = 5005
TEST_MODE = False   # Local test mode flag.
TIME_INT = 1        # time interval to fetch the load.
PLC1_IP = '192.168.10.72'
PLC2_IP = '192.168.10.73'
PLC3_IP = '192.168.10.71'
CSV_VAL = 'pwrSubParm.csv'

#--------------------------------------------------------------------------
#--------------------------------------------------------------------------
class pwrGenClient(object):
    """ Client program running on Raspberry PI or nomral computer to connect
        to PLC and Arduino. A UDP echo server will also be inited to response
        the UI control's request. 
    """
    def __init__(self, parent, debug=True):
        # Set the load number.
        self.parent = parent
        self.loadNum = 0
        self.autoCtrl = False   # Gen auto control based on load number.
        self.debug = debug      # debug mode flag.
        self.bgCtrler = bg.BgController(APP_NAME)

        # try to connect to the arduino by serial port.
        self.serialComm = serialCom.serialCom(None, baudRate=115200)
        # try to connect to the PLCs.
        self.plc1 = m221.M221(PLC1_IP)
        self.plc2 = s71200.S7PLC1200(PLC2_IP)
        self.plc3 = m221.M221(PLC3_IP)
        self.reConnectCount = 0 if self.plc1.connected and self.plc2.connected and self.plc3.connected else 10
        # Init the UDP server.
        # self.server = udpCom.udpServer(None, UDP_PORT)
        self.servThread = CommThread(self, 0, "server thread")

        # init the plat form state:
        if self.serialComm and not TEST_MODE:
            msgStr = "50.00:11.00:green:green:green:green:slow:off"
            self.serialComm.write(msgStr.encode('utf-8'))
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
        #self.server.serverStart(handler=self.msgHandler)
        self.servThread.start()
        print("Manager main loop start.")
        while self.bgCtrler.bgRun():
            # Get the 3 PLC load state:
            if not TEST_MODE:
                self.getLoadState()
                if self.reConnectCount > 0:
                    self.reConnectCount -= 1
                    print(">>> reconnect PLC in %s sec" %str(self.reConnectCount))
            if TEST_MODE:
                self.loadNum+=1
                self.autoCtrlGen(self.loadNum%7)
            if self.reConnectCount == 1:
                self.plcReconnect()
            time.sleep(TIME_INT)
        # Stop the program and stop all the connection
        self.servThread.stop()
        self.servThread = None
        if self.serialComm: self.serialComm.close()
        if self.plc1.connected: self.plc1.disconnect()
        if self.plc2.connected: self.plc2.disconnect()
        if self.plc3.connected: self.plc3.disconnect()
        print("Power generator main loop end.")

#--------------------------------------------------------------------------
    def plcReconnect(self):
        """ Try to reconnect the PLC if the plc is not connect at the beginning.
        """
        if self.plc1 is None or (not self.plc1.connected):
            if not self.plc1 is None:
                self.plc1.disconnect()  # disconnect to release the socket.
            print("Try to reconnect to PLC1: %s" %str(PLC1_IP))
            self.plc1 = m221.M221(PLC1_IP)

        if self.plc2 is None or (not self.plc2.connected):
            if not self.plc2 is None:
                self.plc2.disconnect()  # disconnect to release the socket.
            print("Try to reconnect to PLC2: %s" %str(PLC2_IP))
            self.plc2 = s71200.S7PLC1200(PLC2_IP)

        if self.plc3 is None or (not self.plc3.connected):
            if not self.plc3 is None:
                self.plc3.disconnect()  # disconnect to release the socket.
            print("Try to reconnect to PLC3: %s" %str(PLC3_IP))
            self.plc3 = m221.M221(PLC3_IP)

#--------------------------------------------------------------------------
    def msgHandler(self, msg):
        """ Generator request message handler function.
            incomming message sample:
            msg = { 'Cmd': str(***),
                    'Parm': {}}
        """
        if self.debug: print("Incomming message: %s" %str(msg))
        if msg == b'' or msg == b'end' or msg == b'logout': return None  # get at program terminate signal.
        if msg.decode('utf-8') == 'A;1':
            _thread.start_new_thread( self.startAttack, ("Thread-1", ) )
            return None
        respStr = json.dumps({'Cmd': 'Set', 'Param': 'Done'}) # response string.
        msgDict = json.loads(msg.decode('utf-8'))
        if msgDict['Cmd'] == 'Get':
            # state get request.
            if msgDict['Parm'] == 'Con':
                # connection state fetch request.
                fbDict = {'Serial': self.serialComm.connected,
                          'Plc1': (not self.plc1 is None) and self.plc1.connected,
                          'Plc2': (not self.plc2 is None) and self.plc2.connected,
                          'Plc3': (not self.plc2 is None) and self.plc3.connected
                          }
                respStr = json.dumps(fbDict)
            elif msgDict['Parm'] == 'Gen':
                # Generator's Ardurino controller state.
                respStr = self.stateMgr.getGenInfo()
            elif msgDict['Parm'] == 'Load':
                
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
        
        elif msgDict['Cmd'] == 'SetALC':
            # set auto load control
            self.autoCtrl = msgDict['Parm']
            self.stateMgr.updateGenPlcState(msgDict['Parm'])
        elif msgDict['Cmd'] == 'GetSub':
            # get the Substation memory value;
            respStr = self.stateMgr.getSubInfo()

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
        if self.plc1.connected:
            try:
                s1resp = re.findall('..', str(self.plc1.readMem())[-16:])
                loadDict['Indu'] = 1 if s1resp[7] == '00' else 0
                loadDict['Airp'] = 1 if s1resp[1] == '04' else 0
            except Exception as err: 
                print("PLC1[%s] data read error:\n%s" %(PLC1_IP, err))
                self.plc1.connected = False
        # get PLC 2 state:
        if self.plc2.connected:
            try:
                loadDict['Resi'] = 0 if self.plc2.getMem('qx0.2') else 1
                loadDict['Stat'] = 1 if self.plc2.getMem('qx0.0') else 0
            except Exception as err:
                print("PLC2[%s] data read error:\n%s" %(PLC2_IP, err))
                self.plc2.connected = False
        # get PLC 3 state
        if self.plc3.connected:
            try:
                s3resp = re.findall('..', str(self.plc3.readMem())[-16:])
                loadDict['TrkA'] = 1 if s3resp[1] == '04' else 0
                loadDict['TrkB'] = 1 if s3resp[2] == '10' else 0
                loadDict['City'] = 1 if s3resp[7] == '00' else 0
            except Exception as err:
                print("PLC3[%s] data read error:\n%s" %(PLC3_IP, err))
                self.plc3.connected = False
        
        self.stateMgr.updateLoadPlcState(loadDict)
        self.autoCtrlGen(self.stateMgr.getLoadNum()) # get the load number.

#--------------------------------------------------------------------------
    def autoCtrlGen(self, loadCount):
        """"Auto adjust the gen based on the load number.
        Args:
            loadCount ([int]): [l]
        Returns:
            [type]: [description]
        """
        if (not self.autoCtrl) or (self.loadNum == loadCount):
            return # no change.
        self.loadNum  = loadCount
        freqList= ['52.00', '51.20', '50.80', '50.40', '50.00', '50.00', '50.00', '49.8']
        sirenSt = 'on' if self.loadNum < 2 else 'off'
        color = 'red' if self.loadNum < 5 else 'green'
        if self.loadNum == 7: color = 'amber'
        genDict = {'Freq': freqList[self.loadNum ],
            'Volt': '11.00',
            'Fled': color,
            'Vled': 'green',
            'Mled': 'red',
            'Pled': 'red',
            'Smok': 'fast',
            'Sirn': sirenSt,}
        msgStr = ':'.join((genDict['Freq'], genDict['Volt'], genDict['Fled'], genDict['Vled'],  genDict['Mled'], genDict['Pled'], genDict['Smok'], genDict['Sirn']))
        self.serialComm.write(msgStr.encode('utf-8'))
        self.stateMgr.updateGenSerState(genDict)

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
    def startAttack(self, threadName):
        """ Simulate the attack situation."""
        self.autoCtrl = 0   # Turn off the auto control.
        time.sleep(10)
        self.autoCtrl = False   # turn off the auto control.
        msgStr = "52.00:11.00:amber:amber:amber:amber:off:on"
        self.serialComm.write(msgStr.encode('utf-8'))
        genDict = {'Freq': '52.00',
                   'Volt': '11.00',
                   'Fled': 'amber',
                   'Vled': 'amber',
                   'Mled': 'amber',
                   'Pled': 'amber',
                   'Smok': 'off',
                   'Sirn': 'on',}
        self.stateMgr.updateGenSerState(genDict)
        time.sleep(5)

        msgStr = "50.00:00.00:red:red:red:red:off:off"
        self.serialComm.write(msgStr.encode('utf-8'))
        genDict = {'Freq': '52.00',
                   'Volt': '00.00',
                   'Fled': 'red',
                   'Vled': 'red',
                   'Mled': 'red',
                   'Pled': 'red',
                   'Smok': 'off',
                   'Sirn': 'off',}
        self.stateMgr.updateGenSerState(genDict)
        return None

#--------------------------------------------------------------------------
#--------------------------------------------------------------------------
class stateManager(object):
    """ Manager module to save the current system state.""" 
    def __init__(self):
        # Serial cmd str sequence.
        self.serialSqu = ('Freq', 'Volt', 'Fled', 'Vled', 'Mled', 'Pled', 'Smok', 'Sirn')
        self.subParms = {'Nml':[[] for a in range(4)], 
                        'Atk':[[] for a in range(4)]}        
        self.loadCSVParm(os.path.join(os.path.dirname(__file__), CSV_VAL))
        
        # Generator state dictionary.
        self.genDict = {    'Freq': '50.00',    # frequence (dd.dd)
                            'Volt': '11.00',    # voltage (dd.dd)
                            'Fled': 'green',    # frequence led (green/amber/off)
                            'Vled': 'green',    # voltage led (green/amber/off)
                            'Mled': 'green',    # motor led (green/amber/off)
                            'Pled': 'green',    # pump led (green/amber/off)
                            'Smok': 'off',      # smoke indicator (fast/slow/off)
                            'Pspd': 'off',      # pump speed (high/low/off)
                            'Mspd': 'off',      # moto speed (high/low/off)
                            'Sirn': 'off',      # siren (on/off)
                            'Spwr': 'off',      # sensor power (on/off)
                            'Mpwr': 'on',        # main power (on/off)
                            'Mode': 0           # control mode.
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

        # Substation memory dictrionary.
        self.subMemDict = {
            'ff00': '0',  #
            'ff01': '0',
            'ff02': '0',
            'ff03': '0',
            'ff04': '0',
            'ff05': '0',
            'ff06': '0',
            'ff07': '0',
            'ff08': '0',
            'ff09': '0',
            'ff10': '0',
        }

#--------------------------------------------------------------------------
    def printState(self):
        """ Test function used for debug.(Print all current state.)
        Returns:
            [type]: [description]
        """
        print("self.genDict: \n %s \n" %str(self.genDict))
        print("self.loadDict: \n %s \n" %str(self.loadDict))
        print("self.subMemDict: \n %s \n" %str(self.subMemDict))
        print("self.subParms: \n %s \n" %str(self.subParms))

#--------------------------------------------------------------------------
    def loadCSVParm(self, csvFile):
        """[summary]
        Args:
            csvFile ([type]): [description]
        """
        try:
            with open(csvFile, 'r') as file:
                reader = csv.reader(file)
                rowCnt = 0
                for row in reader: # remove header.
                    if rowCnt == 0:
                        rowCnt +=1
                        continue
                    idx = int(row[1])
                    if int(row[0]) == 0:
                        self.subParms['Nml'][idx].append(row[2:])
                    else:
                        self.subParms['Atk'][idx].append(row[2:])
        except Exception as err:
            print("CSV file IO Error: %s" %str(err))

#--------------------------------------------------------------------------
    def getGenInfo(self):
        """ Return the generator state json string."""
        return json.dumps(self.genDict)

#--------------------------------------------------------------------------
    def getSubInfo(self):
        """ Return the generator state json string."""
        loadNum = 3 if TEST_MODE else sum((self.loadDict['Airp'], self.loadDict['Stat'], self.loadDict['TrkA']))
        valIdx = randint(0,18)
        for i in range(10):
            self.subMemDict["ff{:02d}".format(i)] = self.subParms['Nml'][loadNum][valIdx][i]
            #print(self.subMemDict["ff{:02d}".format(i)])
        return json.dumps(self.subMemDict)

#--------------------------------------------------------------------------
    def getLoadInfo(self):
        """ Return the power load state json string."""
        return json.dumps(self.loadDict)

#--------------------------------------------------------------------------
    def getLoadNum(self):
        """ Return the number of loads """
        return sum(self.loadDict.values())

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

class CommThread(threading.Thread):
    """ Thread to test the UDP server/insert the tcp server in other program.""" 
    def __init__(self, parent, threadID, name):
        threading.Thread.__init__(self)
        self.threadName = name
        self.parent = parent
        self.server = udpCom.udpServer(None, UDP_PORT)

    def run(self):
        """ Start the udp server's main message handling loop."""
        print("Server thread run() start.")
        self.server.serverStart(handler=self.parent.msgHandler)
        print("Server thread run() end.")
        self.threadName = None # set the thread name to None when finished.

    def stop(self):
        """ Stop the udp server. Create a endclient to bypass the revFrom() block."""
        self.server.serverStop()
        endClient = udpCom.udpClient(('127.0.0.1', UDP_PORT))
        endClient.disconnect()
        endClient = None

#-----------------------------------------------------------------------------
#-----------------------------------------------------------------------------
def main(mode=0):
    if mode == 0:
        client = pwrGenClient(None, debug=True)
        client.mainLoop()
    elif mode == 1:
        stateMgr = stateManager()
        stateMgr.printState()

#-----------------------------------------------------------------------------
if __name__ == '__main__':
    main()
