import wx
import time
import json
#from wx.adv import Animation, AnimationCtrl
import wx.gizmos as gizmos
import pwrGenGobal as gv
import udpCom


UDP_PORT = 5005
PERIODIC = 250  # main UI loop call back period.(ms)
TEST_MD = False
RSP_IP = '127.0.0.1' if TEST_MD else '192.168.10.244'


class FancyFrame(wx.Frame):
    def __init__(self, width, height):
        wx.Frame.__init__(self, None,
                          style = wx.STAY_ON_TOP |
                          wx.FRAME_NO_TASKBAR |
                          wx.FRAME_SHAPED,
                          size=(width, height))
        
        main_sizer = wx.BoxSizer(wx.VERTICAL)
        self.panel = MainPanel(self)
        b = wx.Bitmap(width, height)
        dc = wx.MemoryDC()
        dc.SelectObject(b)
        dc.SetBackground(wx.Brush('black'))
        dc.Clear()
        dc.SetBrush(wx.TRANSPARENT_BRUSH)
        dc.SetPen(wx.Pen('green', 50))
        dc.DrawRectangle(0, 0, 200, 200)
        dc.SelectObject(wx.NullBitmap)
        b.SetMaskColour('black')
        self.SetBackgroundColour('red')
        
        main_sizer.Add(self.panel,proportion=1, flag=wx.EXPAND)
        self.SetSizer(main_sizer)
        
        self.SetShape(wx.Region(b))
        self.Centre()
        self.Show(True)

class MainPanel(wx.Panel):
    def __init__(self, frame):
        wx.Panel.__init__(self, frame)
        button_sizer = self._button_sizer(frame)
        main_sizer = wx.BoxSizer(wx.VERTICAL)

        #self.MotoLedBt = wx.Button(self, label='Moto', size=(80, 30))
        main_sizer.Add(button_sizer,proportion=1, flag=wx.EXPAND)
        self.SetSizer(main_sizer)
        self.Fit()

    def _button_sizer(self, frame):
        cmd_save = wx.Button(self, wx.ID_SAVE)
        cmd_cancel = wx.Button(self, wx.ID_CANCEL)
        button_sizer = wx.BoxSizer(wx.HORIZONTAL)
        button_sizer.Add(cmd_save)
        button_sizer.Add((-1, -1), proportion=1)
        button_sizer.Add(cmd_cancel)
        return button_sizer


class pwrGenLDisplay(wx.Frame):
    """ Popup frame to show a transparent window to block the desktop to simulate
        the trojan attack.
    """
    def __init__(self, parent, width, height):
        wx.Frame.__init__(self, parent, title="pwrGenLDisplay",style=wx.MINIMIZE_BOX, size=(width, height))
        self.SetBackgroundColour(wx.Colour('BLACK'))
        # build the UI.
        self.connector = udpCom.udpClient((RSP_IP, UDP_PORT))
        self.lastPeriodicTime = { 'UI':time.time(), 'Data':time.time()}
        self.timer = wx.Timer(self)
        self.updateLock = False
        self.Bind(wx.EVT_TIMER, self.periodic)
        self.timer.Start(PERIODIC)  # every 500 ms
        self.SetSizer(self._buildGenInfoSizer())

        self.connectRsp('Login')
        self.alphaValue = 128
        self.SetTransparent(self.alphaValue)
        self.Layout()
        self.SetPosition((800, 600))
        self.Refresh(False)
        self.Show(True)
        print("----")


    def _buildGenInfoSizer(self):
        """ Build the generator information display panel."""
        # LED area
        uSizer = wx.BoxSizer(wx.HORIZONTAL)
        flagsR = wx.RIGHT
        # Frequence LED
        self.feqLedBt = wx.Button(self, label='Frequency', size=(80, 35))
        self.feqLedBt.SetBackgroundColour(wx.Colour('GRAY'))
        uSizer.Add(self.feqLedBt, flag=flagsR, border=2)
        self.feqLedDis = gizmos.LEDNumberCtrl(
            self, -1, size=(80, 35), style=gizmos.LED_ALIGN_CENTER)
        uSizer.Add(self.feqLedDis, flag=flagsR, border=2)
        uSizer.AddSpacer(10)
        # Voltage LED
        self.volLedBt = wx.Button(self, label='Voltage', size=(80, 35))
        self.volLedBt.SetBackgroundColour(wx.Colour('GRAY'))
        uSizer.Add(self.volLedBt, flag=flagsR, border=2)

        self.volLedDis = gizmos.LEDNumberCtrl(
            self, -1, size=(80, 35), style=gizmos.LED_ALIGN_CENTER)
        uSizer.Add(self.volLedDis, flag=flagsR, border=2)
        uSizer.AddSpacer(10)
        # Smoke LED
        self.smkIdc = wx.Button(
            self, label='Smoke [OFF]', size=(100, 35), name='smoke')
        self.smkIdc.SetBackgroundColour(wx.Colour('GRAY'))
        uSizer.Add(self.smkIdc, flag=flagsR, border=2)
        uSizer.AddSpacer(10)
        # Siren LED
        self.sirenIdc = wx.Button(
            self, label='Siren [OFF]', size=(100, 35), name='smoke')
        self.sirenIdc.SetBackgroundColour(wx.Colour('GRAY'))
        uSizer.Add(self.sirenIdc, flag=flagsR, border=2)
        uSizer.AddSpacer(10)

        return uSizer


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
            #if 'Mled' in resultDict.keys():
            #    self.MotoLedBt.SetBackgroundColour(
            #        wx.Colour(colorDict[resultDict['Mled']]))
            # pump led light.
            #if 'Pled' in resultDict.keys():
            #    self.pumpLedBt.SetBackgroundColour(
            #        wx.Colour(colorDict[resultDict['Pled']]))
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
            self.Refresh(False)


#--AppFrame---------------------------------------------------------------------
    def periodic(self, event):
        """ Call back every periodic time."""
        now = time.time()
        if not self.updateLock:
            if now - self.lastPeriodicTime['Data'] >= 2*gv.gUpdateRate:
                self.lastPeriodicTime['Data'] = now
                self.connectRsp('Gen')

#-----------------------------------------------------------------------------
    def connectRsp(self, evnt, parm=None):
        """ Try to connect to the raspberry pi and send cmd based on the 
            evnt setting.
        """
        if evnt == 'Login':
            # Log in and get the connection state.
            msgStr = json.dumps({'Cmd': 'Get', 'Parm': 'Con'})
            result = self.connector.sendMsg(msgStr, resp=True)
            #self.setConnLED(result)
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
#-----------------------------------------------------------------------------
class TrojanAttFrame(wx.Frame):
    """ Popup frame to show a transparent window to block the desktop to simulate
        the trojan attack.
    """
    def __init__(self, parent):
        wx.Frame.__init__(self, parent, title="TrojanAttFrame",style=wx.MINIMIZE_BOX|wx.STAY_ON_TOP)
        self.SetBackgroundColour(wx.Colour('BLACK'))
        self.alphaValue = 255   # transparent control
        self.alphaIncrement = -4
        self.count = 500        # count to control when to stop the attack.   
        # Build the main UI.
        self.SetSizerAndFit(self.buidUISizer())

        self.changeAlpha_timer = wx.Timer(self)
        self.changeAlpha_timer.Start(100)       # 10 changes per second
        self.Bind(wx.EVT_TIMER, self.changeAlpha)
        self.Bind(wx.EVT_CLOSE, self.onCloseWindow)
        # Set the frame cover full desktop.
        self.Maximize()
        self.ShowFullScreen(True)
        self.Show()

#--TrojanAttFrame--------------------------------------------------------------
    def buidUISizer(self):
        """ Build the UI and the return the wx.sizer. """
        sizer = wx.BoxSizer(wx.VERTICAL)
        #self.ctrl = AnimationCtrl(self, -1, Animation("img\\motor.png"))
        #self.ctrl.Play()
        #sizer.Add(self.ctrl, flag=wx.ALIGN_CENTER_VERTICAL |
        #          wx.CENTER, border=2)
        self.stTxt = wx.StaticText(
            self, -1, "Your computer has been took over by YC's Trojan, we will release control in 10 sec")
        self.stTxt.SetBackgroundColour(wx.Colour('GREEN'))
        self.stTxt.SetFont(wx.Font(30, wx.SWISS, wx.NORMAL, wx.NORMAL))
        sizer.Add(self.stTxt, flag=wx.ALIGN_CENTER, border=2)
        return sizer

 #--TrojanAttFrame--------------------------------------------------------------
    def changeAlpha(self, evt):
        """ The term "alpha" means variable transparency this function we 
            follow the examle in =: 
            https://wiki.wxpython.org/Transparent%20Frames
              as opposed to a "mask" which is binary transparency.
              alpha == 255 :  fully opaque
              alpha ==   0 :  fully transparent (mouse is ineffective!)
            Only top-level controls can be transparent; no other controls can.
            This is because they are implemented by the OS, not wx.
        """
        self.alphaValue += self.alphaIncrement
        if (self.alphaValue) <= 0 or (self.alphaValue >= 255):
            # Reverse the increment direction.
            self.alphaIncrement = -self.alphaIncrement
            if self.alphaValue <= 0:
                self.alphaValue = 0
            if self.alphaValue > 255:
                self.alphaValue = 255
        # Show the release time text.
        self.count -=1
        if self.count%100 == 0:
            self.stTxt.SetLabel("Your computer has been took over by the Trojan, we will release control in "+str(self.count//100).zfill(2)+" sec")
        if self.count == 0:
            self.onCloseWindow(None)
        self.SetTransparent(self.alphaValue)

#--TrojanAttFrame--------------------------------------------------------------
    def onCloseWindow(self, evt):
        """ Stop the timeer and close the window."""
        self.changeAlpha_timer.Stop()
        del self.changeAlpha_timer       # avoid a memory leak
        self.Destroy()


if __name__ == "__main__":
    app = wx.App()
    #f = TrojanAttFrame(None)
    f = pwrGenLDisplay(None, 600, 100)
    #f = FancyFrame(300, 300)
    app.MainLoop()