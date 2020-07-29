import wx

class FancyFrame(wx.Frame):
    def __init__(self, width, height):
        wx.Frame.__init__(self, None,
                          style = wx.STAY_ON_TOP |
                          wx.FRAME_NO_TASKBAR |
                          wx.FRAME_SHAPED,
                          size=(width, height))
        self.panel = MainPanel(self)
        b = wx.Bitmap(width, height)
        dc = wx.MemoryDC()
        dc.SelectObject(b)
        dc.SetBackground(wx.Brush('black'))
        dc.Clear()
        dc.SetBrush(wx.TRANSPARENT_BRUSH)
        dc.SetPen(wx.Pen('red', 10))
        dc.DrawRectangle(0, 0, width, height)
        dc.SelectObject(wx.NullBitmap)
        b.SetMaskColour('black')
        self.SetBackgroundColour('red')

        self.SetShape(wx.Region(b))
        self.Centre()
        self.Show(True)

class MainPanel(wx.Panel):
    def __init__(self, frame):
        wx.Panel.__init__(self, frame)
        button_sizer = self._button_sizer(frame)
        main_sizer = wx.BoxSizer(wx.VERTICAL)
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

if __name__ == "__main__":
    app = wx.App()
    f = FancyFrame(300, 300)
    app.MainLoop()