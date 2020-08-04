import wx
from wx.adv import Animation, AnimationCtrl

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


#-----------------------------------------------------------------------------
#-----------------------------------------------------------------------------
class TrojanAttFrame(wx.Frame):
    """ Popup frame to show a transparent window to block the desktop to simulate
        the trojan attack.
    """
    def __init__(self, parent):
        wx.Frame.__init__(self, parent, title="TrojanAttFrame",style=wx.MINIMIZE_BOX)
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
        #          wx.ALIGN_CENTER_HORIZONTAL, border=2)
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
    f = TrojanAttFrame(None)
    #f = FancyFrame(300, 300)
    app.MainLoop()