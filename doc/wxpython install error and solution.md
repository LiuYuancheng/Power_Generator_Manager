install wxpython on Ubuntu 20.04 with 

Error 1: 
No package 'gtk+-3.0' found
    Package gthread-2.0 was not found in the pkg-config search path.
    Perhaps you should add the directory containing `gthread-2.0.pc'
    to the PKG_CONFIG_PATH environment variable
    No package 'gthread-2.0' found
    no
    *** Could not run GTK+ test program, checking why...
    *** The test program failed to compile or link. See the file config.log for the
    *** exact error that occurred. This usually means GTK+ is incorrectly installed.
 

sudo apt-get install python-wxgtk3.0

sudo apt-get install python3-wxgtk4.0 python3-wxgtk-webview4.0 python3-wxgtk-media4.0

sudo pip3 install -U -f https://extras.wxpython.org/wxPython4/extras/linux/gtk3/ubuntu-16.04 wxPython

 
Error 2: 
 python 3.8.2 (default, Jul 16 2020, 14:00:26) 
[GCC 9.3.0] on linux
Type "help", "copyright", "credits" or "license" for more information.
>>> import wx
Traceback (most recent call last):
  File "<stdin>", line 1, in <module>
  File "/usr/local/lib/python3.8/dist-packages/wx/__init__.py", line 17, in <module>
    from wx.core import *
  File "/usr/local/lib/python3.8/dist-packages/wx/core.py", line 12, in <module>
    from ._core import *
ImportError: libSDL2-2.0.so.0: cannot open shared object file: No such file or directory


 sudo apt-get install git curl libsdl2-mixer-2.0-0 libsdl2-image-2.0-0 libsdl2-2.0-0
 
Python 3.8.2 (default, Jul 16 2020, 14:00:26) 
[GCC 9.3.0] on linux
Type "help", "copyright", "credits" or "license" for more information.
>>> import wx
Traceback (most recent call last):
  File "<stdin>", line 1, in <module>
  File "/usr/local/lib/python3.8/dist-packages/wx/__init__.py", line 17, in <module>
    from wx.core import *
  File "/usr/local/lib/python3.8/dist-packages/wx/core.py", line 12, in <module>
    from ._core import *
ImportError: libpng12.so.0: cannot open shared object file: No such file or directory

 download install packge from : 
 https://www.dropbox.com/s/79x3imq73tcqyw4/libpng12-0_1.2.54-1ubuntu1b_amd64.deb?dl=0
 sudo dpkg -i libpng12-0_1.2.54-1ubuntu1b_amd64.deb
 
 
 

