import wx
import time
import json
#from wx.adv import Animation, AnimationCtrl
import wx.gizmos as gizmos
import pwrGenGobal as gv
import udpCom


#-----------------------------------------------------------------------------
#-----------------------------------------------------------------------------
class TrojanAttFrame(wx.Frame):
    """ Popup frame to show a transparent window to block the desktop to simulate
        the trojan attack.
    """
    def __init__(self, parent, width, height):
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
        #self.Maximize()
        #self.ShowFullScreen(True)
        self.Show()

#--TrojanAttFrame--------------------------------------------------------------
    def buidUISizer(self):
        """ Build the UI and the return the wx.sizer. """
        sizer = wx.BoxSizer(wx.VERTICAL)
        #self.ctrl = AnimationCtrl(self, -1, Animation("img\\motor.png"))
        #self.ctrl.Play()
        #sizer.Add(self.ctrl, flag=wx.ALIGN_CENTER_VERTICAL |
        #          wx.CENTER, border=2)
        image = wx.StaticBitmap(self, wx.ID_ANY)
        image.SetBitmap(wx.Bitmap("img\\pwrbg.png"))
        sizer.Add(image, flag=wx.ALIGN_CENTER_VERTICAL | wx.CENTER, border=2)
        #self.stTxt = wx.StaticText(
        #    self, -1, "Your computer has been took over by YC's Trojan, we will release control in 10 sec")
        #self.stTxt.SetBackgroundColour(wx.Colour('GREEN'))
        #self.stTxt.SetFont(wx.Font(30, wx.SWISS, wx.NORMAL, wx.NORMAL))
        #sizer.Add(self.stTxt, flag=wx.ALIGN_CENTER, border=2)
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
    f = TrojanAttFrame(None, 410, 230)
    #f = pwrGenLDisplay(None, 600, 100)
    #f = FancyFrame(300, 300)
    app.MainLoop()