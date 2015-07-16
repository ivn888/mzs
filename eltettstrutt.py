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

    ComboBox = dialog.findChild(QComboBox,"tipo_el")
    Label1 = dialog.findChild(QLabel,"lab_etichetta")
    textValore1=dialog.findChild(QLineEdit,"lab_a")
    textValore2=dialog.findChild(QLineEdit,"lab_b")

    # assegno l'azione chglabel al segnale di modifica del valore nella combo
    ComboBox.currentIndexChanged.connect(chglabel)

    chglabel()
    
    
def chglabel():
    # Aggiorno le etichette.
   
    if ComboBox.currentText()=='Traccia della sezione geologica rappresentativa del modello del sottosuolo':
        Label1.show()
        textValore1.show()
        textValore2.show()
    else:
    
        Label1.hide()
        textValore1.hide()
        textValore2.hide()


