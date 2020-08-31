# **Problem and Solution**

**In this document we will share the valuable problems and the solution we meet during the project development as a reference menu for the new programmer who may take over this project for further development. Later we will sort the problem based on the problem <type>.**

**Format:** 

**Problem**: (Situation description)

**Error Message**:

**Type**: Setup exception

**Solution**:

------

**Problem [0]**: cmd python3 cmd not exist on window server 2019 

**Error Message**: 

```py
'python3' is not recognized as an internal or external command,
operable program or batch file. 
```

**Type**: Setup exception

**Solution**: use cmd '**py**' instead of python3 link: https://stackoverflow.com/questions/39910730/python3-is-not-recognized-as-an-internal-or-external-command-operable-program

------

**Problem[1]**: After pip installed wxpython, can run "import wx" under py cmd terminal but py pwrGenRun.py got wx module is not installed error. 

**Error Message**: 'wx' module is not installed. 

**Type**: path setup permission error. 

**Solution**: Go to "C:\Users\liu_y\AppData\Local\Programs\Python\Python37-32" find the python.exe file, create the run.bat file with below contents: 

```
"C:\Users\liu_y\AppData\Local\Programs\Python\Python37-32\python.exe" "C:\Works\SingtelTw\OT_Platform\Power_Generator_Mgr\src\pwrGenRun.py"
pause
```

Run the program from the run.bat file.



------

**Problem [2]**: snap7 running time error after pip installed snap7 lib under windows.  

**Error Message**:

**Type**: Windows dll and lib file missing.

**Solution**: Computer **>** System Property **>** Advanced system settings **>** Environment Variables **>** System variable, add the path folder in: 

```
C:\Works\SingtelTw\OT_Platform\Power_Generator_Mgr\lib\Windows\Win32
```

