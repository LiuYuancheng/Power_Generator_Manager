#!/usr/bin/python
#-----------------------------------------------------------------------------
# Name:        serialCom.py
#
# Purpose:     This module will inheritance the python built-in serial module 
#              with automatically serial port serach and connection function.
#
# Author:      Yuancheng Liu
#
# Created:     2019/04/01
# Copyright:   
# License:     
#-----------------------------------------------------------------------------

import os
import sys
import glob
from serial import Serial, SerialException

BYTE_SIZE = 8
PARITY = 'N'
STOP_BIT = 1
TIME_OUT = 1

#-----------------------------------------------------------------------------
#-----------------------------------------------------------------------------
class serialCom(Serial):
    """ The serialCom inheritance from python built-in serial.Serial class. Call 
        read(int *) or write(bytes *) to read number of bytes from the serial
        port or send bytes to the port. Call close() to close the port.
    """
    def __init__(self, parent, serialPort=None, baudRate=9600):
        """ Init the serial comunication and if serialPort is None the program 
            will automatically find the port which can connected. For windows we 
            use the last port(idx=-1) in the list and in linux we use first port(idx=0)  
        """
        # Automatically find the serial port which can read and write.
        if serialPort is None:
            conIdx = 0  # port index used for connection.
            if sys.platform.startswith('win'):
                ports = ['COM%s' % (i + 1) for i in range(256)]
                conIdx = -1
            elif sys.platform.startswith('linux') or sys.platform.startswith('cygwin'):
                # this excludes your current terminal "/dev/tty"
                ports = glob.glob('/dev/tty[A-Za-z]*')
            elif sys.platform.startswith('darwin'):
                ports = glob.glob('/dev/tty.*')
            else:
                raise EnvironmentError('serialCom: Serial Port comm connection error: Unsupported platform.')
            portList = []   # port list can be used for connection.
            for port in ports:
                # Check whether the ports can be open.
                try:
                    s = Serial(port)
                    s.close()
                    portList.append(port)
                except (OSError, SerialException):
                    pass
            print(('serialCom: the serial ports can be used : %s' % str(portList)))
            serialPort = portList[conIdx]
        # Call the parent __init__() to connect to the port.
        try:
            super().__init__(serialPort, baudRate, BYTE_SIZE, PARITY, STOP_BIT, timeout=TIME_OUT)
        except:
            print("serialCom: serial port open error.")

#-----------------------------------------------------------------------------
#-----------------------------------------------------------------------------
def testCase(testMode):

    print("Start serial port communication test. Test mode %s \n" %str(testMode))
    if testMode == 1:
        print("Test Case 1: test connect to the un-readable port.")
        connector = serialCom(None,serialPort="COM_NOT_EXIST", baudRate=115200)

    print("Test Case 2: test connect to com port.")
    connector = serialCom(None, baudRate=115200)
    connector.write('Test String'.encode('utf-8'))
    msg = connector.read(128)
    print("Read message from the com: %s" %str(msg))

#-----------------------------------------------------------------------------
if __name__ == '__main__':
    testCase(1)
