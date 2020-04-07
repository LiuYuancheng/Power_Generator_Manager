#!/usr/bin/python
#-----------------------------------------------------------------------------
# Name:        pwrGenMgr.py
#
# Purpose:     power generator auto-control manager. 
#              GUI -> UDP -> controler-> ModeBus TCP-> PLC               
#                               +-> Serial Comm-> Power station Arduino
# Author:       Yuancheng Liu
#
# Created:     2020/02/17
# Copyright:   YC @ Singtel Cyber Security Research & Development Laboratory
# License:     YC
#--------------------------------------------------------------------------
import os, sys
import time
import glob
import json
import re
import serial
import threading

import udpCom
import serialCom
import M2PLC221 as m221
import S7PLC1200 as s71200

PERIOD = 1  # update frequency
UDP_PORT = 5005
TEST_MODE = True
PLC1_IP = '192.168.10.72'
PLC2_IP = '192.168.10.73'
PLC3_IP = '192.168.10.73'

#--------------------------------------------------------------------------
#--------------------------------------------------------------------------
class pwrGenClient(object):
    """ Client program running on Raspberry PI or nomral computer to connect
        to PLC and Arduino.
    """
    def __init__(self, parent):
        # try to connect to the arduino by serial port.      
        self.serialComm = serialCom.serialCom(None, baudRate=115200)
        print("Arduino connection : %s" %str(self.serialComm.connected))
        # try to connect to the PLCs.
        try:
            self.pcl1 = m221.M221(PLC1_IP)
        except:
            self.pcl1 = None
        finally:
            result = 'connected' if self.pcl1 else 'not response'
            print('PLC 1 [%s] : %s' %(PLC1_IP, result))

        try:
            self.pcl2 = s71200.S7PLC1200(PLC2_IP)
        except:
            self.pcl2 = None
        finally:
            result = 'connected' if self.pcl2 else 'not response'
            print('PLC 2 [%s] : %s' %(PLC1_IP, result))

        try:
            self.pcl3 = m221.M221(PLC3_IP)
        except:
            self.pcl3 = None
        finally:
            result = 'connected' if self.pcl3 else 'not response'
            print('PLC 3 [%s] : %s' %(PLC1_IP, result))
        
        # Set the load number.
        self.loadNum = 0 
        # Init the UDP server.
        self.server = udpCom.udpServer(None, UDP_PORT)
        # Init the state manager.
        self.stateMgr = stateManager()


#--------------------------------------------------------------------------
    def mainLoop(self):
        self.server.serverStart(handler=self.msgHandler)

#--------------------------------------------------------------------------
    def msgHandler(self, msg):
        """ The test handler method passed into the UDP server to handle the 
            incoming messages.
        """
        print("Incomming message: %s" %str(msg))
        msg = msg.decode('utf-8')
        if msg == 'Get':
            pass
        else:
            pumpSp = int(msg.split(';')[-1])
            print("set speed %s" %str(pumpSp))
            #self.setPumpSpeed(pumpSp)

        self.loadNum = self.getLoadNum()
        if 0 < self.loadNum <= 5 :
            self.setMotoSpeed(2)
        elif self.loadNum == 0 :
            self.setMotoSpeed(0)
        else:
            self.setMotoSpeed(1)
        strList = self.serialComm.autoSet(self.loadNum)
        
        msg = ';'.join([strList[0], strList[1], strList[6], strList[7], str(self.loadNum)])
        return msg

#--------------------------------------------------------------------------
    def setPumpSpeed(self, val):
        if TEST_MODE: return
        # update the state manager
        self.stateMgr.updateGenPlcState({'Pspd':val})
        # change the plc state to do the action.
        pSpeedDict = {'off': (0, 0), 'slow': (0, 1), 'fast': (1, 0)}
        self.pcl1.writeMem('M4', pSpeedDict[val][0])
        time.sleep(0.01) # need we sleep a shot while for plc to response?
        self.pcl1.writeMem('M5', pSpeedDict[val][1])

#--------------------------------------------------------------------------
    def setMotoSpeed(self, val):
        if TEST_MODE: return
        # update the state manager
        self.stateMgr.updateGenPlcState({'Mspd':val})
        # change the plc state to do the action.
        mSpeedDict = {'off': (False, False), 'slow': (False, True), 'fast': (True, False)}
        self.pcl2.writeMem('qx0.3', mSpeedDict[0])
        time.sleep(0.01) # need we sleep a shot while for plc to response?
        self.pcl2.writeMem('qx0.4', mSpeedDict[1])

#--------------------------------------------------------------------------
    def getLoadState(self):
        """"Connect to PLC to get the current load state."""
        loadDict = {'Indu': 0,      # Industry area
                    'Airp': 0,      # Air port
                    'Resi': 0,      # Residential area
                    'Stat': 0,      # Stataion power
                    'TrkA': 0,      # Track A power
                    'TrkB': 0,      # Track B power
                    'City': 0,      # City power
                }

        # get the PLC 1 state:
        s1resp = re.findall('..', str(self.pcl1.redMem())[-16:])
        loadDict['Indu'] = 1 if s1resp[7] == '00' else 0
        loadDict['Airp'] = 1 if s1resp[2] == '04' else 0

        # get PLC 2 state:
        loadDict['Resi'] = 1 if self.pcl2.getMem('qx0.2', True) else 0
        loadDict['Stat'] = 1 if self.pcl2.getMem('qx0.0', True) else 0

        # get PLC 3 state
        s3resp = re.findall('..', str(self.pcl3.redMem())[-16:])
        loadDict['TrkA'] = 1 if s3resp[2] == '04' else 0
        loadDict['TrkB'] = 1 if s3resp[3] == '10' else 0
        loadDict['City'] = 1 if s3resp[8] == '00' else 0
        self.stateMgr.updateLoadPlcState(loadDict)            

#--------------------------------------------------------------------------

#--------------------------------------------------------------------------
class ArduinoCOMM(object):
    def __init__(self, parent):
        """ Init the arduino communication."""
        # sequence "Frequency:Voltage:Frequency LED:Voltage LED:Motor LED:Pump LED:Smoke:Siren "
        self.msgDict = {
            '0' : ['52.00', '11.00', 'red', 'green', 'green', 'green', 'off', 'on'], 
            '1' : ['51.20', '11.00', 'amber', 'green', 'green', 'green', 'fast', 'on'], 
            '2' : ['50.80', '11.00', 'amber', 'green', 'green', 'green', 'fast', 'off'], 
            '3' : ['50.40', '11.00', 'green', 'green', 'green', 'green', 'fast', 'off'], 
            '4' : ['50.00', '11.00', 'green', 'green', 'green', 'green', 'fast', 'off'], 
            '5' : ['49.80', '11.00', 'green', 'green', 'green', 'green', 'fast', 'off'], 
            '6' : ['49.40', '11.00', 'amber', 'green', 'amber', 'amber', 'slow', 'on'], 
            '7' : ['48.20', '11.00', 'red', 'green', 'amber', 'amber', 'slow', 'on'], 
        }
        
        self.serComm = None
        if TEST_MODE: return
        portList = []
        if sys.platform.startswith('win'):
            ports = ['COM%s' % (i + 1) for i in range(256)]
        elif sys.platform.startswith('linux') or sys.platform.startswith('cygwin'):
            # this excludes your current terminal "/dev/tty"
            ports = glob.glob('/dev/tty[A-Za-z]*')
        elif sys.platform.startswith('darwin'):
            ports = glob.glob('/dev/tty.*')
        else:
            raise EnvironmentError('Serial Port comm connection error: Unsupported platform.')
        for port in ports:
            # Check whether the port can be open.
            try:
                s = serial.Serial(port)
                s.close()
                portList.append(port)
            except (OSError, serial.SerialException):
                pass
        print(('COM connection: the serial port can be used :%s' % str(portList)))
        self.serialPort = portList[0]
        try:
            self.serComm = serial.Serial(self.serialPort, 115200, 8, 'N', 1, timeout=1)
        except:
            print("Serial connection: serial port open error.")
            return None

    def autoSet(self, loadNum):
        if 0 <= loadNum < 8 :
            strList = self.msgDict[str(loadNum)]
            msgStr = ':'.join(strList)
            if self.serComm and not TEST_MODE:
                print('Send message [%s] to cmd ' %msgStr)
                self.serComm.write(msgStr.encode('utf-8'))
            return strList

#--------------------------------------------------------------------------
#--------------------------------------------------------------------------
class stateManager(object):
    """ save the current system state.""" 
    def __init__(self):
        # Serial cmd str sequence. 
        self.serialSqu = ('Freq', 'Volt', 'Fled', 'Vled', 'Mled', 'Pled', 'Smok', 'Sirn')
        self.genDict = {    'Freq': '0.00',     # frequence (dd.dd)
                            'Volt': '0.00',     # voltage (dd.dd)
                            'Fled': 'green',    # frequence led (green/amber/off)
                            'Vled': 'green',    # voltage led (green/amber/off)
                            'Mled': 'green',    # motor led (green/amber/off)
                            'Pled': 'green',    # pump led (green/amber/off)
                            'Smok': 'off',      # smoke indicator (fast/slow/off)
                            'Pspd': 'off',      # pump speed (fast/slow/off)
                            'Mspd': 'off',      # moto speed (fast/slow/off)
                            'Sirn': 'off',      # siren (on/off)
                            'Spwr': 'off',      # sensor power (on/off)
                            'Mpwr': 'on'        # main power (on/off)
                        }

        self.loadDict = {   'Indu': 0,      # Industry area
                            'Airp': 0,      # Air port
                            'Resi': 0,      # Residential area
                            'Stat': 0,      # Stataion power
                            'TrkA': 0,      # Track A power
                            'TrkB': 0,      # Track B power
                            'City': 0,      # City power
                         }

#--------------------------------------------------------------------------
    def getGenInfo(self):
        return json.dumps(self.genDict)

#--------------------------------------------------------------------------
    def getLoadInfo(self):
        return json.dumps(self.loadDict)

#--------------------------------------------------------------------------
    def getLoadNum(self):
        """return the number of loads"""
        return sum(self.loadDict.value())

#--------------------------------------------------------------------------
    def updateGenSerState(self, changeDict):
        """ passed in the changeDict and the function will return a 
        """
        # first time inti setting.
        if changeDict is None:
            return ':'.join([self.genDict[keyStr] for keyStr in self.serialSqu])
        valList = []
        for keyStr in self.serialSqu:
            if keyStr in changeDict.keys():
                self.genDict[keyStr] = changeDict[changeDict]
                valList.append(self.genDict[keyStr])
            else:
                valList.append('-') # append the ingore char if the value not change.
        return ':'.join(valList)

#--------------------------------------------------------------------------
    def updateGenPlcState(self, changeDict):
        for keyStr in changeDict:
            self.genDict[keyStr] = changeDict[changeDict]

#--------------------------------------------------------------------------
    def updateLoadPlcState(self, changeDict):
        for keyStr in changeDict:
            self.loadDict[keyStr] = changeDict[keyStr]
#--------------------------------------------------------------------------
#--------------------------------------------------------------------------

def testCase():
    client = pwrGenClient(None)
    client.mainLoop()

#-----------------------------------------------------------------------------
if __name__ == '__main__':
    testCase()
