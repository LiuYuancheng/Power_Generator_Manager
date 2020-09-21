#-----------------------------------------------------------------------------
# Name:        pwrGenGlobal.py
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

dirpath = os.path.dirname(__file__)
print("Current working directory is : %s" % dirpath)
APP_NAME = 'Generator Mgr'

#------<IMAGES PATH>-------------------------------------------------------------
IMG_FD = 'img'
ICO_PATH = os.path.join(dirpath, IMG_FD, "geoIcon.ico") # App Icon.
MOIMG_PATH = os.path.join(dirpath, IMG_FD, "motor.png") # moto speed background image
PUIMG_PATH = os.path.join(dirpath, IMG_FD, "pump.png")  # pump speed background image
PGIMG_PATH = os.path.join(dirpath, IMG_FD, "pwrbg.png")  # power generator background image
SMKOIMG_PATH = os.path.join(dirpath, IMG_FD, "smoke_on.png")  # smoke on image
SMKFIMG_PATH = os.path.join(dirpath, IMG_FD, "smoke_off.png")  # smoke off image
SIRIMG_PATH = os.path.join(dirpath, IMG_FD, "siren.png")  # siren on image

#-------<GLOBAL VARIABLES (start with "g")>------------------------------------
# VARIABLES are the built in data type.
gUdpPort = 5005     # UDP communication port.
gAlphaValue = 200   # transparent alphaValue.(0-255)


#-------<GLOBAL INSTANCES (start with "i")>-----------------------------------------------------
# INSTANCES are the object. 
iCtrlPanel = None   # Control panel
iDetailPanel = None # Debug and manually control panel.
iMainFrame = None   # MainFrame.
iDisFrame = None    # Display frame.
iMotoImgPnl = None  # Moto speed image panel.
iPumpImgPnl = None  # Pump image speed panel.
iPerGImgPnl = None  #
iUpdateRate = 0.5   # main frame update rate 1 sec.
