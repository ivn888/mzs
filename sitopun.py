# -*- coding: utf-8 -*-
#-------------------------------------------------------------------------------
# Name:        sitopun.py
# Purpose:
#
# Author:      Luca Lanteri Arpa Piemonte
#
# Created:     05-10-2015
# Copyright:   (c) Luca Lanteri 2015
# Licence:     <GPL>
#-------------------------------------------------------------------------------
#!/usr/bin/env python

import sys, os, datetime
from PyQt4.QtCore import *
from PyQt4.QtGui import *
from qgis.utils import iface
from qgis.core import *
from PyQt4 import QtGui,uic
from qgis.gui import QgisInterface 
import mzs

DEBUGMODE=True

myDialog = None
myfeatureid = None
curLayer = None

sys.path.append(QgsProject.instance().homePath())

def formOpen(dialog,layerid,featureid):
    #definisco le variabili globali
    global myDialog, myfeatureid, curLayer
    global TblIndagini, LblIdSito, LblQuota
  
    curLayer=layerid
    myDialog =dialog
    myfeatureid=featureid
    
    # assegno gli oggetti della combo
    TblIndagini= myDialog.findChild(QTableWidget,"tableIndagini")
    LblIdSito= myDialog.findChild(QLineEdit,"pkey_spu")
    LblQuota= myDialog.findChild(QLineEdit,"quota_slm")
    datDataSito= myDialog.findChild(QDateEdit,"data_sito")
    
    
    #mette la data di default ad oggi quando e null
    if datDataSito.date().toString("dd/MM/yyyy")==QDate(1900,1,1).toString("dd/MM/yyyy"):
        datDataSito.setDateTime(datetime.datetime.now())
        
    #collego i segnali
    LblQuota.textChanged.connect(lambda: mzs.validaQuota(LblQuota))
    