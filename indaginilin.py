from PyQt4.QtCore import *
from PyQt4.QtGui import *
from qgis.utils import iface
from qgis.core import QgsMapLayerRegistry
from qgis.core import *
import os

DEBUGMODE = True

nameField = None
myDialog = None
myfeatureid = None
curLayer = None

def formOpen(dialog,layerid,featureid):
    # avviata all'apertura del form
    
    #definisco le variabili globali
    global myDialog, myfeatureid, curLayer
    global ComboBoxClasse, ComboBoxTipo, LineEditTipo
    global TblParametri, LedidParametro, BtnApriForm
    global LedFilename, PbtFile, LedSpessore, LedTop, LedBottom
    global LedQtop, LedQbottom, BtnApriFile
        
    curLayer=layerid
    myDialog =dialog
    myfeatureid=featureid
    
    # assegno gli oggetti della combo
    ComboBoxClasse = myDialog.findChild(QComboBox,"classe_ind")
    ComboBoxTipo = myDialog.findChild(QComboBox,"tipo_indcmb")
    LineEditTipo = myDialog.findChild(QLineEdit,"tipo_ind")
    
    TblParametri= myDialog.findChild(QTableWidget,"tableParametri")
    LedidParametro= myDialog.findChild(QLineEdit,"pkey_indln")
    BtnApriForm= myDialog.findChild(QPushButton,"btnApriForm")
    LedFilename= myDialog.findChild(QLineEdit,"doc_ind")
    BtnFile = myDialog.findChild(QPushButton,"btnFile")
    BtnApriFile= myDialog.findChild(QPushButton,"btnApriFile")
    
    #collego i segnali
    ComboBoxClasse.activated.connect(updateComboClasse)
    ComboBoxTipo.activated.connect(updateComboTipo)
    BtnApriForm.clicked.connect(apriForm)
    BtnFile.clicked.connect(selectFile)
    BtnApriFile.clicked.connect(apriFile)
    
    if curLayer.isEditable():
       ComboBoxTipo.setEnabled(True)
       BtnFile.setEnabled(True)
    else:
       ComboBoxTipo.setEnabled(False)
       BtnFile.setEnabled(False)
       
    readTipoIndagini()
    updateComboClasse()
    readComboTipo()
    readIndagine()
    popTblParametri()
           
def readTipoIndagini():
    #legge i dati dalla tavola di decodifica 'tab_tipoindagine_lin' per popolare la combo tipoindagine
    global rsTipo
        
    aLayer = QgsMapLayerRegistry.instance().mapLayersByName('tab_tipoindagine_lin')[0]
    #recupero gli attributi delle features
    #[0] TipoIndagineID - int
    #[1] TipoIndagine - text
    #[2] Tipo_ind - text
    
    alist=[]
    rsTipo=[]
    
    for i in aLayer.getFeatures(QgsFeatureRequest().setFlags(QgsFeatureRequest.NoGeometry)):
        alist=[i.attributes()[0],i.attributes()[1],i.attributes()[2],i.attributes()[3]]
        rsTipo.append(alist)
      
def readComboTipo():
    # Aggiorna la combo Tipo Indagine con il valore contenuti in LineEditTipo
    try:
        valtxt = LineEditTipo.displayText()
        if valtxt =='NULL' or valtxt =='':
            ComboBoxTipo.setCurrentIndex(0)
        else:
            ComboBoxTipo.setCurrentIndex(dicTipo[valtxt])
    except:
        print "Unexpected error:"

def updateComboClasse():
    # quando viene agiornata la Classe Indagine popola la combo Tipo Indagine
    
    global dicTipo
    dicTipo={}
    
    val = ComboBoxClasse.currentIndex()
    #aggiorno i valori nella combobox Tipo
    ComboBoxTipo.clear()
    ComboBoxTipo.addItem("No Data")
    x=1
    for row in rsTipo:
        if row[3]==val:
            ComboBoxTipo.addItem(row[1])
            dicTipo[row[2]]=x
            x=x+1
    
def updateComboTipo():
    #quando viene aggiornata la combo Tipo Indagine valorizza LineEditTipo
     
    valtxt = ComboBoxTipo.currentText()
    theval=''
    for row in rsTipo:
        if row[1]==valtxt:
           theval=str(row[2])
        LineEditTipo.setText(theval)
 
        
def readIndagine():
# legge i dati dal layer 'indagini_puntuali' e li carica in rsParametri
    global rsParametri
    
    idSito=LedidParametro.displayText()
    aLayer = QgsMapLayerRegistry.instance().mapLayersByName('parametri_lineari')[0]
    #recupero gli attributi delle features e popolo il vettore rsParametri con i campi:
    # [3] ID_PARPU
    # [2] tipo_parpu
    # [1] - pkey_indpu
    
    lista=[]
    rsParametri=[]
    
    for i in aLayer.getFeatures():
        alist=[i.attributes()[3],i.attributes()[2],i.attributes()[1]]
        if str(i[0])==str(idSito):
            rsParametri.append(alist)

def popTblParametri():
    # popola la tabella Parmetri Collegati
    
    try:
        TblParametri.setRowCount(len(rsParametri))
        TblParametri.setColumnCount(len(rsParametri[0]))

        for i, row in enumerate(rsParametri):
            for j, col in enumerate(row):
                item = QTableWidgetItem(str(col))
                TblParametri.setItem(i, j, item)
        
        TblParametri.setHorizontalHeaderLabels(['Sigla Parametro','Tipo Parametro','ID'])
    except:
        print "Unexpected error: Problemi nel popolare il tipo parametro"
        
def apriForm():
    # Apre il form dei parametri al click sul bottone
    
    try:
        idParametro=TblParametri.selectedItems()
        aLayer = QgsMapLayerRegistry.instance().mapLayersByName('parametri_lineari')[0]
        a= idParametro[2].text()
        
        aFeature=aLayer.getFeatures(QgsFeatureRequest().setFilterFid(int(a)))
        for i in aFeature:
            print i
            iface.openFeatureForm(aLayer, i,0)
    except:
        print "Unexpected error: Problemi nell'apertura del form"
        
def selectFile():
    filename= QFileDialog.getOpenFileName()
    if filename:
       LedFilename.setText(filename)

def apriFile():
    fileName=LedFilename.text()                     
    
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