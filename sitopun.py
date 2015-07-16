import sys, os
from PyQt4.QtCore import *
from PyQt4.QtGui import *
from qgis.utils import iface
from qgis.core import *
from PyQt4 import QtGui,uic
from qgis.gui import QgisInterface 

DEBUGMODE=True

myDialog = None
myfeatureid = None
curLayer = None

def formOpen(dialog,layerid,featureid):
    #definisco le variabili globali
    global myDialog, myfeatureid, curLayer
    global TblIndagini, LblIdSito, LblQuota, BtnToggleEdit
    
    curLayer=layerid
    myDialog =dialog
    myfeatureid=featureid
    
    # assegno gli oggetti della combo
    TblIndagini= myDialog.findChild(QTableWidget,"tableIndagini")
    LblIdSito= myDialog.findChild(QLineEdit,"pkey_spu")
    BtnApriForm= myDialog.findChild(QPushButton,"btnApriForm")
    LblQuota= myDialog.findChild(QLineEdit,"quota_slm")
    BtnToggleEdit= myDialog.findChild(QPushButton,"btnTedit")
    
    readIndagine()
    popTblIndagini()
    
    #collego i segnali
    BtnApriForm.clicked.connect(apriForm)
    LblQuota.textChanged.connect(validaQuota)
    BtnToggleEdit.clicked.connect(toggleEdit)

    checkedit()

def readIndagine():
    # legge i dati dal layer 'indagini_puntuali' e li carica in rsTipoindagine
    global rsTipoindagine
    
    idSito=LblIdSito.displayText()
    aLayer = QgsMapLayerRegistry.instance().mapLayersByName('indagini_puntuali')[0]
    #recupero gli attributi delle features e popolo il vettore rsTipoindagine con i campi:
    # [4] ID_INDPU
    # [3] tipo_ind
    # [1] - pkey_spu
    
    lista=[]
    rsTipoindagine=[]
    
    for i in aLayer.getFeatures():
        alist=[i.attributes()[4],i.attributes()[3],i.attributes()[1]]
        if str(i[0])==str(idSito):
            rsTipoindagine.append(alist)

def popTblIndagini():
    # popola la tabella Indagini Collegate
    
    try:
        TblIndagini.setRowCount(len(rsTipoindagine))
        TblIndagini.setColumnCount(len(rsTipoindagine[0]))

        for i, row in enumerate(rsTipoindagine):
            for j, col in enumerate(row):
                item = QTableWidgetItem(str(col))
                TblIndagini.setItem(i, j, item)
        
        TblIndagini.setHorizontalHeaderLabels(['Sigla Indagine','Tipo Indagine','ID'])
    except:
        print "Unexpected error: Problemi nel popolare il tipo indagine"
        
        
def apriForm():
    # Apre il form delle indagini
    try:
        idIndagine=TblIndagini.selectedItems()
        aLayer = QgsMapLayerRegistry.instance().mapLayersByName('indagini_puntuali')[0]
        a= idIndagine[2].text()
        print a
        
        aFeature=aLayer.getFeatures(QgsFeatureRequest().setFilterFid(int(a)))
        for i in aFeature:
            aFeature1=i
            iface.openFeatureForm(aLayer, aFeature1,0)
    except:
        print "Unexpected error: Problemi nell'apertura del form"
        
def validaQuota():
    quota=unicode(LblQuota.displayText())
    if not isfloat(quota):
        LblQuota.setStyleSheet("background-color: rgba(255, 107, 107, 150);")
        msgBox = QMessageBox()
    else:
        LblQuota.setStyleSheet("")


def isfloat(value):
  try:
    float(value)
    return True
  except ValueError:
    return False

def toggleEdit():
        aLayer = QgsMapLayerRegistry.instance().mapLayersByName('sito_puntuale')[0]
        if not aLayer.isEditable():
                aLayer.startEditing()
        else:
                aLayer.rollBack(True)
        checkedit()

def checkedit():
        aLayer = QgsMapLayerRegistry.instance().mapLayersByName('sito_puntuale')[0]
        if aLayer.isEditable():
            BtnToggleEdit.setDown(True)
        else:
            BtnToggleEdit.setDown(False)

