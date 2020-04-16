#-----------------------------------------------------------------------------
# Name:        uiGlobal.py
#
# Purpose:     This module is used as a local config file to set constants, 
#              global parameters which will be used in the other modules.
#              
# Author:      Yuancheng Liu
#
# Created:     2020/01/10
# Copyright:   YC @ Singtel Cyber Security Research & Development Laboratory
# License:     YC
#-----------------------------------------------------------------------------
import os

dirpath = os.getcwd()
print("Current working directory is : %s" % dirpath)
APP_NAME = 'Generator Mgr'

#------<IMAGES PATH>-------------------------------------------------------------
IMG_FD = 'img'
ICO_PATH = os.path.join(dirpath, IMG_FD, "geoIcon.ico") # App Icon.
MOIMG_PATH = os.path.join(dirpath, IMG_FD, "motor.png") # moto speed background image
PUIMG_PATH = os.path.join(dirpath, IMG_FD, "pump.png")  # pump speed background image

#-------<GLOBAL PARAMTERS>-----------------------------------------------------
iCtrlPanel = None   # Control panel
iDetailPanel = None # Debug and manually control panel.
iMainFrame = None   # MainFrame.
iMotoImgPnl = None  # Moto speed image panel.
iPumpImgPnl = None  # Pump image speed panel.
iUpdateRate = 0.5   # main frame update rate 1 sec.