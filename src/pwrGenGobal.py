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

print("Current working directory is : %s" % os.getcwd())
dirpath = os.path.dirname(__file__)
print("Current source code location : %s" % dirpath)
APP_NAME = 'Generator Manager [Ver:CORPLAB-2019-T3.1-P1]'

#------<IMAGES PATH>-------------------------------------------------------------
IMG_FD = 'img'
ICO_PATH = os.path.join(dirpath, IMG_FD, "geoIcon.ico")         # App Icon.
MOIMG_PATH = os.path.join(dirpath, IMG_FD, "motor.png")         # moto speed background image
PUIMG_PATH = os.path.join(dirpath, IMG_FD, "pump.png")          # pump speed background image
PGIMG_PATH = os.path.join(dirpath, IMG_FD, "pwrbg.png")         # power generator background image
SMKOIMG_PATH = os.path.join(dirpath, IMG_FD, "smoke_on.png")    # smoke on image
SMKFIMG_PATH = os.path.join(dirpath, IMG_FD, "smoke_off.png")   # smoke off image
SIRIMG_PATH = os.path.join(dirpath, IMG_FD, "siren.png")        # siren on image

#-------<GLOBAL VARIABLES (start with "g")>------------------------------------
# VARIABLES are the built in data type.
gUdpPort = 5005             # UDP communication port.
gAlphaValue = 200           # transparent alphaValue.(0-255)
gDisPnlPos  = (600, 780)    # Display panel popup default position.
gSubPnlPos  = (1100, 100)    # Substation panel popup default position.
gUpdateRate = 0.5           # main frame update rate min base 0.5 sec.
gTranspPct = 70             # Windows transparent percentage.

#-------<GLOBAL INSTANCES (start with "i")>-----------------------------------------------------
# INSTANCES are the object. 
iCtrlPanel = None           # Control panel
iDetailPanel = None         # Debug and manually control panel.
iMainFrame = None           # MainFrame.
iDisFrame = None            # Display frame.
iSubFrame = None            # Substation frame.
iMotoImgPnl = None          # Moto speed image panel.
iPumpImgPnl = None          # Pump image speed panel.
iPerGImgPnl = None          # Generator panel.
iPerSImgPnl = None          # Substation panel.
