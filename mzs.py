# -*- coding: utf-8 -*-
#-------------------------------------------------------------------------------
# Name:        mzs.py
# Purpose:
#
# Author:      Luca Lanteri Arpa Piemonte
#
# Created:     05-10-2015
# Copyright:   (c) Luca Lanteri 2015
# Licence:     <GPL>
#-------------------------------------------------------------------------------
#!/usr/bin/env python

from PyQt4.QtCore import *
from PyQt4.QtGui import *
from qgis.utils import iface
from qgis.core import QgsMapLayerRegistry
from qgis.core import *
import sys, os

DEBUGMODE = True

#__all__=["validaQuota"]
    
def validaQuota(Qline):
    try:
        #verifica che la quota non superi i 2500m
        if Qline.displayText():
            quota=float(Qline.displayText())
            if quota > 2500:
                Qline.setStyleSheet("background-color: rgba(255, 107, 107, 150);")
            else:
                Qline.setStyleSheet("background-color: rgba(255, 255, 255, 255);")
    except:
        return False

def updSpessore(QLineTop,QLineBottom,QLineSpessore):
    # calcola lo spessore dell'indagine
    try:
        if QLineTop.displayText():
            valTop=float(QLineTop.displayText())
        else:
            return False
        if QLineBottom.displayText():
            valBottom=float(QLineBottom.displayText())
        else:
            return False

        if (valTop > valBottom):
            #QMessageBox.about(indmyDialog, "Info", "La profondita' top deve essere minore della profondita' bottom")
            QLineTop.setStyleSheet("background-color: rgba(255, 107, 107, 150);")
            QLineBottom.setStyleSheet("background-color: rgba(255, 107, 107, 150);")
            QLineSpessore.setStyleSheet("background-color: rgba(255, 107, 107, 150);")
            QLineSpessore.setText("NULL")
            return None
        if (valTop != NULL) and (valTop != NULL):
            QLineSpessore.setText(str(float(valBottom)-float(valTop )))
            QLineSpessore.setStyleSheet("background-color: rgba(255, 255, 255, 255);")
            QLineTop.setStyleSheet("background-color: rgba(255, 255, 255, 255);")
            QLineBottom.setStyleSheet("background-color: rgba(255, 255, 255, 255);")

    except:
        QLineTop.setStyleSheet("background-color: rgba(255, 107, 107, 150);")
        QLineBottom.setStyleSheet("background-color: rgba(255, 107, 107, 150);")
        QLineSpessore.setStyleSheet("background-color: rgba(255, 107, 107, 150);")
        #indLedSpessore.setText("NULL")

def ctrlquota(QLineTop,QLineBottom):
    #controlla la validita' delle quote inserite
    try:
        if QLineTop.displayText():
            valQTop=float(QLineTop.displayText())
        else:
            return False
        if QLineBottom.displayText():
            valQBottom=float(QLineBottom.displayText())
        else:
            return False
    
        if (valQTop < valQBottom):
            #QMessageBox.about(indmyDialog, "Info", "La quota top deve essere maggiore della quota bottom")
            QLineTop.setStyleSheet("background-color: rgba(255, 107, 107, 150);")
            QLineBottom.setStyleSheet("background-color: rgba(255, 107, 107, 150);")
        else:
            QLineTop.setStyleSheet("background-color: rgba(255, 255, 255, 255);")
            QLineBottom.setStyleSheet("background-color: rgba(255, 255, 255, 255);")
    except:
        print "ctrlquota: errore"
        
def apriFile(QLine):
    fileName=QLine.text()
    try:
        if os.path.isfile(fileName):
                os.startfile(fileName)
        else:
                msgBox = QMessageBox()
                msgBox.setText("Il file non esiste.")
                msgBox.exec_()
    except:
        msgBox = QMessageBox()
        msgBox.setText("Non riesco ad aprire il file.")
        msgBox.exec_()

def selectFile(QLine):
    # gestisce il pulsante seleziona file
    filename= QFileDialog.getOpenFileName()
    if filename:
       QLine.setText(filename)
       
def chkEditState(layer,controlli):
    #attivo i controlli se il layer e' in editing
    if layer.isEditable():
        for i in controlli:
            i.setEnabled(True)
    else:
        for i in controlli:
            i.setEnabled(False)
            
def readTipoIndagini(layer):
    #legge i dati dalla tavola di decodifica 'tab_tipoindagine_pun' per popolare la combo tipoindagine
    #recupero gli attributi delle features e li carico in rsTipo
    #[0] TipoIndagineID - int
    #[1] TipoIndagine - text
    #[2] CodIndagine - text
    #[3] Classeindagine_id - int
    
    rsTipo=[]
    alist=[]
    for i in layer.getFeatures(QgsFeatureRequest().setFlags(QgsFeatureRequest.NoGeometry)):
        alist=[i.attributes()[0],i.attributes()[1],i.attributes()[2],i.attributes()[3]]
        rsTipo.append(alist)
    return rsTipo
