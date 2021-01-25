#!/usr/bin/python
#-----------------------------------------------------------------------------
# Name:        tcpComTest.py
#
# Purpose:     This module will provide a muti-thread test case program to test 
#              the TCP communication modules by using port 5005.
#
# Author:      Yuancheng Liu
#
# Created:     2019/01/15
# Copyright:   
# License:     
#-----------------------------------------------------------------------------

import time
import threading    # create multi-thread test case.
import tcpCom

TCP_PORT = 5005
#-----------------------------------------------------------------------------
#-----------------------------------------------------------------------------
class testThread(threading.Thread):
    """ Thread to test the TCP server/insert the tcp server in other program.""" 
    def __init__(self, parent, threadID, name):
        threading.Thread.__init__(self)
        self.threadName = name
        self.server = tcpCom.tcpServer(None, TCP_PORT, connectNum=1)

    def msgHandler(self, msg):
        """ The test handler method passed into the TCP server to handle the 
            incoming messages.
        """
        print("Incoming message: %s" %str(msg))
        return msg

    def run(self):
        """ Start the tcp server's main message handling loop."""
        print("Server thread run() start.")
        self.server.serverStart(handler=self.msgHandler)
        print("Server thread run() end.")
        self.threadName = None # set the thread name to None when finished.

    def stop(self):
        """ Stop the tcp server. Create a endclient to bypass the rev() block."""
        self.server.serverStop()
        endClient =tcpCom.tcpClient(('127.0.0.1', TCP_PORT))
        endClient.disconnect()
        endClient = None

#-----------------------------------------------------------------------------
#-----------------------------------------------------------------------------
def testCase(mode):
    print("Start TCP client-server test. test mode: %s \n" % str(mode))
    tCount, tPass = 0, True  # test fail count and test pass flag.
    if mode == 1:
        print("Start the TCP Server.")
        servThread = testThread(None, 0, "server thread")
        servThread.start()
        print("Start the TCP Client.")
        client = tcpCom.tcpClient(('127.0.0.1', TCP_PORT))
        # test case 0
        print("0. HearBeat message test:\n----")
        tPass = True
        for i in range(3):
            msg = "Test data %s" % str(i)
            result = client.sendMsg(msg, resp=True)
            tPass = tPass and (msg.encode('utf-8') == result)
        if tPass: tCount += 1
        print("Test passed: %s \n----\n" % str(tPass))
        # test case 1
        print("1. Client reconnection test:\n----")
        tPass = True
        client.connect()
        msg = 'Re-connected'.encode('utf-8')
        result = client.sendMsg(msg, resp=True)
        tPass = (msg == result)
        if tPass: tCount += 1
        print("Test passed: %s \n----\n" % str(tPass))
        #  test case 2
        print("2. Client disconnect test:\n----")
        tPass = True
        client.disconnect()
        try:
            client.sendMsg('Testdata', resp=True)
            tPass = False
        except:
            tPass = True
        if tPass: tCount += 1
        print("Test passed: %s \n----\n" % str(tPass))
        # test case 3
        print("3. Server stop test:\n----")
        servThread.stop()
        time.sleep(1)  # wait 1 second for all the sorcket close.
        tPass = (servThread.threadName is None)
        if tPass: tCount += 1
        print("Test passed: %s \n----\n" % str(tPass))

        print(" => All test finished: %s/4" % str(tCount))
        client = servThread = None

    else:
        print("Add more other exception test here.")

#-----------------------------------------------------------------------------
if __name__ == '__main__':
    testCase(1) # 1 - normal test mode.




