# -*- coding: utf-8 -*-

from PyQt4.QtCore import *
from PyQt4.QtGui import *
from qgis.utils import iface

DEBUGMODE = True

nameField = None
myDialog = None
myfeatureid = None
curLayer = None


def formOpen(dialog,layerid,featureid):
    global myDialog
    myDialog = dialog
    global Label1, Label2, ComboBox, textValore1, textValore2, cmbTipo_gi

    ComboBox = dialog.findChild(QComboBox,"tipo_gi")
    Label1 = dialog.findChild(QLabel,"lbl_valore1")
    Label2 = dialog.findChild(QLabel,"lbl_valore2")
    textValore1=dialog.findChild(QLineEdit,"valore")
    textValore2=dialog.findChild(QLineEdit,"valore2")

    # assegno l'azione chglabel al segnale di modifica del valore nella combo
    ComboBox.currentIndexChanged.connect(chglabel)
    textValore1.editingFinished.connect(ctrldipdir)
    textValore2.editingFinished.connect(ctrldip)

    chglabel()
    ctrldipdir()
    ctrldip()
    
    
def chglabel():
    # Aggiorno le etichette.
    val = ComboBox.currentIndex()
    if val == 1: 
        Label1.setText("dip direction")
        Label2.setText("dip")
        Label2.show()
        textValore2.show()
    else:
        Label1.setText("Profondita' (m)")
        Label2.hide()
        textValore2.hide()


def ctrldipdir():
    try:
        if textValore1.displayText():           
            dipdir = int(str(textValore1.displayText()))
        else:
            return None

        if (dipdir > 360 or dipdir <0) and (ComboBox.currentText()=='Giacitura strati'):
            #QMessageBox.about(myDialog, "Info", "La quota top deve essere maggiore della quota bottom")
            textValore1.setStyleSheet("background-color: rgba(255, 107, 107, 150);")
        else:
            textValore1.setStyleSheet("background-color: rgba(0, 0, 0, 0);")
    except:
        print "Unexpected error: dato nullo"
    
def ctrldip():
    if textValore2.displayText():  
        dip = int(str(textValore2.displayText()))
    else:
        return None
    try:
        if (dip > 90 or dip <0) and (ComboBox.currentText()=='Giacitura strati'):
            #QMessageBox.about(myDialog, "Info", "La quota top deve essere maggiore della quota bottom")
            textValore2.setStyleSheet("background-color: rgba(255, 107, 107, 150);")
        else:
            textValore2.setStyleSheet("background-color: rgba(0, 0, 0, 0);")
    except:
        print "Unexpected error: dato nullo"
