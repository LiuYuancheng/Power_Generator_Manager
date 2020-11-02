# **Problem and Solution**

**In this document we will share the valuable problems and the solution we meet during the project development as a reference menu for the new programmer who may take over this project for further development. Later we will sort the problem based on the problem <type>.**

[TOC]



**Format:** 

**Problem**: (Situation description)

**OS Platform** :

**Error Message**:

**Type**: Setup exception

**Solution**:

**Related Reference**:



------

###### Problem [0]: cmd python3 cmd not exist on window server 2019 

**Error Message**: 

```py
'python3' is not recognized as an internal or external command,
operable program or batch file. 
```

**OS Platform** : Windows Server 2019 Ver2.

**Type**: Setup exception

**Solution**: use cmd '**py**' instead of python3 

**Related Reference**: https://stackoverflow.com/questions/39910730/python3-is-not-recognized-as-an-internal-or-external-command-operable-program



------

###### Problem[1]: After pip installed wxpython, can run "import wx" under py cmd terminal but py pwrGenRun.py got wx module is not installed error. 

**Error Message**: 'wx' module is not installed. 

**OS Platform** : Windows Server 2019 Ver2.

**Type**: path setup permission error. 

**Solution**: Go to "C:\Users\liu_y\AppData\Local\Programs\Python\Python37-32" find the python.exe file, create the run.bat file with below contents: 

```
"C:\Users\liu_y\AppData\Local\Programs\Python\Python37-32\python.exe" "C:\Works\SingtelTw\OT_Platform\Power_Generator_Mgr\src\pwrGenRun.py"
pause
```

Run the program from the run.bat file.



------

###### Problem [2]: snap7 running time error after pip installed snap7 lib under windows.  

**Error Message**: 

```
Traceback (most recent call last):
  File "Y:\Lonnox\Projekte\Bibliothek\Python und SPS\S7-1200 Test.py", line 6, in <module>
    plc = snap7.client.Client()
  File "C:\Python34\lib\site-packages\snap7\client.py", line 30, in __init__
    self.library = load_library()
  File "C:\Python34\lib\site-packages\snap7\common.py", line 54, in load_library
    return Snap7Library(lib_location).cdll
  File "C:\Python34\lib\site-packages\snap7\common.py", line 46, in __init__
    raise Snap7Exception(msg)
snap7.snap7exceptions.Snap7Exception: can't find snap7 library. If installed, try running ldconfig
```

**OS Platform** : Windows 7, Windows 10.

**Type**: Windows dll and lib file missing.

**Solution**: Computer **>** System Property **>** Advanced system settings **>** Environment Variables **>** System variable, add the path folder in: 

```
C:\Works\SingtelTw\OT_Platform\Power_Generator_Mgr\lib\Windows\Win32
```

**Related Reference**:  https://stackoverflow.com/questions/33697263/python-snap7-windows-cant-find-snap7-library



------

###### Problem [3]: install wxpython on Ubuntu 20.04 fail.

**Error Message**:

```
No package 'gtk+-3.0' found
    Package gthread-2.0 was not found in the pkg-config search path.
    Perhaps you should add the directory containing `gthread-2.0.pc'
    to the PKG_CONFIG_PATH environment variable
    No package 'gthread-2.0' found
    no
    *** Could not run GTK+ test program, checking why...
    *** The test program failed to compile or link. See the file config.log for the
    *** exact error that occurred. This usually means GTK+ is incorrectly installed.
```

**OS Platform** : Ubuntu 16.04, 18.04,  20.04.

**Type**: UI dependency package not installed. 

**Solution**:

- Solution 1 : Install python with gtk package bind in: 

  ```
  sudo apt install libgtk-3-dev
  sudo apt-get install python-wxgtk3.0
  ```

- Solution 2 : If solution show install error for latest Ubuntu version(20.04), install the related dependency package: 

  ```
  sudo apt-get install python3-wxgtk4.0 python3-wxgtk-webview4.0 python3-wxgtk-media4.0
  ```

- Solution 3 : After finished tried solution 2, if "pip install wxPython " still not work,  install the specific wxpython package: 

  ```
  sudo pip3 install -U -f https://extras.wxpython.org/wxPython4/extras/linux/gtk3/ubuntu-16.04 wxPython
  ```

  

------

###### Problem [4]: Successful installed wxpython but got error during import. 

**Error Message**:

```
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
```

**OS Platform** : Ubuntu  20.04.

**Type**: Lib not installed. 

**Solution**:

```
sudo apt-get install git curl libsdl2-mixer-2.0-0 libsdl2-image-2.0-0 libsdl2-2.0-0
```



------

###### Problem [5]:  Successful installed wxpython but got error during import. 

**Error Message**:

```
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
```

**OS Platform** : Ubuntu 20.04.

**Type**:  Lib not installed. 

**Solution**:

Download the lib deb from below link or from the folder "lib/libpng12-0_1.2.54-1ubuntu1b_amd64.deb"

https://www.dropbox.com/s/79x3imq73tcqyw4/libpng12-0_1.2.54-1ubuntu1b_amd64.deb?dl=0

Install the lib by cmd: 

```
 sudo dpkg -i libpng12-0_1.2.54-1ubuntu1b_amd64.deb
```

**Related Reference**: 

- https://www.blog.neudeep.com/python/install-wxpython-with-solved-importerror/501/

- https://www.cnblogs.com/dyc99/p/12600913.html

- https://askubuntu.com/questions/1136302/can-not-install-libpng12-so-0-on-ubuntu-19-04-for-packet-tracert-7

  

------

###### Problem [6]: The program is running and created the background process record, but the Background process control program shows "The program is NOT running" .

**OS Platform** : Ubuntu 20.04, Raspbian. 

**Error Message**: N.A.

**Type**: Permission access limitation caused problem. 

**Solution**:

if we run the background program with "sudo" permission, if we want to check we also need to sudo run the BgCtrl.py to control. 

- python3 pwrGenMgr.py  + python 3 BgCtrl.py => work
- python3 pwrGenMgr.py  + sudo python 3 BgCtrl.py => work
- sudo python3 pwrGenMgr.py  + python 3 BgCtrl.py => not work

**Related Reference**: 

------

###### Problem[7]: Set auto run when start up on CentOs Linux7 in rc.local and cause the system can not boot up

**OS Platform** : CentOs Linux7

**Error Message**: The system hang during enter the system. 

> A start job is running for /etc/rc.local Compatibility 

**Type**: N.a 

**Solution**:

- Reboot the system, wait until the system selection page and press "e" to enter the grub mode. 

- Some message will be show below: 

  > root (hd0,0)
  > kernel /vmlinuz-2.6.18-128.el5 ro root=LABEL=/ rhgb quiet
  > initrd /initrd-2.6.18-128.el5.img

  Move to line "kernel /vmlinuz-2.6.18-128.el5 ro root=LABEL=/ rhgb quiet
  initrd /initrd-2.6.18-128.el5.img"  and add the word "single" behind "quiet"

  > kernel /vmlinuz-2.6.18-128.el5 ro root=LABEL=/ rhgb **quiet**
  > initrd /initrd-2.6.18-128.el5.img

- Press the Ctrl+x to run the system under the config. Then type in the admin password to enter the system cmd line mode. 
- cd to /etc/rc.d/ or vim /etc/rc.d/rc.local then removed all the line in the rc.local. Save the file and reboot the system. 

**Related Reference**:

https://blog.csdn.net/m0_38078650/article/details/101944002

https://blog.csdn.net/freudlv/article/details/46549303

https://blog.csdn.net/baobingji/article/details/85239527

http://blog.ckeck.cn/?p=126

------

